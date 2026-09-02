import pathlib

f = pathlib.Path('/Users/vinci/Documents/stock_research/ACN/埃森哲（ACN）分析报告.md')
lines = f.read_text().splitlines()

# Find the index of the first "# AI 对 Accenture 产生了怎么样的冲击" after the valuation section
# We need to remove the duplicate block from the first occurrence of this heading (at line ~227)
# to just before the second real occurrence (at line ~237)

# Let's find all occurrences of "# AI 对 Accenture 产生了怎么样的冲击"
indices = [i for i, line in enumerate(lines) if line == '# AI 对 Accenture 产生了怎么样的冲击']
print(f"Found {len(indices)} occurrences at lines: {[i+1 for i in indices]}")

if len(indices) >= 2:
    # Remove everything from the first duplicate occurrence to just before the second real one
    # The first occurrence at indices[0] is the start of the duplicate block
    # The second occurrence at indices[1] is the real heading we want to keep
    # We want to keep lines[indices[1]:]
    # But we need to be careful - let's remove from indices[0] to indices[1]-1
    
    # Actually, looking at the content:
    # Line 227 (idx 226): # AI 对 Accenture 产生了怎么样的 impact (duplicate heading start)
    # ... duplicate content ...
    # Line 237 (idx 236): # AI 对 Accenture 产生了怎么样的 impact (real heading)
    
    new_lines = lines[:indices[0]] + lines[indices[1]:]
    f.write_text('\n'.join(new_lines) + '\n')
    print(f"Removed {indices[1] - indices[0]} duplicate lines")
else:
    print("Not enough occurrences found")
