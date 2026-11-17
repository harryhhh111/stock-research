"""Offline SVG flows: reported group totals, no invented product cost allocations."""
from pathlib import Path
from html import escape
from bs4 import BeautifulSoup
import json
P=Path(__file__).resolve().parent
D=json.loads((P/'financials.json').read_text())
S=BeautifulSoup((P/'data/2026Q3.html').read_bytes(),'html.parser')
provenance={}
def raw(fid):
 n=S.find(id=fid);assert n is not None,fid
 t=n.get_text(strip=True).replace(',','');v=0 if t=='—' else float(t)
 v*=10**int(n.get('scale',0))/1e6
 if n.get('sign')=='-':v=-v
 provenance[fid]={'value':v,'tag':n.get('name'),'context':n.get('contextref'),'source':'data/2026Q3.html#'+fid}
 return v
q=D['quarters']['2026Q3'];products=D['products']['2026Q3']
rev=raw('f-131');cost=raw('f-135');gross=raw('f-139');sga=raw('f-143');dep=raw('f-147');amort=raw('f-151');op=raw('f-159')
assert rev==q['revenue'] and gross==q['gross'] and cost==q['cost']
flows={
'income':{'title':'2026Q3：收入来源 → 集团收入 → 成本、毛利与经营利润','unit':'MUSD','scale':.060,'width':1280,'height':640,'nodes':[
 ['roof','屋顶产品',products['roof'],155,65,'#194e72'],['insulation','保温与服务',products['insulation'],155,207,'#38799b'],['complement','配套建材',products['complement'],155,329,'#46a9a0'],['software','软件与服务',products['software'],155,427,'#8e9aa2'],
 ['revenue','集团收入',rev,415,112,'#194e72'],['cost','销售成本',cost,740,55,'#a76b56'],['gross','毛利',gross,740,386,'#388c77'],
 ['sga','销售管理费',sga,1040,330,'#a76b56'],['dep','折旧',dep,1040,435,'#a76b56'],['amort','摊销',amort,1040,493,'#a76b56'],['op','经营利润',op,1040,560,'#388c77']],
 'links':[['roof','revenue',products['roof']],['insulation','revenue',products['insulation']],['complement','revenue',products['complement']],['software','revenue',products['software']],['revenue','cost',cost],['revenue','gross',gross],['gross','sga',sga],['gross','dep',dep],['gross','amort',amort],['gross','op',op]]},
'cash':{'title':'2026年9M：现金来源 → 现金汇总 → 净用途与期末余额','unit':'MUSD','scale':.033,'width':1280,'height':665,'nodes':[], 'links':[]}}
start=raw('f-525');debt=raw('f-487')+raw('f-491')+raw('f-495');common=raw('f-503');seriesC=raw('f-507');awards=raw('f-501');other=-raw('f-483')
oper=-raw('f-477');capex=raw('f-479');acq=raw('f-481');finpay=sum(raw(x) for x in ['f-489','f-493','f-497','f-499','f-509','f-511','f-513','f-515','f-517']);end=raw('f-527')
total=start+debt+common+seriesC+awards+other
assert total==acq+oper+capex+finpay+end
assert debt+common+seriesC+awards-finpay==raw('f-519')
c=flows['cash'];c['nodes']=[['start','期初含受限现金',start,190,50,'#667c8b'],['debt','新增借款',debt,190,150,'#194e72'],['common','普通股净发行',common,190,371,'#38799b'],['seriesC','C优先股净发行',seriesC,190,420,'#46a9a0'],['awards','股权奖励行权',awards,190,545,'#667c8b'],['other','其他投资净流入',other,190,585,'#667c8b'],['pool','现金汇总',total,525,130,'#194e72'],['acq','并购净现金支付',acq,910,50,'#a76b56'],['oper','经营净耗现',oper,910,440,'#a76b56'],['capex','现金CapEx',capex,910,490,'#a76b56'],['finpay','融资现金支出',finpay,910,540,'#a76b56'],['end','期末含受限现金',end,910,605,'#388c77']]
c['links']=[[x,'pool',v] for x,v in [('start',start),('debt',debt),('common',common),('seriesC',seriesC),('awards',awards),('other',other)]]+[['pool',x,v] for x,v in [('acq',acq),('oper',oper),('capex',capex),('finpay',finpay),('end',end)]]
metadata={'date':'2026-11-17','source':'2026Q3 10-Q, 2026-11-13','provenance':provenance,'flows':flows,'financing_cash_paid':{'循环贷款偿还':raw('f-489'),'定期贷款偿还':raw('f-493'),'债务发行及融资费':raw('f-497'),'设备融资及融资租赁本金':raw('f-499'),'授股代扣税':raw('f-509'),'C优先股承诺费用':raw('f-511'),'A优先股现金分配':raw('f-513'),'B优先股现金分配':raw('f-515'),'C优先股现金分配':raw('f-517')}}
(P/'flow_data.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
def render(key):
 f=flows[key];k=f['scale'];ns={n[0]:n for n in f['nodes']};inpos={x:0 for x in ns};outpos={x:0 for x in ns};out=[]
 out.append(f'<svg viewBox="0 0 {f["width"]} {f["height"]}" role="img" aria-label="{escape(f["title"])}" data-flow="{key}" data-scale="{k}"><title>{escape(f["title"])}</title>')
 for a,b,v in f['links']:
  na,nb=ns[a],ns[b];x0=na[3]+16;x1=nb[3];y0=na[4]+outpos[a]*k;y1=nb[4]+inpos[b]*k;h=v*k;mid=(x0+x1)/2
  d=f'M{x0},{y0} C{mid},{y0} {mid},{y1} {x1},{y1} L{x1},{y1+h} C{mid},{y1+h} {mid},{y0+h} {x0},{y0+h} Z'
  out.append(f'<path d="{d}" fill="{na[5]}" opacity=".25" data-from="{a}" data-to="{b}" data-amount="{v}" data-thickness="{h}"/>');outpos[a]+=v;inpos[b]+=v
 for nid,label,v,x,y,color in f['nodes']:
  out.append(f'<rect x="{x}" y="{y}" width="16" height="{v*k}" fill="{color}" data-node="{nid}" data-amount="{v}"/>')
  isleft=(key=='income' and x==155) or (key=='cash' and x==190)
  if isleft:
   tx=8;ty=y+max(8,min(v*k/2,40));textanchor='start'
  elif nid in ['revenue','pool']:
   tx=x+8;ty=y-35;textanchor='middle'
  else:
   tx=x+27;ty=y+max(5,min(v*k/2,35));textanchor='start'
  out.append(f'<text x="{tx}" y="{ty}" text-anchor="{textanchor}" style="font-size:17px">{escape(label)}<tspan x="{tx}" dy="23" style="font-weight:650">{v:,.0f}</tspan></text>')
  if nid=='op':out.append(f'<text x="{x+27}" y="{ty+43}" style="font-size:14px">占收入0.04%；流量未放大</text>')
 out.append('</svg>');return ''.join(out)
