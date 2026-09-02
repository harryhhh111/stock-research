import pathlib

f = pathlib.Path('/Users/vinci/Documents/stock_research/ACN/埃森哲（ACN）分析报告.md')
lines = f.read_text().splitlines()

result = []
skip_until = None

for i, line in enumerate(lines):
    # Skip duplicate industry plain-text block (starts with tab-separated header)
    if line == '行业\tFY2023→FY2024\tFY2024→FY2025\t最新趋势（FY2026 Q3 TTM）\t解读':
        skip_until = '## 三、FY2026 季度进展（截至2026年5月31日）'
        continue
    if skip_until and line == skip_until:
        skip_until = None
        result.append(line)
        continue
    if skip_until:
        continue

    # Skip duplicate quarterly plain-text block
    if line == '季度\t咨询营收（TTM）\t管理服务营收（TTM）\t管理服务-咨询差距':
        skip_until = '## 四、其他值得关注的营收数据'
        continue
    if skip_until and line == skip_until:
        skip_until = None
        result.append(line)
        continue
    if skip_until:
        continue

    result.append(line)

text = '\n'.join(result)

# Fix $...$ to italic markdown
text = text.replace(' $Consulting$', ' *Consulting*')
text = text.replace(' $Managed Services$', ' *Managed Services*')
text = text.replace(' $Type of Work$', ' *Type of Work*')
text = text.replace(' $Service Groups$', ' *Service Groups*')
text = text.replace(' $Reinvention Services$', ' *Reinvention Services*')
text = text.replace(' $Service Group$', ' *Service Group*')
text = text.replace(' $Strategy \& Consulting$', ' *Strategy & Consulting*')
text = text.replace(' $Digital Core$', ' *Digital Core*')
text = text.replace(' $Industry and Enterprise$', ' *Industry and Enterprise*')
text = text.replace(' $客户增长$', ' *客户增长*')
text = text.replace(' $TTM$', ' *TTM*')
text = text.replace(' $亿美元$', ' *亿美元*')
text = text.replace(' $美元$', ' *美元*')
text = text.replace(' $本币$', ' *本币*')

# Fix escaped asterisks
text = text.replace('\\*\\*+4%\\*\\*', '**+4%**')
text = text.replace('\\*\\*+1%\\*\\*', '**+1%**')
text = text.replace('\\*\\*+8%\\*\\*', '**+8%**')
text = text.replace('\\*\\*+5%\\*\\*', '**+5%**')

# Fix *** to ---
text = text.replace('\n***\n', '\n---\n')

f.write_text(text)
print("Done")
