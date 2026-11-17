from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'reports.py'
spec=importlib.util.spec_from_file_location('reports',SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ReportTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  subprocess.run(['git','init','-q',str(self.root)],check=True)
  self.index={'schema_version':1,'reports':[],'redirects':[]}
  (self.root/m.INDEX).parent.mkdir(parents=True);self.write_index()
 def write_index(self):
  (self.root/m.INDEX).write_text(json.dumps(self.index,ensure_ascii=False))
 def file(self,path,body='<html><h1 id="top">Example</h1></html>'):
  p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body);return p
 def record(self,path='TEST/reports/main.html',rid='test-main',kind='company_research'):
  return {'report_id':rid,'title':'测试报告','entity_id':'company:test','project_dir':'TEST','entry_path':path,
   'report_type':kind,'status':'draft','content_status':'unreviewed','document_updated_at':None,
   'financial_as_of':None,'market_as_of':None,'assets':[],'unpublished_links':{},'layout':'standard','content_sha256':None}
 def registered(self,**kwargs):
  r=self.record(**kwargs);self.file(r['entry_path']);self.index['reports'].append(r);return r
 def errors(self):return m.validate(self.root,self.index)[0]
 def test_valid_registered_report(self):
  self.registered();self.assertEqual(self.errors(),[])
 def test_unregistered_html_outside_reports_is_detected(self):
  self.file('TEST/forgotten.html');self.assertTrue(any('未登记' in x for x in self.errors()))
 def test_raw_templates_and_ignored_checkouts_excluded(self):
  for p in ['TEST/factcheck/data/source.html','TEST/reports/assets/template.html','TEST/skills/pkg/assets/report.html',
            '参考库/test/report.html','AI_BERKSHIRE/repo/report.html']:
   self.file(p)
  self.assertEqual(self.errors(),[])
 def test_untracked_not_ignored_html_is_detected(self):
  self.file('TEST/reports/new.html');self.assertIn('TEST/reports/new.html',m.candidates(self.root))
 def test_registered_missing_file(self):
  self.index['reports'].append(self.record());self.assertTrue(any('不存在' in x for x in self.errors()))
 def test_duplicate_id_and_entry(self):
  r=self.registered();self.index['reports'].append(deepcopy(r));self.assertTrue(self.errors())
 def test_duplicate_main_across_directories(self):
  self.registered();r=self.record('OTHER/reports/main.html','other-main');r['project_dir']='OTHER'
  self.file(r['entry_path']);self.index['reports'].append(r)
  self.assertTrue(any('多份当前主报告' in x for x in self.errors()))
 def test_arbitrary_legacy_escape_rejected(self):
  r=self.registered(path='TEST/old.html');r['layout']='legacy'
  self.assertTrue(any('六份历史' in x for x in self.errors()))
 def test_layout_and_update_date(self):
  for path,kind in [('TEST/foo.html','topic'),('TEST/reports/main.html','topic'),
                    ('TEST/reports/2026-02-30-news.html','update')]:
   with self.subTest(path=path):
    r=self.record(path,'case',kind);self.file(path)
    self.assertTrue(m.validate(self.root,{'schema_version':1,'reports':[r],'redirects':[]},discover=False)[0])
 def test_path_traversal_and_symlinks(self):
  for path in ['../outside.html','/tmp/file.html','TEST/../outside.html','TEST//reports/main.html']:
   with self.subTest(path=path),self.assertRaises(m.ReportError):m.repo_path(self.root,path)
  self.file('actual.html');(self.root/'TEST').symlink_to(self.root,target_is_directory=True)
  with self.assertRaises(m.ReportError):m.repo_path(self.root,'TEST/actual.html')
 def test_unknown_keys_and_bad_date(self):
  r=self.registered();r['surprise']=True;self.assertTrue(self.errors())
  del r['surprise'];r['financial_as_of']='2026-02-30';self.assertTrue(self.errors())
 def test_demo_must_be_synthetic(self):
  r=self.registered(path='TEST/reports/demo.html',kind='demo');self.assertTrue(self.errors())
  r['content_status']='synthetic';self.assertEqual(self.errors(),[])
 def ready(self,r):
  r.update(status='ready',document_updated_at='2026-11-17',content_sha256=__import__('hashlib').sha256((self.root/r['entry_path']).read_bytes()).hexdigest())
 def test_ready_requires_date_and_hash(self):
  r=self.registered();r['status']='ready';self.assertTrue(self.errors())
  self.ready(r);self.assertEqual(self.errors(),[])
  r['document_updated_at']=None;self.assertTrue(self.errors())
  r['document_updated_at']='2026-11-17';r['content_sha256']=None;self.assertTrue(self.errors())
 def test_ready_keeps_independent_content_status_and_warns(self):
  r=self.registered();self.ready(r)
  for state in ['unreviewed','partial','verified']:
   with self.subTest(state=state):
    r['content_status']=state;errors,warnings=m.validate(self.root,self.index)
    self.assertEqual(errors,[]);self.assertEqual(r['content_status'],state)
    self.assertEqual(any('内容核验状态=' in x for x in warnings),state!='verified')
 def test_ready_allows_explicitly_unavailable_source(self):
  r=self.registered();self.file(r['entry_path'],'<a href="../factcheck/missing.json">source</a>')
  r['unpublished_links']={'../factcheck/missing.json':'未纳入网站访问范围'};self.ready(r)
  errors,warnings=m.validate(self.root,self.index)
  self.assertEqual(errors,[]);self.assertTrue(any('来源链接' in x for x in warnings))
 def test_unpublished_link_does_not_exempt_display_dependency(self):
  r=self.registered();self.file(r['entry_path'],'<a href="assets/chart.json">source</a><script>fetch("assets/chart.json")</script>')
  r['unpublished_links']={'assets/chart.json':'附件未开放'};self.ready(r)
  self.assertTrue(any('不存在' in x for x in self.errors()))
  self.file('TEST/reports/assets/chart.json','{}')
  self.assertTrue(any('展示依赖未登记assets' in x for x in self.errors()))
 def test_image_must_exist_and_be_registered(self):
  r=self.registered();self.file(r['entry_path'],'<img src="assets/image.png">');self.file('TEST/reports/assets/image.png','not real image')
  self.assertTrue(any('未登记assets' in x for x in self.errors()))
  r['assets']=['TEST/reports/assets/image.png'];self.assertEqual(self.errors(),[])
  (self.root/r['assets'][0]).unlink();self.assertTrue(self.errors())
 def test_source_link_requires_explicit_visibility(self):
  r=self.registered();self.file(r['entry_path'],'<a href="../factcheck/data/source.json">source</a>')
  self.file('TEST/factcheck/data/source.json','{}');self.assertTrue(self.errors())
  r['unpublished_links']={'../factcheck/data/source.json':'尚未批准发布'}
  self.assertEqual(self.errors(),[])
  self.file(r['entry_path'],'<h1>updated</h1>');self.assertTrue(any('声明已失效' in x for x in self.errors()))
 def test_relative_encoded_path_and_anchor(self):
  r=self.registered();self.file(r['entry_path'],'<a href="assets/%E4%B8%AD%E6%96%87.html#x">x</a>')
  self.file('TEST/reports/assets/中文.html','<h1 id="x">x</h1>');r['assets']=['TEST/reports/assets/中文.html']
  self.assertEqual(self.errors(),[])
  self.file('TEST/reports/assets/中文.html','<h1>no id</h1>');self.assertTrue(self.errors())
 def test_double_encoding_and_absolute_links_rejected(self):
  r=self.registered()
  for link in ['%252e%252e/secret.html','/etc/passwd','file:///etc/passwd','../../../../secret','javascript:alert(1)']:
   with self.subTest(link=link):
    self.file(r['entry_path'],f'<a href="{link}">bad</a>');self.assertTrue(self.errors())
 def test_css_fetch_and_srcset_dependencies(self):
  r=self.registered()
  for body in ['<style>body{background:url(assets/bg.png)}</style>',
               '<script>fetch("assets/data.json")</script>',
               '<img srcset="assets/small.png 1x, assets/large.png 2x">']:
   with self.subTest(body=body):
    self.file(r['entry_path'],body);self.assertTrue(self.errors())
 def test_external_sources_allowed_external_assets_rejected(self):
  r=self.registered();self.file(r['entry_path'],'<a href="https://example.com/filing">source</a>');self.assertEqual(self.errors(),[])
  self.file(r['entry_path'],'<script src="https://example.com/lib.js"></script>');self.assertTrue(self.errors())
 def test_duplicate_anchors_and_base_rejected(self):
  r=self.registered()
  for body in ['<p id="x"></p><p id="x"></p>','<base href="https://example.com">','<a href="#missing">x</a>']:
   self.file(r['entry_path'],body);self.assertTrue(self.errors())
 def test_create_register_update_archive(self):
  r=self.record();m.add_report(self.root,self.index,r,create=True)
  idx=m.load(self.root/m.INDEX);self.assertTrue((self.root/r['entry_path']).exists())
  m.metadata_update(self.root,idx,'test-main',{'status':'archived'});self.assertEqual(m.load(self.root/m.INDEX)['reports'][0]['status'],'archived')
  with self.assertRaises(m.ReportError):m.metadata_update(self.root,idx,'test-main',{'entry_path':'bad.html'})
  with self.assertRaises(m.ReportError):m.metadata_update(self.root,idx,'test-main',[])
 def test_failed_create_rolls_back_no_overwrite(self):
  r=self.record();r['unknown']=True
  with self.assertRaises(m.ReportError):m.add_report(self.root,self.index,r,create=True)
  self.assertFalse((self.root/r['entry_path']).exists());self.assertEqual(m.load(self.root/m.INDEX),self.index)
  p=self.file(r['entry_path'],'keep')
  with self.assertRaises(m.ReportError):m.add_report(self.root,self.index,self.record(),create=True)
  self.assertEqual(p.read_text(),'keep')
 def test_register_existing_and_reject_raw(self):
  r=self.record();self.file(r['entry_path']);m.add_report(self.root,self.index,r)
  r=self.record('TEST/factcheck/raw.html','bad','topic');r['layout']='legacy';self.file(r['entry_path'])
  with self.assertRaises(m.ReportError):m.add_report(self.root,self.index,r)
 def test_move_keeps_bytes_id_dates_and_registered_compatibility(self):
  r=self.registered(path='TEST/reports/topic.html',rid='topic',kind='topic');original=(self.root/r['entry_path']).read_bytes()
  result=m.move_report(self.root,self.index,'topic',slug='renamed')
  updated=m.load(self.root/m.INDEX)
  self.assertEqual(updated['reports'][0]['report_id'],'topic')
  self.assertIsNone(updated['reports'][0]['document_updated_at'])
  self.assertEqual((self.root/result['entry_path']).read_bytes(),original)
  self.assertEqual(m.validate(self.root,updated)[0],[])
  self.assertIn('location.hash',(self.root/result['old_path']).read_text())
  (self.root/result['old_path']).write_text('not a redirect');self.assertTrue(m.validate(self.root,updated)[0])
 def test_move_with_dependencies_refuses_without_changes(self):
  r=self.registered(path='TEST/reports/topic.html',rid='topic',kind='topic');self.file(r['entry_path'],'<a href="../note.md">x</a>')
  before=(self.root/r['entry_path']).read_bytes()
  with self.assertRaises(m.ReportError):m.move_report(self.root,self.index,'topic',slug='new')
  self.assertEqual((self.root/r['entry_path']).read_bytes(),before)
  self.assertFalse((self.root/'TEST/reports/new.html').exists())
 def test_schema_rejects_duplicate_json_fields(self):
  p=self.file('duplicate.json','{"reports":[],"reports":[]}')
  with self.assertRaises(m.ReportError):m.load(p)
 def test_git_base_prevents_silent_deletion(self):
  self.registered();self.write_index()
  subprocess.run(['git','-C',str(self.root),'add','.'],check=True)
  subprocess.run(['git','-C',str(self.root),'-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','fixture'],check=True)
  self.assertTrue(m.check_git_base(self.root,{'reports':[]},'HEAD'))
 def test_changed_ready_content_requires_hash_refresh(self):
  r=self.registered();r.update(document_updated_at='2026-11-17',content_status='partial',status='ready')
  r['content_sha256']=__import__('hashlib').sha256((self.root/r['entry_path']).read_bytes()).hexdigest()
  self.assertEqual(self.errors(),[])
  self.file(r['entry_path'],'<h1>changed</h1>');self.assertTrue(any('哈希' in x for x in self.errors()))
  self.write_index();m.metadata_update(self.root,self.index,r['report_id'],{})
  self.assertEqual(m.validate(self.root,m.load(self.root/m.INDEX))[0],[])
 def test_hidden_credentials_not_publishable(self):
  r=self.registered();self.file('TEST/.env','SECRET');r['assets']=['TEST/.env']
  self.assertTrue(self.errors())
 def test_generated_placeholder_cannot_be_marked_ready(self):
  r=self.record();m.add_report(self.root,self.index,r,create=True)
  idx=m.load(self.root/m.INDEX)
  with self.assertRaises(m.ReportError):
   m.metadata_update(self.root,idx,'test-main',{'status':'ready','content_status':'partial','document_updated_at':'2026-11-17'})
  self.assertEqual(m.load(self.root/m.INDEX)['reports'][0]['status'],'draft')
 def test_invalid_git_base_does_not_silently_skip(self):
  self.assertTrue(m.check_git_base(self.root,self.index,'--all'))
  self.assertTrue(m.check_git_base(self.root,self.index,'not-existing-ref'))
 def test_git_base_recognises_index_before_directory_move(self):
  self.registered();self.write_index()
  new_path=self.root/m.INDEX
  old_path=self.root/'研究流程/html-index.json'
  old_path.write_bytes(new_path.read_bytes());new_path.unlink()
  subprocess.run(['git','-C',str(self.root),'add','.'],check=True)
  subprocess.run(['git','-C',str(self.root),'-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','legacy location'],check=True)
  self.assertTrue(m.check_git_base(self.root,{'reports':[]},'HEAD'))
 def test_cli_from_other_directory(self):
  result=subprocess.run([__import__('sys').executable,str(SCRIPT),'--root',str(self.root),'create','--id','test-main','--project','TEST','--title','测试','--type','company_research','--entity','company:test'],cwd='/tmp',capture_output=True,text=True)
  self.assertEqual(result.returncode,0,result.stderr)
  subprocess.run(['git','-C',str(self.root),'-c','user.name=Test','-c','user.email=test@example.invalid','commit','--allow-empty','-qm','baseline'],check=True)
  result=subprocess.run([__import__('sys').executable,str(SCRIPT),'--root',str(self.root),'check'],capture_output=True,text=True)
  self.assertEqual(result.returncode,0,result.stderr)

if __name__=='__main__':unittest.main(verbosity=2)
