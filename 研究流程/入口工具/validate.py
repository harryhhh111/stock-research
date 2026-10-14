"""研究入口试点校验与章节提取。运行方法见同目录 README.md。"""
import argparse
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
KEYS = {'schema_version', 'entity_id', 'kind', 'name', 'aliases', 'securities',
        'primary_document', 'documents', 'related_entities', 'sections'}
MARKETS = {'US': {'XNYS', 'XNAS'}, 'HK': {'XHKG'}, 'CN': {'XSHG', 'XSHE', 'XBSE'}}
MIC_MARKET = {mic: market for market, mics in MARKETS.items() for mic in mics}
SEMANTICS = {'thesis', 'open_questions', 'metrics', 'risks', 'research_metadata'}

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f'重复 YAML 键: {key}')
        result[key] = loader.construct_object(value_node)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def require(condition, message):
    if not condition:
        raise ValueError(message)

def shape(value, required, optional=()):
    require(isinstance(value, dict), '需要映射对象')
    require(set(required) <= value.keys() and value.keys() <= set(required) | set(optional),
            f'字段缺失或未知: {list(value)}')

def string(value):
    require(isinstance(value, str) and bool(value.strip()), '需要非空字符串')

def strings(value):
    require(isinstance(value, list), '需要列表')
    for item in value:
        string(item)

def document(root, entry, value):
    string(value)
    require(not Path(value).is_absolute(), f'禁止绝对路径: {value}')
    path = (entry.parent / value).resolve()
    require(path.is_relative_to(root.resolve()), f'路径越界: {value}')
    require(path.is_file() and path.suffix == '.md', f'Markdown 文件不存在: {value}')
    return path

def extract(text, heading_path, limit=None):
    """按真实标题祖先链定位；跳过 fenced code，保留完整章节。"""
    lines = text.splitlines(keepends=True)
    headings, stack = [], []
    fence = None
    for index, line in enumerate(lines):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if marker:
            run = marker[1]
            if fence is None:
                fence = (run[0], len(run))
            elif run[0] == fence[0] and len(run) >= fence[1] and not line[marker.end():].strip():
                fence = None
            continue
        if fence:
            continue
        match = re.match(r'^ {0,3}(#{1,6})\s+(.+?)\s*$', line)
        if not match:
            continue
        level = len(match[1])
        title = re.sub(r'\s+#+\s*$', '', match[2])
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, title))
        headings.append((index, level, [item[1] for item in stack]))
    matches = [h for h in headings if h[2] == heading_path]
    if len(matches) != 1:
        return {'status': 'missing' if not matches else 'ambiguous', 'text': ''}
    start, level, _ = matches[0]
    end = next((i for i, depth, _ in headings if i > start and depth <= level), len(lines))
    body = ''.join(lines[start:end]).strip()
    truncated = limit is not None and len(body) > limit
    return {'status': 'truncated' if truncated else 'ok', 'text': body[:limit] if truncated else body,
            'line': start + 1, 'total_chars': len(body)}

