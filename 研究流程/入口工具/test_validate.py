import copy
import tempfile
import unittest
from pathlib import Path
import yaml
from validate import ROOT, extract, validate, lookup_market

class EntryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.base = yaml.safe_load((ROOT/'ORCL/research.yaml').read_text())
        self.base.update(primary_document='main.md', documents=[], related_entities=[])
        self.base['sections'] = {key: None for key in self.base['sections']}
        self.base['sections']['thesis'] = {'path':'main.md','heading_path':['研究','判断']}
        self.write('中文/嵌套', self.base)

    def write(self, folder, data):
        path=self.root/folder
        path.mkdir(parents=True,exist_ok=True)
        (path/'main.md').write_text('# 研究\n## 判断\n结论一\n### 证据\n证据二\n## 风险\n风险三\n')
        (path/'research.yaml').write_text(yaml.safe_dump(data,allow_unicode=True))
        return path

    def test_nested_and_complete_section(self):
        result=validate(self.root)
        self.assertFalse(result['errors'])
        self.assertEqual(result['security_index']['XNYS:ORCL'],'company:oracle')
        section=result['entities'][0]['extracted_sections']['thesis']
        self.assertIn('证据二',section['text'])
        self.assertNotIn('风险三',section['text'])

    def test_missing_ambiguous_fenced_and_truncated(self):
        self.assertEqual(extract('# A\n', ['B'])['status'],'missing')
        self.assertEqual(extract('# A\nx\n# A\ny', ['A'])['status'],'ambiguous')
        self.assertEqual(extract('# A\n```md\n# A\n```\n尾部', ['A'])['status'],'ok')
        self.assertEqual(extract('# A\n正文', ['A'], 3)['status'],'truncated')

    def test_duplicate_identity_and_security(self):
        self.write('duplicate', self.base)
        self.assertTrue(validate(self.root)['errors'])
        other=copy.deepcopy(self.base); other['entity_id']='company:another'
        self.write('duplicate',other)
        self.assertIn('重复证券',str(validate(self.root)['errors']))

    def test_invalid_fields_paths_version_relations(self):
        variants=[{'schema_version':3}, {'unexpected':1}, {'primary_document':'missing.md'},
                  {'primary_document':'../../outside.md'}, {'primary_document':'/tmp/outside.md'},
                  {'related_entities':[{'entity_id':'topic:unknown','relation':'theme'}]},
                  {'securities':[{'mic':'XNAS','symbol':123}]}]
        for update in variants:
            with self.subTest(update=update):
                data=copy.deepcopy(self.base); data.update(update)
                self.write('中文/嵌套',data)
                self.assertTrue(validate(self.root)['errors'])

    def test_duplicate_yaml_keys(self):
        path=self.root/'中文/嵌套/research.yaml'
        path.write_text(path.read_text()+'\nname: duplicate\n')
        self.assertIn('重复 YAML 键',str(validate(self.root)['errors']))

    def test_topic_and_multi_security(self):
        data=copy.deepcopy(self.base)
        data['securities'].append({'market':'HK','mic':'XHKG','symbol':'00123'})
        self.write('中文/嵌套',data)
        topic=copy.deepcopy(self.base)
        topic.update(entity_id='topic:nand',kind='topic',securities=[],related_entities=[
            {'entity_id':'company:oracle','relation':'related'}])
        self.write('主题',topic)
        result=validate(self.root)
        self.assertFalse(result['errors'])
        self.assertIn('XHKG:00123',result['security_index'])

    def test_market_validation(self):
        for security in ({'mic':'XNYS','symbol':'ORCL'},
                         {'market':'XX','mic':'XNYS','symbol':'ORCL'},
                         {'market':'HK','mic':'XNYS','symbol':'ORCL'},
                         {'market':'US','mic':'XXXX','symbol':'ORCL'},
                         {'market':'CN','mic':'XBSE','symbol':'920001'}):
            with self.subTest(security=security):
                data=copy.deepcopy(self.base); data['securities']=[security]
                self.write('中文/嵌套',data)
                self.assertTrue(validate(self.root)['errors'])

    def test_legacy_market_inference(self):
        data=copy.deepcopy(self.base); data['schema_version']=1
        del data['securities'][0]['market']
        self.write('中文/嵌套',data)
        result=validate(self.root)
        self.assertFalse(result['errors'])
        entity=result['entities'][0]
        self.assertEqual(entity['securities'][0]['market'],'US')
        self.assertEqual(entity['market_source'],'inferred-from-mic')
        self.assertTrue(entity['warnings'])
        data['securities'][0]['mic']='XXXX'
        self.write('中文/嵌套',data)
        self.assertTrue(validate(self.root)['errors'])

    def test_market_lookup_and_ambiguity(self):
        other=copy.deepcopy(self.base); other['entity_id']='company:other'
        other['securities']=[{'market':'HK','mic':'XHKG','symbol':'ORCL'}]
        self.write('other',other)
        result=validate(self.root)
        self.assertFalse(result['errors'])
        self.assertEqual(lookup_market(result,'US','ORCL')['entity_ids'],['company:oracle'])
        self.assertEqual(lookup_market(result,'HK','ORCL')['entity_ids'],['company:other'])
        self.assertEqual(lookup_market(result,'CN','ORCL')['status'],'missing')
        other['securities']=[{'market':'US','mic':'XNAS','symbol':'ORCL'}]
        self.write('other',other)
        result=validate(self.root)
        self.assertEqual(lookup_market(result,'US','ORCL')['status'],'ambiguous')
        self.assertEqual(lookup_market(result,'US','ORCL','XNYS')['status'],'ok')

    def test_extended_market_combinations(self):
        for market,mic,symbol in [('CN','BJSE','920001'),('JP','XTKS','285A'),('KR','XKRX','000660'),
                                  ('DE','XETR','ENR'),('CA','XTSE','BB'),('TW','XTAI','2330'),
                                  ('IN','XNSE','TCS'),('FR','XPAR','CAP'),('AU','XASX','APX'),('IT','XMIL','PRY')]:
            with self.subTest(market=market):
                data=copy.deepcopy(self.base)
                data['securities']=[{'market':market,'mic':mic,'symbol':symbol}]
                self.write('中文/嵌套',data)
                self.assertFalse(validate(self.root)['errors'])

    def test_shared_primary_section_and_company_row(self):
        data=copy.deepcopy(self.base)
        data['primary_section']={'heading_path':['研究','比较'],'table_row':'Company A'}
        data['research_scope']='公司比较专题'
        path=self.write('中文/嵌套',data)
        (path/'main.md').write_text('# 研究\n## 比较\n| 公司 | 收入 |\n|---|---|\n| Company A | 10 |\n| Company B | 20 |\n| Company A | 30 |\n## 其他\n别的研究')
        result=validate(self.root)
        self.assertFalse(result['errors'])
        text=result['entities'][0]['primary_excerpt']['text']
        self.assertIn('| 公司 | 收入 |',text)
        self.assertIn('| Company A | 10 |',text)
        self.assertIn('| Company A | 30 |',text)
        self.assertNotIn('Company B',text)
        self.assertNotIn('别的研究',text)
        self.assertEqual(validate(self.root,limit=12)['entities'][0]['primary_excerpt']['status'],'truncated')
        data['primary_section']['table_row']='Unknown'
        self.write('中文/嵌套',data)
        self.assertTrue(validate(self.root)['errors'])
        data['primary_section']={'heading_path':['Unknown']}
        self.write('中文/嵌套',data)
        self.assertTrue(validate(self.root)['errors'])

    def test_full_library_sections_and_subject_boundaries(self):
        result=validate(ROOT)
        self.assertFalse(result['errors'])
        for entity in result['entities']:
            self.assertEqual(entity['schema_version'],2)
            for section in entity['extracted_sections'].values():
                if section.get('path'):
                    self.assertEqual(section['status'],'ok',entity['entry'])
            if entity.get('primary_section'):
                self.assertEqual(entity['primary_excerpt']['status'],'ok',entity['entry'])
        identities={e['entity_id']:e for e in result['entities']}
        for subject in ('company:haier-group','company:hitachi-energy','company:telus-digital','company:stateline-power'):
            self.assertEqual(identities[subject]['securities'],[])
        self.assertEqual(identities['company:haier-smart-home']['related_entities'][0]['entity_id'],'company:haier-group')

    def test_real_pilot(self):
        result=validate(ROOT)
        self.assertFalse(result['errors'])
        for data in result['entities']:
            if data['entity_id'] in {'company:oracle','company:nebius','company:intel','topic:nand'}:
                self.assertEqual(data['extracted_sections']['thesis']['status'],'ok')
        self.assertTrue({'company:oracle','company:nebius','company:intel','topic:nand'} <= {d['entity_id'] for d in result['entities']})

if __name__=='__main__':
    unittest.main()
