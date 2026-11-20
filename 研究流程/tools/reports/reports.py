#!/usr/bin/env python3
"""Manage explicit HTML report registration. No research facts are inferred."""
import argparse
import hashlib
from copy import deepcopy
from datetime import date
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    raise SystemExit('缺少报告工具依赖，请按 HTML报告命名与索引规范.md 安装 requirements.txt')

DEFAULT_ROOT = Path(__file__).resolve().parents[3]
INDEX = Path('研究流程/index/html-index.json')
SCHEMA = DEFAULT_ROOT / INDEX.with_suffix('.schema.json')
LEGACY_INDEX_PATHS = ('研究流程/索引/html-index.json', '研究流程/html-index.json')
# Frozen migration exceptions: new reports cannot opt into arbitrary legacy locations.
LEGACY_PATHS = {
    'MSFT/MSFT.html', 'MSFT/传统软件与现金流.html', 'AMD/近期股价催化.html',
    'QXO/QXO.html', 'AI_BERKSHIRE/微软-AI-Berkshire研究试验-2026-11-15.html',
    '估值反推Skill/演示报告.html',
}
EXCLUDED_PARTS = {'.git', '.venv', 'venv', '__pycache__', 'node_modules', 'factcheck', 'assets', 'skills', '参考库'}
EXCLUDED_ROOTS = {'研究流程', 'docs', '.github'}
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
COMPANY_MODULE_CARD_ORDER = (
    'industry-position.html', 'business-model.html', 'revenue-profit.html',
    'cash-capital.html', 'governance.html', 'valuation.html',
)
SCHEMA_VALIDATOR = Draft202012Validator(json.loads(SCHEMA.read_text()), format_checker=FormatChecker())
Draft202012Validator.check_schema(SCHEMA_VALIDATOR.schema)


class ReportError(ValueError):
    pass


