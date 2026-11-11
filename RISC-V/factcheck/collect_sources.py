"""保存公开网页证据；不覆盖已有快照。PDF下载地址见data/sources.json。"""
from pathlib import Path
import json, hashlib
import requests
P=Path(__file__).resolve().parent/'data'
S={
'sifive-business-model':'https://www.sifive.com/about/business-model',
'sifive-2026-funding':'https://www.sifive.com/press/sifive-raises-400-million-to-accelerate-high-performance-risc-v-data-center-solutions',
'sifive-2026-amd':'https://www.sifive.com/press/sifive-amd-rocm-riscv-datacenter-servers',
'sifive-2026-bigsky':'https://www.sifive.com/press/risc-v-in-the-datacenter-bigsky-development-server',
'riscv-2026-market-methodology':'https://riscv.org/blog/shd-forecast-2026/',
'andes-q3-announcement-secondary':'https://www.ahan.net/announcements.php?q=6533',
'andes-share-issue-secondary':'https://www.nstock.tw/news/article_m?id=553703',
'andes-price-secondary':'https://www.cnyes.com/twstock/ps_historyprice.aspx?code=6533',
'eswin-quote-secondary':'https://www.itiger.com/hant/stock/01256/filings',
'eswin-monthly-secondary':'https://www.hstong.com/news/detail/26110421300491859'
}
manifest=[]
for name,url in S.items():
 f=P/('2026-11-11-'+name+'.html')
 try:
  if not f.exists(): f.write_bytes(requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=15).content)
  manifest.append({'url':url,'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'retrieved':'2026-11-11'})
 except Exception as e:manifest.append({'url':url,'error':str(e),'retrieved':'2026-11-11'})
(P/'web-sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print([(x.get('file'),x.get('error','ok')) for x in manifest])
