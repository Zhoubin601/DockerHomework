from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json,shutil
WORK=Path(__file__).resolve().parent
archive=WORK/'qa-iteration-1'
archive.mkdir(exist_ok=False)
for name in ['candidate-v8.docx','word-final.docx','native-final.pdf','word-native-check.json','final-checks.json','final-text.txt','pdf-text.txt','render-final']:
    shutil.move(str(WORK/name),str(archive/name))
src=archive/'candidate-v8.docx';dest=WORK/'candidate-v8.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(src) as z:root=E.fromstring(z.read('word/document.xml'))
drawings=root.xpath('.//w:drawing',namespaces=ns)
changes=[]
for index in (20,21):
    for extent in drawings[index].xpath('.//wp:extent|.//a:xfrm/a:ext',namespaces=ns):
        old={key:extent.get(key) for key in ('cx','cy')}
        for key in old:extent.set(key,str(round(int(old[key])*0.92)))
        changes.append({'image_index':index+1,'before':old,'after':dict(extent.attrib)})
with ZipFile(src) as zin,ZipFile(dest,'w') as zout:
    for item in zin.infolist():zout.writestr(item,E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True) if item.filename=='word/document.xml' else zin.read(item.filename))
(WORK/'layout-refinement.json').write_text(json.dumps({'reason':'Keep both A7 log figures on the same page after prose edit','scale':0.92,'changes':changes},indent=2),encoding='utf-8')
print('A7 figures scaled proportionally to 92%; previous QA retained.')
