"""从已保存的PDF提取带物理页码的文本。依赖PyMuPDF；不覆盖PDF原件。"""
from pathlib import Path
import pymupdf
P = Path(__file__).resolve().parent/'data'
for f in P.glob('*.pdf'):
    with pymupdf.open(f) as doc:
        f.with_suffix('.txt').write_text('\n'.join(
            '\n=== PDF PAGE %d ===\n%s'%(i+1,page.get_text(sort=True))
            for i,page in enumerate(doc)))