def read_entry(root, entry, limit=None):
    data = yaml.load(entry.read_text(encoding='utf-8'), Loader=UniqueLoader)
    shape(data, KEYS - {'aliases'}, {'aliases'})
    require(type(data['schema_version']) is int and data['schema_version'] in (1, 2), '未知 schema_version')
    string(data['entity_id']); string(data['name'])
    require(re.fullmatch(r'(company|topic|protocol|token|other):[a-z0-9][a-z0-9-]*', data['entity_id']), '非法 ID')
    require(data['kind'] == data['entity_id'].split(':')[0], 'kind 与 ID 不匹配')
    strings(data.get('aliases', []))
    for field in ('securities', 'documents', 'related_entities'):
        require(isinstance(data[field], list), f'{field} 需要列表')
    require(data['kind'] == 'company' or not data['securities'], '非公司不能填股票证券')
    for security in data['securities']:
        shape(security, {'mic', 'symbol'} if data['schema_version'] == 1 else {'market', 'mic', 'symbol'})
        string(security['symbol'])
        require(isinstance(security['mic'], str) and re.fullmatch('[A-Z0-9]{4}', security['mic']), '非法 MIC')
        require(security['symbol'] == security['symbol'].upper(), '证券代码须大写')
        require(security['mic'] in MIC_MARKET, '未知或未支持 MIC')
        if data['schema_version'] == 1:
            security['market'] = MIC_MARKET[security['mic']]
        string(security['market'])
        require(security['market'] in MARKETS, '未知或未支持 market')
        require(security['mic'] in MARKETS[security['market']], 'market/MIC 不匹配')
    declared = {document(root, entry, data['primary_document'])}
    for doc in data['documents']:
        shape(doc, {'path', 'role'})
        require(doc['role'] in {'supplement', 'opinion', 'review', 'source'}, '非法文档角色')
        path = document(root, entry, doc['path'])
        require(path not in declared, '重复文档路径')
        declared.add(path)
    for relation in data['related_entities']:
        shape(relation, {'entity_id', 'relation'})
        string(relation['entity_id'])
        require(relation['relation'] in {'theme', 'related', 'parent', 'subsidiary', 'underlying'}, '非法关系')
    shape(data['sections'], SEMANTICS)
    sections = {}
    for key, locator in data['sections'].items():
        if locator is None:
            sections[key] = {'status': 'missing', 'text': ''}
            continue
        shape(locator, {'path', 'heading_path'})
        strings(locator['heading_path'])
        require(bool(locator['heading_path']), '标题链不能为空')
        path = document(root, entry, locator['path'])
        require(path in declared, '章节引用未声明文档')
        sections[key] = {**extract(path.read_text(encoding='utf-8'), locator['heading_path'], limit),
                         'path': str(path.relative_to(root.resolve()))}
    return {**data, 'entry': str(entry.relative_to(root.resolve())), 'extracted_sections': sections,
            'market_source': 'explicit' if data['schema_version'] == 2 else 'inferred-from-mic',
            'warnings': [] if data['schema_version'] == 2 else ['旧格式版本 1：market 由已知 MIC 推导，请迁移到版本 2']}

def lookup_market(report, market, symbol, mic=None):
    matches = [data for data in report['entities'] if any(
        s['market'] == market and s['symbol'] == symbol and (mic is None or s['mic'] == mic)
        for s in data['securities'])]
    return {'status': 'missing' if not matches else 'ok' if len(matches) == 1 else 'ambiguous',
            'entity_ids': [data['entity_id'] for data in matches]}

def validate(root=ROOT, limit=None):
    root = root.resolve()
    entities, securities, errors = {}, {}, []
    excluded = {'.git', '.venv', 'venv', '__pycache__', '参考库', 'node_modules'}
    for entry in sorted(root.rglob('research.yaml')):
        if any(p in excluded for p in entry.relative_to(root).parts):
            continue
        try:
            data = read_entry(root, entry, limit)
            identity = data['entity_id']
            require(identity not in entities, f'重复 ID: {identity}')
            pending = [(s['mic'], s['symbol']) for s in data['securities']]
            require(len(set(pending)) == len(pending), '入口内重复证券')
            for security in pending:
                require(security not in securities, f'重复证券: {security}')
            entities[identity] = data
            for security in pending:
                securities[security] = identity
        except (ValueError, yaml.YAMLError, OSError, TypeError) as exc:
            errors.append({'entry': str(entry.relative_to(root)), 'error': str(exc)})
    for identity, data in entities.items():
        for relation in data['related_entities']:
            if relation['entity_id'] not in entities:
                errors.append({'entry': data['entry'], 'error': f"关联不存在: {relation['entity_id']}"})
            elif relation['relation'] == 'theme' and entities[relation['entity_id']]['kind'] != 'topic':
                errors.append({'entry': data['entry'], 'error': 'theme 目标必须为主题'})
    return {'source': 'working-tree', 'version_note': '本地工作树预览，未声明为已审核 commit',
            'errors': errors, 'entities': list(entities.values()),
            'security_index': {f'{mic}:{symbol}': identity for (mic, symbol), identity in securities.items()}}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--limit', type=int, help='每个章节最多展示字符数，截断会显式标记')
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error('--limit 必须为正整数')
    report = validate(args.root.resolve(), args.limit)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(bool(report['errors']))
