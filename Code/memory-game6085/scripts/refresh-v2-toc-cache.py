"""Refresh cached TOC page references from the verified render without Office automation."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
import re
import fitz
from lxml import etree

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / 'docs/v2-report-work'
FILE = WORK / '20261021-docker-lab-report-v2.docx'
PDF = WORK / 'render-layout-check/20261021-docker-lab-report-v2.pdf'
entries = json.loads((WORK / 'toc-headings.json').read_text(encoding='utf8'))
normalize = lambda s: re.sub(r'\s+', '', s)
pdf = fitz.open(PDF)
pages = [normalize(p.get_text()) for p in pdf]
for entry in entries:
    matches = [i + 1 for i, text in enumerate(pages) if i >= 2 and normalize(entry['heading']) in text]
    assert len(matches) == 1, (entry['heading'], matches)
    entry['page'] = matches[0]
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(FILE) as z:
    contents = {n: z.read(n) for n in z.namelist()}
root = etree.fromstring(contents['word/document.xml'])
for entry in entries:
    fields = root.xpath(f'.//w:fldSimple[contains(@w:instr,"PAGEREF {entry["bookmark"]} ")]', namespaces=ns)
    assert len(fields) == 1, entry
    fields[0].find('.//w:t', ns).text = str(entry['page'])
contents['word/document.xml'] = etree.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)
app = etree.fromstring(contents['docProps/app.xml'])
for el in app:
    if etree.QName(el).localname == 'Pages': el.text = str(len(pdf))
contents['docProps/app.xml'] = etree.tostring(app, encoding='UTF-8', xml_declaration=True, standalone=True)
with ZipFile(FILE, 'w', ZIP_DEFLATED) as z:
    for name, data in contents.items(): z.writestr(name, data)
(WORK/'toc-verified-pages.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf8')
print('Refreshed', len(entries), 'TOC entries across', len(pdf), 'pages')
