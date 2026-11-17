"""Generate the scoped HTML review; run from any directory. Prices are preserved inputs."""
import json
from pathlib import Path

base = Path(__file__).resolve().parent
d = json.loads((base/'data/2026-11-13-week-prices.json').read_text())
returns = {k:(v[-1]/v[0]-1)*100 for k,v in d['prices'].items()}
print('Five-session returns:', returns)
print('AMD vs Nov4:', (585.30/d['amd_nov4']-1)*100)
rows = ''.join(f'<tr><th>{k}</th><td>{v[0]:.2f}</td><td>{v[-1]:.2f}</td><td>{returns[k]:+.2f}%</td></tr>' for k,v in d['prices'].items())
daily = ''.join(f'<tr><th>{date}</th><td>{price:.2f}</td><td>{(price/d["prices"]["AMD"][i-1]-1)*100:+.2f}%</td></tr>' for i,(date,price) in enumerate(zip(d['dates'],d['prices']['AMD'])) if i)
colors = {'AMD':'#14665b','NVDA':'#a13a39','QQQ':'#7753a6','SOXX':'#b06d15'}
lines = ''
for k,v in d['prices'].items():
    pts = ' '.join(f'{70+i*110},{255-(p/v[0]-1)*100*4}' for i,p in enumerate(v))
    lines += f'<polyline fill="none" stroke="{colors[k]}" stroke-width="3" points="{pts}"/>'