def unique_object(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise ReportError(f'JSON重复字段：{k}')
        obj[k] = v
    return obj


def load(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object,
                      parse_constant=lambda v: (_ for _ in ()).throw(ReportError(f'非法JSON常量：{v}')))


def repo_path(root, value, must_exist=True):
    """Manifest paths are literal POSIX paths, not URL-encoded paths."""
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value:
        raise ReportError(f'无效仓库路径：{value!r}')
    p = PurePosixPath(value)
    if p.is_absolute() or str(p) != value or '..' in p.parts or ':' in p.parts[0]:
        raise ReportError(f'路径必须规范、相对且不可越界：{value}')
    target = root.joinpath(*p.parts)
    walk = root
    for part in p.parts:
        walk = walk / part
        if walk.is_symlink():
            raise ReportError(f'不允许符号链接：{value}')
    if not target.resolve().is_relative_to(root.resolve()):
        raise ReportError(f'路径越界：{value}')
    if must_exist and not target.is_file():
        raise ReportError(f'文件不存在：{value}')
    return target


def excluded(path):
    parts = PurePosixPath(path).parts
    return (not parts or parts[0] in EXCLUDED_ROOTS or any(p in EXCLUDED_PARTS for p in parts)
            or path.startswith(('AI_BERKSHIRE/repo/', 'AI_BERKSHIRE/原生研究/')))


def candidates(root):
    result = subprocess.run(['git', '-C', str(root), 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
                            capture_output=True, check=True)
    return {p for p in result.stdout.decode('utf-8').split('\0')
            if p.lower().endswith('.html') and not excluded(p) and (root / p).is_file()}


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.card_links = []
        self.ids = set()
        self.duplicate_ids = set()
        self.base = False
        self.feed(source)
        for value in re.findall(r'url\(\s*[\"\x27]?([^\)\"\x27]+)', source, re.I):
            self.refs.append(('dependency', value.strip()))
        for value in re.findall(r'\bfetch\(\s*[\"\x27]([^\"\x27]+)', source):
            self.refs.append(('dependency', value))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and 'card' in (a.get('class') or '').split():
            self.card_links.append(a.get('href') or '')
        if tag == 'base':
            self.base = True
        if 'id' in a:
            if a['id'] in self.ids:
                self.duplicate_ids.add(a['id'])
            self.ids.add(a['id'])
        for key in ('href', 'src', 'poster'):
            if key in a:
                self.refs.append(('link' if tag == 'a' and key == 'href' else 'dependency', a[key]))
        if 'srcset' in a:
            if a['srcset'].lstrip().startswith('data:'):
                # Ambiguous comma separators in inline data: require explicit src instead.
                self.refs.append(('invalid-srcset', a['srcset']))
            else:
                for item in a['srcset'].split(','):
                    if item.strip():
                        self.refs.append(('dependency', item.strip().split()[0]))


def check_company_card_order(page):
    names = []
    for href in page.card_links:
        url = urlsplit(href)
        names.append(PurePosixPath(unquote(url.path)).name if not (url.scheme or url.netloc) else '')
    modules = [name for name in names if name in COMPANY_MODULE_CARD_ORDER]
    if not modules:
        return
    expected = [name for name in COMPANY_MODULE_CARD_ORDER if name in modules]
    if names[0] != COMPANY_MODULE_CARD_ORDER[0] or names[:len(modules)] != expected:
        raise ReportError('公司首页卡片须以行业开始，业务发布后居第二，已发布模块保持固定顺序：'
                          + ' → '.join(COMPANY_MODULE_CARD_ORDER))


def resolve_ref(root, entry, url):
    if not url or url.isspace():
        raise ReportError('空资源/链接地址')
    u = urlsplit(url)
    if u.scheme or u.netloc:
        if u.scheme in ('http', 'https') or u.netloc:
            return None, None, 'remote'
        if u.scheme in ('mailto', 'tel', 'data'):
            return None, None, u.scheme
        raise ReportError(f'禁止的URL协议：{url}')
    decoded = unquote(u.path)
    if re.search(r'%[0-9a-fA-F]{2}', decoded):
        raise ReportError(f'拒绝多重URL编码：{url}')
    if '\\' in decoded or '\x00' in decoded or decoded.startswith('/'):
        raise ReportError(f'禁止绝对/特殊路径：{url}')
    target = (root / entry).parent / decoded if decoded else root / entry
    resolved = target.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ReportError(f'链接越出研究库：{url}')
    rel = resolved.relative_to(root.resolve()).as_posix()
    # Check unresolved components too: an in-repo symlink is still disallowed.
    cursor = target
    while cursor != root and cursor.is_relative_to(root):
        if cursor.is_symlink():
            raise ReportError(f'链接使用符号链接：{url}')
        cursor = cursor.parent
    return rel, unquote(u.fragment), 'local'


def validate(root, index, discover=True):
    errors, warnings = [], []
    for e in sorted(SCHEMA_VALIDATOR.iter_errors(index), key=lambda e: str(list(e.absolute_path))):
        errors.append(f'索引结构 {list(e.absolute_path)}: {e.message}')
    if errors:
        return errors, warnings
    rows = index['reports']
    ids, paths, mains = set(), set(), set()
    aliases = {a['from']: a['report_id'] for a in index['redirects']}
    if len(aliases) != len(index['redirects']):
        errors.append('重复兼容入口路径')
    by_id = {r['report_id']: r for r in rows}
    pages = {}
    for r in rows:
        label = r['report_id']
        try:
            if label in ids:
                raise ReportError('report_id重复')
            ids.add(label)
            if r['entry_path'] in paths:
                raise ReportError('正文路径重复')
            paths.add(r['entry_path'])
            project = r['project_dir']
            repo_path(root, project + '/.placeholder', must_exist=False)
            if excluded(project + '/file.html') or project.endswith('/reports'):
                raise ReportError('project_dir须为公司/主题目录，不是工具、证据或reports目录')
            path = repo_path(root, r['entry_path'])
            if not path.is_relative_to(root / project):
                raise ReportError('正文不在指定project_dir内')
            if path.suffix != '.html' or excluded(r['entry_path']):
                raise ReportError('正文须为可展示的.html，不得登记原始证据或模板')
            if r['layout'] == 'legacy':
                if r['entry_path'] not in LEGACY_PATHS:
                    raise ReportError('仅固定的六份历史报告可使用legacy路径')
            else:
                rel = PurePosixPath(r['entry_path']).relative_to(PurePosixPath(project))
                if len(rel.parts) != 2 or rel.parts[0] != 'reports':
                    raise ReportError('正文须直接位于 <project_dir>/reports/')
                name = rel.name
                if r['report_type'] == 'company_research':
                    if name != 'main.html':
                        raise ReportError('公司主报告必须命名main.html')
                elif name == 'main.html':
                    raise ReportError('main.html仅供公司主报告')
                elif r['report_type'] == 'update':
                    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.html', name):
                        raise ReportError('更新命名须为YYYY-MM-DD-slug.html')
                    date.fromisoformat(name[:10])
                elif not SLUG.fullmatch(path.stem):
                    raise ReportError('专题/演示文件名须为小写英文slug.html')
            if r['report_type'] == 'company_research':
                if not r['entity_id'] or not r['entity_id'].startswith('company:'):
                    raise ReportError('公司主报告须显式关联company主体')
                if r['status'] != 'archived':
                    if r['entity_id'] in mains:
                        raise ReportError('同一公司存在多份当前主报告')
                    mains.add(r['entity_id'])
            if r['report_type'] == 'demo' and r['content_status'] != 'synthetic':
                raise ReportError('demo须标记synthetic')
            if r['content_status'] == 'synthetic' and r['report_type'] != 'demo':
                raise ReportError('synthetic只能登记为demo')
            if r['status'] == 'ready':
                if 'data-report-scaffold' in path.read_text(encoding='utf-8'):
                    raise ReportError('尚为工具生成的占位草稿，不能标ready')
                if not r['document_updated_at'] or not r['content_sha256']:
                    raise ReportError('ready须有更新日和正文哈希')
            if r['status'] == 'ready' and r['content_status'] in ('unreviewed', 'partial'):
                warnings.append(f'{label}: 已交付阅读但内容核验状态={r["content_status"]}，网站须显示核验状态及缺口')
            if r['content_sha256'] and hashlib.sha256(path.read_bytes()).hexdigest() != r['content_sha256']:
                raise ReportError('正文已修改但索引内容哈希未同步；请复核后运行update')
            allowed = set(r['assets'])
            for asset in allowed:
                a = repo_path(root, asset)
                if a.suffix.lower() in ('.env', '.pem', '.key') or any(p.startswith(('.git', '.env')) for p in a.relative_to(root).parts):
                    raise ReportError('禁止登记凭据/Git内部文件为资源')
                if asset == r['entry_path']:
                    raise ReportError('assets不要重复entry_path')
            p = Page(path.read_text(encoding='utf-8'))
            if p.base or p.duplicate_ids:
                raise ReportError('禁止base标签或重复HTML id')
            if r['report_type'] == 'company_research' and r['status'] != 'archived':
                check_company_card_order(p)
            pages[r['entry_path']] = p
        except (ReportError, ValueError, OSError) as exc:
            errors.append(f'{label}: {exc}')
    for old_path, report_id in aliases.items():
        try:
            if old_path in paths or report_id not in by_id:
                raise ReportError('兼容入口与正文冲突或目标报告不存在')
            if excluded(old_path) or not old_path.endswith('.html'):
                raise ReportError('兼容入口必须是研究HTML，不得放入排除目录')
            stub = repo_path(root, old_path)
            expected = redirect_html(old_path, by_id[report_id]['entry_path'])
            if stub.read_text(encoding='utf-8') != expected:
                raise ReportError('兼容页内容与工具生成的跳转页不一致')
        except (ReportError, OSError) as exc:
            errors.append(f'兼容入口 {old_path}: {exc}')
    for r in rows:
        p = pages.get(r['entry_path'])
        if not p:
            continue
        seen_blocked = set()
        for kind, url in p.refs:
            try:
                if kind == 'invalid-srcset':
                    raise ReportError('data: srcset暂不支持，请改用明确src')
                target, fragment, mode = resolve_ref(root, r['entry_path'], url)
                if mode != 'local':
                    if kind == 'dependency' and mode not in ('data',):
                        raise ReportError(f'核心展示不得依赖外网或其他协议资源：{url}')
                    continue
                if kind == 'link' and url in r['unpublished_links']:
                    seen_blocked.add(url)
                    continue
                file = repo_path(root, target)
                if kind == 'dependency' and target not in r['assets'] and target != r['entry_path']:
                    raise ReportError(f'展示依赖未登记assets：{url}')
                if kind == 'link' and target not in {r['entry_path'], *r['assets'], *paths, *aliases}:
                    raise ReportError(f'本地链接未登记为资源/报告，亦未声明未发布原因：{url}')
                if fragment and file.suffix == '.html':
                    effective = by_id[aliases[target]]['entry_path'] if target in aliases else target
                    other = pages.get(effective) or Page(repo_path(root, effective).read_text(encoding='utf-8'))
                    if fragment not in other.ids:
                        raise ReportError(f'章节锚点不存在：{url}')
            except (ReportError, ValueError, OSError) as exc:
                errors.append(f'{r["report_id"]}: {exc}')
        unused = set(r['unpublished_links']) - seen_blocked
        if unused:
            errors.append(f'{r["report_id"]}: 未发布链接声明已失效，应移除：{sorted(unused)}')
        if r['unpublished_links']:
            warnings.append(f'{r["report_id"]}: {len(r["unpublished_links"])}个来源链接尚未批准网站发布；状态={r["status"]}')
    if discover:
        try:
            for path in sorted(candidates(root) - paths - set(aliases)):
                errors.append(f'研究HTML未登记索引：{path}')
        except subprocess.CalledProcessError:
            errors.append('无法通过Git盘点研究HTML；请在研究库checkout运行')
    return errors, warnings


def save(root, index):
    errors, _ = validate(root, index, discover=False)
    if errors:
        raise ReportError('\n'.join(errors))
    dest = root / INDEX
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.html-index-', dir=dest.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(json.dumps(index, ensure_ascii=False, indent=2) + '\n')
        os.replace(tmp, dest)
    finally:
        if Path(tmp).exists():
            Path(tmp).unlink()


def conventional_path(project, kind, slug=None, day=None):
    if kind == 'company_research':
        return f'{project}/reports/main.html'
    if not slug or not SLUG.fullmatch(slug) or slug == 'main':
        raise ReportError('专题/更新/演示须提供非main的小写英文--slug')
    if kind == 'update':
        if not day:
            raise ReportError('更新报告须显式提供--date，不自动猜事件日期')
        date.fromisoformat(day)
        slug = day + '-' + slug
    return f'{project}/reports/{slug}.html'


def add_report(root, index, r, create=False):
    if any(x['report_id'] == r['report_id'] for x in index['reports']):
        raise ReportError('report_id已存在，请更新原报告元数据而非重复登记')
    p = repo_path(root, r['entry_path'], must_exist=not create)
    if create and p.exists():
        raise ReportError('文件已存在，请使用register登记；不会覆盖正文')
    new = deepcopy(index)
    new['reports'].append(r)
    if create:
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('x', encoding='utf-8') as f:
            f.write('<!doctype html>\n<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                    f'<title>{escape(r["title"])}</title><h1>{escape(r["title"])}</h1>'
                    '<p data-report-scaffold>草稿：尚未开展内容核验，不作为完整研究交付。</p></html>\n')
    try:
        save(root, new)
    except Exception:
        if create:
            p.unlink()  # Only the placeholder created by this invocation.
        raise


def metadata_update(root, index, report_id, patch):
    if not isinstance(patch, dict):
        raise ReportError('元数据补丁必须是JSON对象')
    immutable = {'report_id','entry_path','project_dir','layout','entity_id','report_type'}
    if immutable & patch.keys():
        raise ReportError('更新不可改身份/路径；迁移请使用move，主体变更须人工审查')
    new = deepcopy(index)
    r = next((r for r in new['reports'] if r['report_id'] == report_id), None)
    if r is None:
        raise ReportError('未知report_id')
    r.update(patch)
    r['content_sha256'] = hashlib.sha256(repo_path(root, r['entry_path']).read_bytes()).hexdigest()
    save(root, new)


def redirect_html(old_path, dest):
    relative = os.path.relpath(dest, str(PurePosixPath(old_path).parent)).replace(os.sep, '/')
    href = quote(relative, safe='/')
    return ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>报告已迁移</title>'
            f'<p>报告已迁移：<a href="{escape(href)}">打开标准入口</a>。旧地址仅为兼容。</p>'
            f'<script>location.replace({json.dumps(href)}+location.hash)</script></html>\n')


def move_report(root, index, report_id, slug=None, day=None):
    """Move self-contained HTML while retaining registered compatibility pages."""
    new = deepcopy(index)
    r = next((r for r in new['reports'] if r['report_id'] == report_id), None)
    if r is None:
        raise ReportError('未知report_id')
    old_path = r['entry_path']
    dest = conventional_path(r['project_dir'], r['report_type'], slug, day)
    if dest == old_path:
        raise ReportError('已处于指定标准路径')
    old = repo_path(root, old_path)
    target = repo_path(root, dest, must_exist=False)
    if target.exists():
        raise ReportError('目标已存在，不覆盖')
    page = Page(old.read_text(encoding='utf-8'))
    for _, url in page.refs:
        resolved, _, mode = resolve_ref(root, old_path, url)
        if mode == 'local' and resolved != old_path:
            raise ReportError('正文有跨文件相对依赖；请先审阅重写引用和生成脚本，再登记标准路径，不自动搬迁')
    # Move does not change research timestamps or its review status.
    original = old.read_bytes()
    rollback = {root / a['from']: (root / a['from']).read_bytes()
                for a in index['redirects'] if a['report_id'] == report_id}
    rollback[old] = original
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as f:
        f.write(original)
    r.update(entry_path=dest, layout='standard')
    new['redirects'].append({'from':old_path,'report_id':report_id})
    try:
        for a in new['redirects']:
            if a['report_id'] == report_id:
                (root / a['from']).write_text(redirect_html(a['from'],dest),encoding='utf-8')
        save(root, new)
    except Exception:
        for path, content in rollback.items():
            path.write_bytes(content)
        target.unlink()
        raise
    return {'old_path':old_path,'entry_path':dest,'compatibility':'旧址保留登记的兼容页；禁脚本时点击链接，启用脚本时保留锚点跳转'}


def check_git_base(root, index, base):
    """Prevent silent deletion of stable report identities relative to a Git base."""
    # Whole-tree scanning covers unregistered HTML. Never infer fact-check dates.
    if not re.fullmatch(r'[A-Za-z0-9_./-]+', base) or base.startswith('-'):
        return ['无效Git基准引用']
    exists = subprocess.run(['git','-C',str(root),'rev-parse','--verify',f'{base}^{{commit}}'],capture_output=True)
    if exists.returncode:
        return ['Git基准引用不存在，请拉取完整历史']
    for index_path in (INDEX.as_posix(), *LEGACY_INDEX_PATHS):
        result = subprocess.run(['git','-C',str(root),'show',f'{base}:{index_path}'],capture_output=True,text=True)
        if not result.returncode:
            break
    else:
        # No index existed before initial rollout. Whole-tree validation still applies.
        return []
    old = json.loads(result.stdout)
    ids = {r['report_id']:r for r in index['reports']}
    errors=[]
    for r in old['reports']:
        if r['report_id'] not in ids:
            errors.append(f'索引不得静默删除历史ID，改用archive：{r["report_id"]}')
    return errors


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=DEFAULT_ROOT)
    sub=p.add_subparsers(dest='command',required=True)
    check=sub.add_parser('check');check.add_argument('--base-ref',default='HEAD')
    sub.add_parser('list')
    for command in ('create','register'):
        q=sub.add_parser(command)
        q.add_argument('--id',required=True);q.add_argument('--project',required=True)
        q.add_argument('--title',required=True);q.add_argument('--entity')
        q.add_argument('--type',choices=['company_research','topic','update','demo'],required=True)
        q.add_argument('--slug');q.add_argument('--date')
        q.add_argument('--metadata',type=Path,help='可选JSON补充元数据；不可覆盖ID、项目、类型或计算出的路径')
    q=sub.add_parser('update');q.add_argument('--id',required=True);q.add_argument('--metadata',type=Path,required=True)
    q=sub.add_parser('archive');q.add_argument('--id',required=True)
    q=sub.add_parser('move');q.add_argument('--id',required=True);q.add_argument('--slug');q.add_argument('--date')
    args=p.parse_args(argv);root=args.root.resolve()
    try:
        index=load(root/INDEX)
        if args.command != 'check':
            issues=list(SCHEMA_VALIDATOR.iter_errors(index))
            if issues:
                raise ReportError(f'索引结构无效：{issues[0].message}')
        if args.command=='check':
            errors,warnings=validate(root,index)
            if args.base_ref:errors+=check_git_base(root,index,args.base_ref)
            print(json.dumps({'reports':len(index['reports']) if isinstance(index,dict) and isinstance(index.get('reports'),list) else 0,'errors':errors,'warnings':warnings},ensure_ascii=False,indent=2))
            return 1 if errors else 0
        if args.command=='list':
            print(json.dumps(index,ensure_ascii=False,indent=2));return 0
        if args.command in ('create','register'):
            entry=conventional_path(args.project,args.type,args.slug,args.date)
            r={'report_id':args.id,'entity_id':args.entity,'project_dir':args.project,'title':args.title,
               'entry_path':entry,'report_type':args.type,'status':'draft','content_status':'synthetic' if args.type=='demo' else 'unreviewed',
               'document_updated_at':None,'financial_as_of':None,'market_as_of':None,
               'assets':[],'unpublished_links':{},'layout':'standard','content_sha256':None}
            if args.metadata:
                patch=load(args.metadata)
                if not isinstance(patch,dict) or {'report_id','project_dir','entity_id','title','entry_path','report_type','layout'} & patch.keys():
                    raise ReportError('补充元数据不得覆盖命令明确的身份、类型或路径')
                r.update(patch)
            add_report(root,index,r,create=args.command=='create')
            print(entry)
        elif args.command=='update':metadata_update(root,index,args.id,load(args.metadata))
        elif args.command=='archive':metadata_update(root,index,args.id,{'status':'archived'})
        elif args.command=='move':print(json.dumps(move_report(root,index,args.id,args.slug,args.date),ensure_ascii=False))
        return 0
    except (ReportError,ValueError,OSError,subprocess.SubprocessError) as exc:
        print(f'报告工具错误：{exc}',file=sys.stderr);return 2


if __name__=='__main__':
    sys.exit(main())
