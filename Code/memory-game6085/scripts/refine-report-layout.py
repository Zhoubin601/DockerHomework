from pathlib import Path
from zipfile import ZipFile
import json,re,subprocess,sys
from lxml import etree

file=Path(sys.argv[1]).resolve()
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','w14':'http://schemas.microsoft.com/office/word/2010/wordml'}
commands=[]
with ZipFile(file) as z:
    xml=etree.fromstring(z.read('word/document.xml'))
for index,p in enumerate(xml.findall('w:body/w:p',ns),1):
    text=''.join(p.xpath('.//w:t/text()',namespaces=ns))
    para_id=p.get('{'+ns['w14']+'}paraId')
    if not para_id: continue
    path=f'/body/p[@paraId={para_id}]'
    if p.find('.//w:drawing',ns) is not None:
        commands.append({'command':'set','path':path,'props':{'lineSpacing':'1x','size':'1pt','spaceBefore':'3pt','spaceAfter':'1pt','keepNext':'true'}})
    elif len(text)>45 and not re.match(r'^图\d',text) and not p.xpath('.//w:rFonts[@w:ascii="Consolas"]',namespaces=ns):
        style=p.find('w:pPr/w:pStyle',ns)
        if style is None or style.get('{'+ns['w']+'}val')=='Normal':
            commands.append({'command':'set','path':path,'props':{'firstLineChars':'200'}})
batch=file.parent/'layout-refinement.json'
batch.write_text(json.dumps(commands,ensure_ascii=False),encoding='utf-8')
subprocess.run(['officecli','batch',str(file),'--input',str(batch),'--stop-on-error'],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['officecli','save',str(file)],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['officecli','close',str(file)],check=True,stdout=subprocess.DEVNULL)
print('Refined picture line boxes and prose indentation:',len(commands),'paragraphs')
