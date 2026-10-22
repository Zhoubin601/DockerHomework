"""Render the native Word inspection PDF and verify every TOC page."""
from pathlib import Path
import json
import re

import fitz
from PIL import Image, ImageDraw

work = Path(__file__).resolve().parent
pdf = fitz.open(work / 'native-final.pdf')
dest = work / 'render-final'
dest.mkdir(exist_ok=True)
for i, page in enumerate(pdf):
    page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).save(dest / f'page-{i+1}.png')
for start in range(0, len(pdf), 16):
    end = min(start + 16, len(pdf))
    tilew, tileh = 340, 505
    contact = Image.new('RGB', (tilew * 4, tileh * ((end - start + 3) // 4)), '#e5e5e5')
    draw = ImageDraw.Draw(contact)
    for offset, index in enumerate(range(start, end)):
        im = Image.open(dest / f'page-{index+1}.png')
        im.thumbnail((tilew - 14, tileh - 26))
        x = (offset % 4) * tilew + (tilew - im.width) // 2
        y = (offset // 4) * tileh + 8
        contact.paste(im, (x, y))
        draw.text(((offset % 4) * tilew + 12, (offset // 4) * tileh + tileh - 18), str(index + 1), fill='black')
    contact.save(dest / f'contact-{start+1}-{end}.png')

native = json.loads((work / 'word-native-check.json').read_text(encoding='utf-8-sig'))
clean = lambda t: re.sub(r'\s+', '', t)
pages = [clean(p.get_text()) for p in pdf]
checks = []
for heading in native['headings']:
    checks.append({**heading, 'pdfContainsHeading': clean(heading['heading']) in pages[heading['page'] - 1]})
assert len(checks) == 42 and all(h['pdfContainsHeading'] for h in checks)
toc_lines = [clean(t) for t in pdf[1].get_text().splitlines()]
for heading in checks:
    assert any(re.fullmatch(re.escape(clean(heading['heading'])) + r'[.·…]*' + str(heading['page']), line)
               for line in toc_lines), (heading, 'TOC mismatch')
assert all(len(p.get_text().strip()) > 25 for p in pdf), 'Blank or nearly blank page'
(work / 'native-pagination-verification.json').write_text(json.dumps({
    'pages': len(pdf), 'tocEntries': len(checks), 'allNativeHeadingPagesVerifiedInPDF': True,
    'allTOCPagesVerifiedInPDF': True, 'headings': checks}, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Rendered {len(pdf)} pages at 144 dpi; verified all {len(checks)} TOC entries.')
