from pathlib import Path
import json, re, subprocess
import fitz
from PIL import Image, ImageDraw

W=Path(__file__).resolve().parent
pdf=fitz.open(W/'report-review.pdf')
native=json.loads((W/'word-native.json').read_text(encoding='utf-8-sig'))
clean=lambda s:re.sub(r'\s+','',s)
pages=[clean(p.get_text()) for p in pdf]
toc=[clean(s) for s in pdf[1].get_text().splitlines()]
headings=[]
for h in native['headings']:
    h['headingInRealPage']=clean(h['heading']) in pages[h['page']-1]
    h['tocPageMatches']=any(re.fullmatch(re.escape(clean(h['heading']))+r'[.·…]*'+str(h['page']),s) for s in toc)
    headings.append(h)
assert len(pdf)==31 and len(headings)==42
assert all(h['headingInRealPage'] and h['tocPageMatches'] for h in headings)
dest=W/'render'
dest.mkdir(exist_ok=True)
subprocess.run(['pdftoppm','-r','72','-png',str(W/'report-review.pdf'),str(dest/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
for first,last in [(1,16),(17,31)]:
    tw,th=310,455
    canvas=Image.new('RGB',(tw*4,th*4),'#dddddd')
    draw=ImageDraw.Draw(canvas)
    for i,number in enumerate(range(first,last+1)):
        im=Image.open(dest/f'page-{number:02d}.png')
        im.thumbnail((tw-12,th-24))
        x=(i%4)*tw+(tw-im.width)//2
        y=(i//4)*th+4
        canvas.paste(im,(x,y))
        draw.text(((i%4)*tw+10,(i//4)*th+th-17),str(number),fill='black')
    canvas.save(dest/f'contact-{first}-{last}.png')
result={'pages':len(pdf),'tables':native['tables'],'images':native['images'],'verifiedTocEntries':len(headings),'allHeadingAndTocPagesMatch':True,'headings':headings}
(W/'pagination-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('PDF pages=31; all 42 heading/TOC pages match; Poppler rendered 31 pages')
