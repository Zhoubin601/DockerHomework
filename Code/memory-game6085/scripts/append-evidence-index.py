from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import subprocess,json,sys

file=Path(sys.argv[1]).resolve()
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(file) as z: xml=etree.fromstring(z.read('word/document.xml'))
tables=len(xml.findall('w:body/w:tbl',ns))
if tables!=6: raise SystemExit('Expected six original report tables; refusing to append duplicate index')
rows=[['图号','内容','来源文件'],['1','容器首页','04-container-home.png'],['2','环境与项目命名','01-environment.png'],['3','容器中保存成绩','05-container-completed.png'],['4','镜像构建成功','02-build.png'],['5','容器运行与健康检查','03b-container-run.png'],['6','本机仓库推送','05-registry-push.png'],['7','本地镜像移除','06-remove-local.png'],['8','从仓库重新拉取','07-registry-pull.png'],['9','重建前成绩','04-data-before.png'],['10','拉取镜像创建新容器','08-run-pulled-image.png'],['11','重建后榜单与数据卷','09-data-after.png']]
commands=[{'command':'add','parent':'/body','type':'paragraph','props':{'text':'9.1 截图来源索引','style':'Heading2','font':'黑体','size':'14pt','bold':'true','color':'000000','keepNext':'true','snapToGrid':'false','spaceBefore':'10pt','spaceAfter':'8pt'}},
 {'command':'add','parent':'/body','type':'table','props':{'rows':str(len(rows)),'cols':'3','width':'16.5cm','colWidths':'1.2cm,7cm,8.3cm','padding':'0.12cm','border.all':'single;4;D9D9D9','border.horizontal':'single;4;D9D9D9','border.vertical':'single;4;D9D9D9'}},
 {'command':'get','path':'/body/tbl[7]'}]
for ri,row in enumerate(rows,1):
 for ci,value in enumerate(row,1):
  commands.append({'command':'set','path':f'/body/tbl[7]/tr[{ri}]/tc[{ci}]','props':{'text':value,'font':'宋体','size':'9pt','valign':'center','align':'left','bold':str(ri==1).lower(),'fill':'E9EDEB' if ri==1 else 'FFFFFF','color':'000000','padding.top':'0.12cm','padding.bottom':'0.12cm','padding.left':'0.14cm','padding.right':'0.14cm'}})
commands.append({'command':'add','parent':'/body','type':'paragraph','props':{'text':'截图源文件统一位于 docs/docker-evidence/。终端图片采集自专用 Windows 控制台窗口，浏览器图片采集自实际运行的应用容器。完整实验标识、镜像摘要和成绩对比保存在同目录 results.json。','font':'宋体','size':'10pt','color':'000000','spaceBefore':'8pt','spaceAfter':'6pt','lineSpacing':'1.3x','snapToGrid':'false'}})
batch=file.parent/'evidence-index.json';batch.write_text(json.dumps(commands,ensure_ascii=False),encoding='utf-8')
subprocess.run(['officecli','batch',str(file),'--input',str(batch),'--stop-on-error'],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['officecli','save',str(file)],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['officecli','close',str(file)],check=True,stdout=subprocess.DEVNULL)
print('Added the evidence source index.')
