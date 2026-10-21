from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import json,subprocess,sys

file=Path(sys.argv[1]).resolve()
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing','w14':'http://schemas.microsoft.com/office/word/2010/wordml'}
with ZipFile(file) as z: xml=etree.fromstring(z.read('word/document.xml'))
commands=[]
for index,p in enumerate(xml.findall('w:body/w:p',ns),1):
    para_id=p.get('{'+ns['w14']+'}paraId')
    if not para_id: continue
    path=f'/body/p[@paraId={para_id}]'
    props={'snapToGrid':'false','firstLineChars':'0'}
    text=''.join(p.xpath('.//w:t/text()',namespaces=ns))
    style=p.find('w:pPr/w:pStyle',ns)
    is_normal=style is None or style.get('{'+ns['w']+'}val')=='Normal'
    if is_normal and len(text)>45 and not text.startswith('图') and not p.xpath('.//w:rFonts[@w:ascii="Consolas"]',namespaces=ns): props['firstLineChars']='200'
    if text=='7.3 对比重建后的成绩': props['pageBreakBefore']='true'
    if text=='九 参考资料与证据来源': props['pageBreakBefore']='true'
    if p.find('.//w:drawing',ns) is not None:
        props.update({'lineSpacing':'1x','size':'1pt','spaceBefore':'3pt','spaceAfter':'1pt','keepNext':'true','firstLineChars':'0'})
    commands.append({'command':'set','path':path,'props':props})
    desc=p.xpath('.//wp:docPr/@descr',namespaces=ns)
    if desc and desc[0]=='Spring Boot 打包成功并导出 Docker 镜像':
        for run_index,run in enumerate(p.findall('w:r',ns),1):
            if run.find('.//w:drawing',ns) is not None:
                commands.append({'command':'set','path':path+f'/r[{run_index}]','props':{'width':'14cm','height':'8.867cm'}})
    if desc and desc[0]=='容器中完成配对并保存演示成绩':
        for run_index,run in enumerate(p.findall('w:r',ns),1):
            if run.find('.//w:drawing',ns) is not None:
                commands.append({'command':'set','path':path+f'/r[{run_index}]','props':{'width':'14cm','height':'10.694cm'}})
batch=file.parent/'grid-fix.json'; batch.write_text(json.dumps(commands,ensure_ascii=False),encoding='utf-8')
subprocess.run(['officecli','batch',str(file),'--input',str(batch),'--stop-on-error'],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['officecli','save',str(file)],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['officecli','close',str(file)],check=True,stdout=subprocess.DEVNULL)
print('Disabled document-grid snapping for body paragraphs and refined figure pagination.')
