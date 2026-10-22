from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import json, hashlib, re, shutil

WORK=Path(__file__).resolve().parent
ROOT=WORK.parents[1]
SOURCE=ROOT/'output/v7/20261022-docker-lab-report-v7.docx'
DEST=WORK/'candidate-v8.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','w14':'http://schemas.microsoft.com/office/word/2010/wordml'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for folder in ('raw','output') for p in sorted((ROOT/folder).rglob('*')) if p.is_file()}
assert not DEST.exists()
(WORK/'baseline-sha256.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copyfile(SOURCE,WORK/'source-v7.docx')
assert sha(SOURCE)=='762780c6d3ed8001d6120b853f56fd619b3e1c12e400d95c36b1d37c8844fd7b'

with ZipFile(SOURCE) as z: root=E.fromstring(z.read('word/document.xml'))
text=lambda p:''.join(p.xpath('.//w:t/text()',namespaces=NS))
changes=[]
def set_text(p,new,group):
    old=text(p)
    if old==new:return
    assert not p.xpath('.//w:drawing|.//w:fldChar|.//w:instrText',namespaces=NS)
    nodes=p.xpath('.//w:t',namespaces=NS)
    assert nodes
    nodes[0].text=new
    nodes[0].set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    for node in nodes[1:]:node.text=''
    changes.append({'group':group,'paraId':p.get('{'+NS['w14']+'}paraId'),'before':old,'after':new})
def para(pid):
    found=root.xpath('./w:body/w:p[@w14:paraId="'+pid+'"]',namespaces=NS)
    assert len(found)==1,pid
    return found[0]
def repl(pid,old,new,group):
    p=para(pid)
    assert text(p).count(old)==1,(pid,old,text(p))
    set_text(p,text(p).replace(old,new),group)

repl('4295FB1E','inspect 确认标签不存在、镜像列表为空后，才从 Registry 执行 pull。','通过 inspect 确认两个本地标签均不存在，并检查筛选后的镜像列表中已无 memory-game6085，再从 Registry 拉取镜像。','1-2')
repl('4295FB1E','构建缓存及其他基础镜像未作为本地应用标签存在的依据。','拉取日志中部分镜像层显示 Already exists，说明这些层仍保留在本地；应用镜像的两个本地标签在拉取前均已删除。','1-2')
repl('598B4170','启动健康检查曾早于应用就绪，补充重试后通过；该次初始失败记录另行保存在过程文档中。','首次健康检查时应用尚未就绪，连接失败；加入重试后，健康接口返回 UP。','3')
set_text(para('733A6987'),'本次在隔离 Ubuntu 环境中安装 Docker Engine，完成了应用镜像的构建、发布和拉取。使用拉取的镜像重建容器并挂载同一数据卷后，完整排行榜与重建前一致，浏览器中仍能查看原成绩。','4')
set_text(para('57420516'),'第二至九章记录 2026 年 10 月 21 日在 Windows 上完成的实验。附录 A 记录 10 月 22 日在本机隔离 Ubuntu 环境中安装 Docker Engine 并部署应用的过程。两次实验使用不同的引擎和资源。','5')
set_text(para('755DB3F7'),'本实验将 Spring Boot 项目打包为镜像，推送到本机 Registry，并在删除本地应用镜像标签后重新拉取。使用拉取的镜像创建新容器后，页面和接口可正常访问。','6')
repl('2774A1C0','实验重建容器时继续挂载同一数据卷，以验证程序与数据的生命周期可以分离。','重建容器时继续挂载同一数据卷，检查已保存的成绩是否仍可读取。','7')
repl('3DD924A6','随后从容器复制 /app/app.jar，与配套 JAR 计算 SHA-256 并逐字节比较，结果一致。','随后将容器内的 /app/app.jar 复制出来，分别计算它和配套 JAR 的 SHA-256，并逐字节比较两个文件，两项检查结果均一致。','8')
repl('3F7729CC','外层把本机 127.0.0.1:18089 转发到该环境的 18085，浏览器通过此地址完成一局轻松模式并保存成绩。','将本机 127.0.0.1:18089 的访问请求转发到隔离环境的 18085 端口后，通过浏览器打开该地址，完成一局轻松难度游戏并保存成绩。','9')

tables=root.xpath('./w:body/w:tbl',namespaces=NS)
def cell_para(t,r,c):
    return tables[t-1].xpath('./w:tr',namespaces=NS)[r-1].xpath('./w:tc',namespaces=NS)[c-1].xpath('./w:p',namespaces=NS)[0]
set_text(cell_para(7,8,2),'使用源码包中的配套 JAR；容器内文件与配套 JAR 的 SHA-256 相同，逐字节比较也一致。','8')
set_text(cell_para(4,6,2),'完成牌局后可填写昵称并保存成绩，成绩会显示在对应难度的排行榜中。','10')
set_text(cell_para(4,5,2),'在 1440、768、375、812（横屏）及 320 px 宽度下均无横向溢出。','11')

caption_map={
'图5 应用容器运行状态 端口映射 健康检查与普通用户':'图5 应用容器运行状态、端口映射、健康检查与运行用户',
'图6 镜像实际推送成功与仓库标签查询':'图6 镜像推送成功与仓库标签查询',
'图7 移除实验容器和本地镜像 数据卷仍然保留':'图7 移除实验容器和本地镜像，数据卷仍然保留',
'图9 重建前的容器标识 成绩与数据卷':'图9 重建前的容器标识、成绩与数据卷',
'图11 重建后榜单一致 数据卷仍挂载到同一目录':'图11 重建后榜单一致，数据卷仍挂载到同一目录',
'A6 创建网络 数据卷和镜像仓库':'A6 创建网络、数据卷和镜像仓库',
}
for p in root.xpath('./w:body/w:p',namespaces=NS):
    old=text(p)
    if old in caption_map:set_text(p,caption_map[old],'12')
    elif re.match(r'^图A\d+',old) and ' 操作日志' in old:
        title,part=old.split(' 操作日志',1)
        title=title.replace('创建网络 数据卷','创建网络、数据卷')
        set_text(p,title+'（操作日志'+('，'+part if part else '')+'）','12')

with ZipFile(SOURCE) as zin, ZipFile(DEST,'w') as zout:
    for item in zin.infolist():
        data=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True) if item.filename=='word/document.xml' else zin.read(item.filename)
        zout.writestr(item,data)
with ZipFile(SOURCE) as a,ZipFile(DEST) as b:
    changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
assert changed==['word/document.xml'],changed
(WORK/'applied-changes.json').write_text(json.dumps({'source_sha256':sha(SOURCE),'changes':changes,'zip_parts_changed_before_word':changed},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'changes':len(changes),'candidate':str(DEST),'source_sha256':sha(SOURCE)},ensure_ascii=False))
