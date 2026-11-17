"""Optional developer QA: Playwright + installed Chrome; not a Skill runtime dependency."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / 'visual'
OUT.mkdir(exist_ok=True)
chrome = os.environ.get('VALUATION_QA_CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
records = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome, headless=True)
    for name, width, media in [('desktop',1280,'screen'),('mobile',390,'screen'),('print-style',1123,'print')]:
        context = browser.new_context(viewport={'width':width,'height':900}, java_script_enabled=False, offline=True)
        page = context.new_page()
        failures=[]
        page.on('pageerror', lambda err: failures.append(str(err)))
        page.goto((ROOT / '演示报告.html').as_uri())
        page.emulate_media(media=media)
        page.screenshot(path=str(OUT / (name+'.png')), full_page=True)
        result=page.evaluate('''() => ({
            width: innerWidth,
            bodyWidth: document.documentElement.scrollWidth,
            headingCount: document.querySelectorAll('section h2').length,
            tables: document.querySelectorAll('table').length,
            externalDependencies: document.querySelectorAll('script,link[rel="stylesheet"],img,iframe').length,
            cells: Array.from(document.querySelectorAll('td')).length,
            overflowContainers: Array.from(document.querySelectorAll('.scroll')).map(el=>({width:el.clientWidth,content:el.scrollWidth,overflow:getComputedStyle(el).overflowX})),
            containsResult: document.body.textContent.includes('8,052.55'),
            syntheticLabel: document.body.textContent.includes('纯示意数据'),
            allHeadingsVisible: Array.from(document.querySelectorAll('h2')).every(el=>el.getBoundingClientRect().width > 0)
        })''')
        assert result['bodyWidth'] <= width + 1, result
        assert result['headingCount']==4 and result['tables']==4, result
        assert result['externalDependencies']==0 and result['containsResult'] and result['syntheticLabel'],result
        assert not failures, failures
        if media=='print':
            assert all(x['content']<=x['width']+1 for x in result['overflowContainers']),result
        records.append({'view':name,'offline':True,'javascript_enabled':False,'page_errors':failures,**result})
        context.close()
    browser.close()
(Path(__file__).parent/'html_validation.json').write_text(json.dumps({'date':'2026-11-17','scope':'offline desktop/mobile and print CSS, not paginated print dialog','checks':records},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(records,ensure_ascii=False,indent=2))
