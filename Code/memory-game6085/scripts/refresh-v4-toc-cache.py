"""Update v4 cached TOC pages from a verified render while retaining Word fields."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
import re
import sys
import fitz
from lxml import etree

ROOT=Path(__file__).resolve().parents[3]
WORK=ROOT/'docs/v4-report-work'
FILE=WORK/'20261021-docker-lab-report-v4.docx'
PDF=WORK/(sys.argv[1] if len(sys.argv)>1 else 'render-layout')/'20261021-docker-lab-report-v4.pdf'
entries=json.loads((WORK/'toc-headings.json').read_text())
normalize=lambda s:re.sub(r'\s+','',s)
pdf=fitz.open(PDF)
pages=[normalize(p.get_text()) for p in pdf]
for entry in entries:
    matches=[i+1 for i,text in enumerate(pages) if i>=2 and normalize(entry['heading']) in text]
    assert len(matches)==1,(entry['heading'],matches)
    entry['page']=matches[0]
with ZipFile(FILE) as z:contents={n:z.read(n) for n in z.namelist()}
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
root=etree.fromstring(contents['word/document.xml'])
for entry in entries:
    fields=root.xpath(f'.//w:fldSimple[contains(@w:instr,"PAGEREF {entry["bookmark"]} ")]',namespaces=ns)
    assert len(fields)==1,entry
    fields[0].find('.//w:t',ns).text=str(entry['page'])
contents['word/document.xml']=etree.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
app=etree.fromstring(contents['docProps/app.xml'])
for el in app:
    if etree.QName(el).localname=='Pages':el.text=str(len(pdf))
contents['docProps/app.xml']=etree.tostring(app,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(FILE,'w',ZIP_DEFLATED) as z:
    for name,data in contents.items():z.writestr(name,data)
(WORK/'toc-verified-pages.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
print('Updated',len(entries),'entries,',len(pdf),'pages')