labels = ''.join(f'<text x="{70+i*110}" y="320" text-anchor="middle">{date}</text>' for i,date in enumerate(d['dates']))
ticks = ''.join(f'<line x1="65" x2="635" y1="{255-n*4}" y2="{255-n*4}" stroke="#ddd"/><text x="15" y="{259-n*4}">{n}%</text>' for n in [-10,0,10,20,30,40,50])
sources = ''.join(f'<li><a href="{url}">{k} 日收盘历史</a></li>' for k,url in d['sources'].items())
out = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AMD 最近一周上涨原因｜2026-11-13</title>
<style>body{{font:17px/1.8 system-ui,sans-serif;color:#172b35;background:#f5f6f4;margin:0}}main{{max-width:980px;width:100%;box-sizing:border-box;margin:auto;padding:32px}}h1,h2{{line-height:1.4}}section{{background:white;padding:24px;margin:20px 0;border-radius:12px}}table{{border-collapse:collapse;table-layout:fixed;width:100%;font-variant-numeric:tabular-nums}}td,th{{padding:9px;overflow-wrap:anywhere;border-bottom:1px solid #ddd;text-align:right}}th:first-child{{text-align:left}}a{{color:#14665b;overflow-wrap:anywhere}}svg{{width:100%;height:auto}}.legend span{{margin-right:18px}}@media(max-width:600px){{main{{padding:12px}}section{{padding:15px}}body{{font-size:15px}}}}@media print{{body{{background:white}}main{{padding:0}}section{{break-inside:auto;padding:10px}}}}</style>
<main><h1>AMD 最近一周上涨原因</h1><p><strong>判断：暴跌后的修复叠加券商升级、EPYC 商业进展，以及 NVIDIA 风波中的替代受益预期。不是整个 AI 板块同步上涨，更没有证据把全部涨幅归因于某一条消息。</strong></p>
<p>整理：2026-11-13（北京时间）。行情截至美国 2026-11-12 常规交易收盘；不混入盘后价。范围仅为近期股价事件，非完整公司研究或当前估值报告。</p><nav><a href="#prices">涨幅</a> · <a href="#events">催化</a> · <a href="#limits">判断边界</a> · <a href="#checks">核验</a></nav>
<section id="prices"><h2>先确认涨了多少</h2><p>最近五个交易日为 11 月 6、9、10、11、12 日，以 11 月 5 日收盘为基期。下表单位：美元/股；收益为价格收益，不含分红。公式＝期末/期初−1。</p><table><tr><th>标的</th><th>11-05</th><th>11-12</th><th>区间涨跌</th></tr>{rows}</table>
<p>AMD 先在 11 月 5 日下跌 17.26%，再连续五日上涨；从下跌前 11 月 4 日的 488.78 美元算至最新，涨幅为 {(585.30/d['amd_nov4']-1)*100:.2f}%。低点起算的 44.73% 不能当作没有此前下跌的单向涨幅。</p>
<svg viewBox="0 0 680 340" role="img" aria-label="以11月5日为零点的累计价格涨跌：AMD显著跑赢SOXX、QQQ和NVDA"><title>累计价格变化（%，11月5日为基期；纵轴-10%至50%）</title>{ticks}{lines}{labels}</svg><div class="legend">{''.join(f'<span style="color:{c}">{k}</span>' for k,c in colors.items())}</div>
<table><tr><th>AMD 日期（2026）</th><th>收盘价</th><th>当日涨跌</th></tr>{daily}</table><p>来源为下方四份历史行情；AMD 11 月 12 日 585.30 美元另与公司 IR 行情交叉核对。</p></section>
<section id="events"><h2>已找到的催化</h2><p><strong>11 月 9 日：Oppenheimer 升级评级与 Google Cloud 合作。</strong>媒体报道 Rick Schafer 将评级由 Perform 升至 Outperform，目标价 600 美元；这是分析师判断，不是公司保证。AMD 当天公告 EPYC 为 Google TPU 8tx 提供主机 CPU。投资含义是客户使用自研 AI 加速器时，AMD 仍可从服务器 CPU 获得业务；没有披露此次新增收入金额，不能当作新的 GPU 大订单。AMD 当日收涨 13.26%。<a href="https://www.kiplinger.com/investing/stocks/dow-adds-1-104-points-even-as-nvidia-stock-sinks-stock-market-today">评级报道</a>；<a href="https://ir.amd.com/news-events/press-releases/detail/1304/amd-epyc-expands-its-leadership-at-the-foundation-of-ai">AMD 原公告</a>。</p>
<p><strong>11 月 10 日：第六代 EPYC 正式上市。</strong>公司披露 Zen 6/SP7 处理器已由主要服务器厂商出货，Azure、OCI 云实例将陆续提供。它加强 CPU 路线兑现证据，但不能直接证明整个 GPU 机柜交付完成，也不能把未量化的收入计入订单。<a href="https://ir.amd.com/news-events/press-releases/detail/1305/amd-showcases-6th-gen-amd-epyc-processors-to-lead-next-era-of-ai-and-enterprise-computing">AMD 原公告</a>。</p>
<p><strong>11 月 9—12 日：NVIDIA 治理及领导层事件引发竞争替代预期。</strong>11 月 12 日路透报道 NVIDIA 领导层变动，并将当时 AMD/Broadcom 逆势上涨与投资者预期竞争机会联系起来。此处为权威媒体转述；本轮未独立核验 NVIDIA 董事会文件，不延伸报道中的私人指控。AMD 同期上涨、NVDA 下跌与轮动叙事一致，但没有资金流或订单迁移证据，不能断言客户已转单。<a href="https://ca.marketscreener.com/news/global-ai-stocks-sink-as-nvidia-crisis-deepens-sector-selloff-ce785ed8dc80f526">路透报道及盘中时间边界</a>。</p>
<p><strong>板块反弹提供背景。</strong>同期 SOXX 涨 {returns['SOXX']:.2f}%、QQQ 涨 {returns['QQQ']:.2f}%，AMD 跑赢两者；这里的简单收益差不是统计归因，不能精确分拆各消息贡献多少涨幅。</p></section>
<section id="limits"><h2>对研究判断的影响</h2><p>【我的推演】本轮增强了“AMD 是 AI 基础设施第二供应来源，且 EPYC 可跨 GPU/自研 ASIC 平台受益”的叙事。它与此前 FPGA 工业周期无直接等价关系。股价重估不等于 CUDA 壁垒消失，也不等于 NVIDIA 的客户、软件和交付能力已经转移。</p><p>继续跟踪 EPYC/Instinct 的实际销售、Helios 验收和回款、营运资金及 FCF；本轮未重做最新 PE/EV，没有将历史市值与最新价格混用。未确认的空头回补、期权挤压及机构流入不列作事实原因。</p></section>
<section id="checks"><h2>核验与来源</h2><p>价格为手工摘录，保存于 <a href="factcheck/data/2026-11-13-week-prices.json">输入文件</a>，以 <a href="factcheck/build_week_review.py">生成/复算脚本</a>重算表格和图；涨幅、逐日基期及图表同源。判定：连续五日上涨与区间涨幅 ✅ 属实；消息贡献比例 ⚠ 无法量化。评级为媒体转述，产品/合作为公司披露，因果解释为推演。</p><ul>{sources}<li><a href="https://ir.amd.com/stock-data/stock-data">AMD IR 行情交叉核对</a></li></ul><p>HTML 尚未接入研究入口；原 research.yaml 仅指向停更的历史 Markdown，本次不改旧入口、不维护第二份正文。本 HTML 仅覆盖近期行情专题，完整公司研究此前缺口不因本轮完成而消失。</p><p id="visual-check">展示验收：Chrome 本地桌面图表及表格已检查；窄屏与打印已实际生成检查并调整。390像素无头截图存在视口裁切，另以500像素窄屏复核。外链内容在取证时核对，未模拟点击全部外链；本地输入与脚本路径存在。</p></section></main></html>'''
(base.parent/'近期股价催化.html').write_text(out)
