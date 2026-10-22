from pathlib import Path
import sys, json, re
import fitz
from PIL import Image, ImageDraw, ImageOps

work=Path(__file__).resolve().parent
pdf=fitz.open(work/(sys.argv[1] if len(sys.argv)>1 else 'native-pass1.pdf'))
dest=work/(sys.argv[2] if len(sys.argv)>2 else 'render-pass1')
dest.mkdir(exist_ok=True)
for i,page in enumerate(pdf):
    page.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(dest/f'page-{i+1}.png')
for start,end in [(0,16),(16,len(pdf))]:
    tilew,tileh=340,505
    contact=Image.new('RGB',(tilew*4,tileh*((end-start+3)//4)), '#e5e5e5')
    draw=ImageDraw.Draw(contact)
    for offset,index in enumerate(range(start,end)):
        im=Image.open(dest/f'page-{index+1}.png')
        im.thumbnail((tilew-14,tileh-26))
        x=(offset%4)*tilew+(tilew-im.width)//2
        y=(offset//4)*tileh+8
        contact.paste(im,(x,y))
        draw.text(((offset%4)*tilew+12,(offset//4)*tileh+tileh-18),str(index+1),fill='black')
    contact.save(dest/f'contact-{start+1}-{end}.png')
native=json.loads((work/'word-native-check.json').read_text(encoding='utf-8-sig'))
clean=lambda t:re.sub(r'\s+','',t)
pages=[clean(p.get_text()) for p in pdf]
checks=[]
for h in native['headings']:
    page=h['page']
    present=clean(h['heading']) in pages[page-1]
    checks.append({**h,'pdfContainsHeading':present})
assert len(checks)==42 and all(h['pdfContainsHeading'] for h in checks)
toc_lines=[clean(t) for t in pdf[1].get_text().splitlines()]
for h in checks:
    assert any(re.fullmatch(re.escape(clean(h['heading']))+r'[.·…]*'+str(h['page']),line) for line in toc_lines),(h,'TOC mismatch')
(work/'native-pagination-verification.json').write_text(json.dumps({'pages':len(pdf),'tocEntries':len(checks),'allNativeHeadingPagesVerifiedInPDF':True,'allTOCPagesVerifiedInPDF':True,'headings':checks},ensure_ascii=False,indent=2),encoding='utf-8')
print(dest,'Pages',len(pdf),'Verified TOC',len(checks))
