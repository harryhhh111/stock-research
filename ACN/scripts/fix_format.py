import pathlib

f = pathlib.Path('/Users/vinci/Documents/stock_research/ACN/埃森哲（ACN）分析报告.md')
t = f.read_text()

# 1. Remove duplicate industry plain-text block
start1 = "| **资源** | +2.10% | +4.80% | +3.40% | 稳定低速增长 |\n\n行业"
end1 = "稳定低速增长\n\n## 三、FY2026"
idx1 = t.find(start1)
if idx1 != -1:
    idx1_end = t.find(end1, idx1)
    if idx1_end != -1:
        t = t[:idx1] + "| **资源** | +2.10% | +4.80% | +3.40% | 稳定低速增长 |\n\n## 三、FY2026" + t[idx1_end + len(end1):]

# 2. Remove duplicate quarterly plain-text block
start2 = "| **FY2026 Q3**（2026/6/30） | 363.7亿 | 367.3亿 | **管理服务领先3.6亿** |\n\n季度"
end2 = "管理服务领先3.6亿\n\n## 四、其他值得关注的营收数据"
idx2 = t.find(start2)
if idx2 != -1:
    idx2_end = t.find(end2, idx2)
    if idx2_end != -1:
        t = t[:idx2] + "| **FY2026 Q3**（2026/6/30） | 363.7亿 | 367.3亿 | **管理服务领先3.6亿** |\n\n## 四、其他值得关注的营收数据" + t[idx2_end + len(end2):]

# 3. Replace $...$ with *...* (Lark export artifact)
# Use regex for this to be safe
import re

def replace_dollar(m):
    return ' *' + m.group(1) + '*'

t = re.sub(r' \$([^$]+)\$', replace_dollar, t)

# 4. Fix *** to ---
t = t.replace('\n***\n', '\n---\n')

# 5. Fix escaped asterisks
t = t.replace('\\*\\*+4%\\*\\*', '**+4%**')
t = t.replace('\\*\\*+1%\\*\\*', '**+1%**')
t = t.replace('\\*\\*+8%\\*\\*', '**+8%**')
t = t.replace('\\*\\*+5%\\*\\*', '**+5%**')

f.write_text(t)
print("Done - all formatting fixed")
