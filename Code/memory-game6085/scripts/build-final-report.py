"""Build the confirmed submission report from completed Docker evidence with OfficeCLI."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / 'Code/memory-game6085'
EVIDENCE = ROOT / 'docs/docker-evidence'
WORK = ROOT / 'docs/report-final-work'
WORK.mkdir(parents=True, exist_ok=True)
FILE = WORK / '20261021-docker-lab-report-v1.docx'
RESULT = json.loads((EVIDENCE/'results.json').read_text(encoding='utf-8'))
assert RESULT['leaderboardPreserved'] and RESULT['health']['status'] == 'UP'
SCORE = RESULT['leaderboard']['scores'][0]
commands, notes = [], []
paragraph_count = table_count = figure_count = 0


def add(parent, kind, **props):
    commands.append({'command':'add','parent':parent,'type':kind,'props':{k:str(v).lower() if isinstance(v,bool) else str(v) for k,v in props.items()}})


def p(text='', style='Normal', **props):
    global paragraph_count
    paragraph_count += 1
    values = dict(text=text,style=style,font='宋体',size='11pt',color='000000',spaceAfter='7pt',lineSpacing='1.3x',snapToGrid=False)
    values.update(props)
    add('/body','paragraph',**values)
    notes.append(text)
    return f'/body/p[{paragraph_count}]'


def h(text, level=1, page=False):
    return p(text,f'Heading{level}',font='黑体',size='18pt' if level==1 else '14pt',bold=True,spaceBefore='12pt',spaceAfter='10pt',keepNext=True,pageBreakBefore=page)


def code(text, size='8.5pt'):
    for line in text.splitlines():
        if line.strip(): p(line,font='Consolas',size=size,**{'font.ea':'宋体'},spaceAfter='2pt',lineSpacing='1.1x',keepLines=True)


def picture(name, caption, width=15.8):
    global figure_count
    from PIL import Image
    path = EVIDENCE/name
    assert path.is_file(), name
    with Image.open(path) as img: height=width*img.height/img.width
    parent=p('',align='center',size='1pt',lineSpacing='1x',spaceBefore='3pt',spaceAfter='1pt',keepNext=True)
    add(parent,'picture',src=str(path),width=f'{width}cm',height=f'{height:.3f}cm',alt=caption)
    figure_count += 1
    p(f'图{figure_count}  {caption}',size='9pt',align='center',spaceAfter='10pt')


def table(headers, rows, widths):
    global table_count
    table_count += 1
    path=f'/body/tbl[{table_count}]'
    add('/body','table',rows=len(rows)+1,cols=len(headers),width='16.5cm',colWidths=','.join(f'{x}cm' for x in widths),padding='0.14cm',
        **{'border.all':'single;4;D9D9D9','border.horizontal':'single;4;D9D9D9','border.vertical':'single;4;D9D9D9'})
    commands.append({'command':'get','path':path})
    for ri,row in enumerate([headers,*rows],1):
        for ci,value in enumerate(row,1):
            commands.append({'command':'set','path':f'{path}/tr[{ri}]/tc[{ci}]','props':dict(text=str(value),font='宋体',size='10pt',valign='center',align='left',
                bold=str(ri==1).lower(),fill='E9EDEB' if ri==1 else ('FFFFFF' if ri%2==0 else 'F7F8F6'),color='000000',
                **{'padding.top':'0.14cm','padding.bottom':'0.14cm','padding.left':'0.16cm','padding.right':'0.16cm'})})
    notes.extend([' | '.join(headers), *[' | '.join(map(str,row)) for row in rows]])


# Cover: all identity fields supplied and confirmed by the user.
p('Spring Boot 小游戏\vDocker 容器化实验报告','Title',font='黑体',size='28pt',bold=True,align='center',spaceBefore='20pt',spaceAfter='18pt',lineSpacing='1.25x')
p('记忆花园 memory-game6085',size='17pt',align='center',spaceAfter='18pt')
for item in ['课程：2026云计算技术与架构','姓名：周宇斌','班级：软件2401','学号：20246085','实验日期：2026年10月21日']:
    p(item,size='12pt',align='center',spaceAfter='7pt')
picture('04-container-home.png','记忆花园容器运行页面',width=9.4)
p('本实验将 Vue3、Spring Boot 与 SQLite 构成的记忆翻牌小游戏打包为 Docker 镜像，在本机私有 Registry 完成发布与重新拉取，并使用拉取的镜像创建新容器。新旧容器挂载同一命名数据卷，成绩记录保持一致。报告中的终端画面与游戏页面均来自实际运行。',size='10.5pt')

p('目录','Title',font='黑体',size='20pt',bold=True,pageBreakBefore=True,keepNext=True)
toc_anchor = h('一 实验目的与任务要求')
p('本实验的目的是掌握 Spring Boot 应用容器化的基本过程，理解 Docker 镜像、容器、镜像仓库和持久化数据卷的作用，并通过实际命令和访问结果验证部署流程。')
p('原始作业要求来自 raw/要求.png：在机器上部署 Docker 环境，将一个已有 Spring Boot 项目打包到 Docker 上发布，项目名称末尾加学号后四位；发布后演示拉取，所有过程截图放在一个 Word 文件中提交。')
table(['任务要求','本实验对应方式'],[
 ['项目名称包含学号后四位','memory-game6085，学号后四位为 6085'],
 ['Spring Boot 项目打包发布','三阶段 Dockerfile 构建，运行阶段提供页面和 API'],
 ['发布后演示拉取','发布到 localhost:5000；删除本地镜像后重新 pull'],
 ['全过程截图汇总','真实 Windows 终端截图、容器页面及持久化对比截图']
],[4.2,12.3])

h('二 实验环境与项目结构',page=True)
table(['项目','本次实际配置'],[
 ['操作系统','Windows 11 家庭版 中文版 64 位，10.0.26300'],
 ['本地开发工具','Java 21.0.11；Node.js 24.14.1；npm 11.11.0；Maven 3.9.16'],
 ['应用技术栈','Vue 3.5.44、Vite 7.3.7、Spring Boot 4.1.1、SQLite JDBC 3.53.4.0'],
 ['Docker 环境','Docker Desktop 4.95.0；Client / Server 29.8.2；Compose 5.6.0'],
 ['构建与运行镜像','Node 24；Maven 3.9.9 + Java 21；Temurin 21 JRE'],
 ['源码目录','Code/memory-game6085/'],
 ['应用端口','宿主机 127.0.0.1:18085 → 容器 8080'],
 ['镜像仓库','本机 Registry，127.0.0.1:5000'],
 ['持久化目录','memory-game6085-data → /app/data，数据库 garden.db']
],[3.4,13.1])
p('frontend 保存 Vue 页面和图案，backend 保存 Spring Boot 接口及数据库逻辑，scripts 保存本地构建与实验辅助脚本。Dockerfile 与 compose.yaml 位于项目根目录。8080 被已有课堂项目占用，因此本实验采用 18085 作为宿主机端口。')
picture('01-environment.png','Docker Client 与 Server 版本及项目名称检查',width=15.8)

h('三 系统设计与持久化',page=True)
h('3.1 应用结构',2)
p('浏览器通过 Vue3 页面操作游戏，Spring Boot 提供牌局、翻牌、暂停、成绩提交和排行榜接口。前端构建结果复制到后端静态资源目录，再打入可执行 JAR，因此一个应用容器即可同时提供页面和接口。')
p('游戏提供轻松 6 对、标准 8 对和挑战 12 对三种难度。后端随机生成卡牌顺序并判断配对，负责步数和计时。未翻开的答案不会直接传给浏览器；暂停时保留本局状态并停止计时，恢复后继续游戏。')
h('3.2 SQLite 数据设计',2)
table(['字段','用途'],[
 ['game_id','牌局唯一标识，防止同一局重复写入'],['nickname / difficulty','玩家昵称与难度，按难度分别查询排行榜'],
 ['moves / duration_ms','服务端生成的步数与用时，作为排序依据'],['created_at','成绩记录创建时间']
],[5.2,11.3])
p('运行中的牌局保存在服务端内存中；服务重启后需要重新开局。已提交成绩保存在 SQLite 数据库，排行榜按步数升序排列，步数相同再比较用时。持久化对象是已保存成绩，不包括未完成牌局。')
h('3.3 容器数据卷',2)
code('volumes:\n  - garden-data:/app/data\n# 命名数据卷的实际名称\nname: memory-game6085-data')
p('镜像保存应用程序，数据库由运行时生成并写入 /app/data。该目录挂载到命名数据卷后，删除应用容器不会自动删除成绩文件。实验重建容器时继续挂载同一数据卷，以验证程序与数据的生命周期可以分离。')

h('四 本地构建与功能验证',page=True)
h('4.1 本地构建与自动验证',2)
code('.\\scripts\\build.ps1\njava -jar backend/target/memory-game6085.jar')
p('本地构建已生成可执行 JAR。后端测试覆盖隐藏牌面、无效操作、暂停状态、服务端成绩统计和 SQLite 重新打开后的数据保留。浏览器测试覆盖完整配对、昵称校验、成绩提交、榜单刷新、窄屏布局以及接口失败后的重试。')
table(['检查项目','结果'],[
 ['npm run build','成功生成前端静态资源'],['后端测试','3 项通过，0 失败，0 错误'],['浏览器端到端测试','3 项全部通过'],
 ['界面检查','1440、768、375、812 横屏及 320 宽度无横向溢出'],['数据保存','完成牌局后可提交昵称并进入对应难度榜单']
],[5.1,11.4])
h('4.2 容器中的真实游戏操作',2)
p(f'在实际应用容器中通过浏览器完成轻松难度一局，保存昵称“{SCORE["nickname"]}”。本次演示记录为 {SCORE["moves"]} 步、{SCORE["durationMs"]/1000:.2f} 秒，记录编号 {SCORE["id"]}。这些数值来自服务端实际返回，仅用于展示成绩保存流程。')
picture('05-container-completed.png','容器中完成配对并保存演示成绩',width=14.0)

h('五 Docker 镜像构建与运行',page=True)
h('5.1 多阶段构建',2)
p('第一阶段使用 Node 构建 Vue，第二阶段使用 Maven 编译和打包 Spring Boot，第三阶段只复制 JAR 到 Java 运行环境。以下为实际 Dockerfile 的关键流程；完整文件位于项目根目录。')
code('FROM node:24-bookworm-slim AS frontend\nWORKDIR /build/frontend\nCOPY frontend/package*.json ./\nRUN npm ci --no-audit --no-fund\nCOPY frontend/ ./\nRUN npm run build\nFROM maven:3.9.9-eclipse-temurin-21 AS backend\nWORKDIR /build/backend\nCOPY backend/pom.xml ./\nRUN mvn -B -ntp dependency:go-offline\nCOPY backend/src ./src\nCOPY --from=frontend /build/frontend/dist /build/frontend/dist\nRUN mvn -B -ntp package\nFROM eclipse-temurin:21-jre-jammy\n# 创建普通用户与数据目录后复制 JAR\nCOPY --from=backend --chown=garden:garden /build/backend/target/memory-game6085.jar /app/app.jar\nUSER garden\nENV DATA_DIR=/app/data PORT=8080\nEXPOSE 8080\nENTRYPOINT ["java", "-XX:MaxRAMPercentage=70.0", "-jar", "/app/app.jar"]')
code('docker compose --progress plain build')
p('构建日志显示 Maven BUILD SUCCESS，最终镜像命名为 memory-game6085:1.0.0。Docker CLI 显示磁盘占用约 469 MB。首次基础镜像下载曾发生短读错误，完成基础镜像拉取后重新构建成功。')
picture('02-build.png','Spring Boot 打包成功并导出 Docker 镜像',width=14.0)
h('5.2 启动容器与接口检查',2,page=True)
code('docker compose up -d --no-build\ndocker compose ps\ncurl.exe -s http://localhost:18085/api/health\ndocker exec memory-game6085-garden-1 id')
p('应用容器运行后，18085 端口可访问游戏和 API。健康检查返回 status 为 UP，database 为 SQLite。容器内运行身份为 garden，UID 和 GID 均为 999，应用不使用 root 用户运行。')
picture('03b-container-run.png','应用容器运行状态 端口映射 健康检查与普通用户',width=16.4)
p('浏览器访问 http://localhost:18085 可进入游戏。该地址映射至应用容器的 8080，前端和后端同源访问，SQLite 无需额外数据库容器。')

h('六 镜像发布与拉取',page=True)
h('6.1 启动本机镜像仓库',2)
p('本实验使用已确认的本机私有 Registry，仓库端口绑定 127.0.0.1:5000，镜像数据保存在 memory-game6085-registry-data 数据卷。仓库用于本机课程实验。')
code('docker run -d --name memory-game6085-registry -p 127.0.0.1:5000:5000 -e OTEL_TRACES_EXPORTER=none --mount type=volume,source=memory-game6085-registry-data,target=/var/lib/registry registry:3')
h('6.2 标记与推送镜像',2)
code('docker tag memory-game6085:1.0.0 localhost:5000/memory-game6085:1.0.0\ndocker push localhost:5000/memory-game6085:1.0.0\ncurl.exe -s http://localhost:5000/v2/memory-game6085/tags/list')
p('推送日志显示镜像层 Pushed，仓库标签查询返回 1.0.0。发布路径为 localhost:5000/memory-game6085:1.0.0。')
picture('05-registry-push.png','镜像实际推送成功与仓库标签查询',width=16.4)
h('6.3 删除本地镜像后重新拉取',2,page=True)
p('为验证镜像来自仓库，先移除本实验应用容器，保留数据卷，并删除本地的两个实验镜像标签。镜像列表确认本地不存在 memory-game6085 后，再执行 pull。')
code('docker compose down\ndocker image rm localhost:5000/memory-game6085:1.0.0 memory-game6085:1.0.0\ndocker image ls\ndocker pull localhost:5000/memory-game6085:1.0.0')
picture('06-remove-local.png','移除实验容器和本地镜像 数据卷仍然保留',width=14.7)
picture('07-registry-pull.png','从 Registry 重新拉取成功',width=14.7)
p('拉取结果为 Downloaded newer image。推送与拉取的摘要一致，说明使用的是已发布的同一版本镜像。摘要记录如下：',size='10pt')
code(RESULT['digest'],size='8pt')

h('七 容器重建与持久化验证',page=True)
h('7.1 记录重建前的数据',2)
p('原容器中已保存轻松难度演示成绩。实验记录了原容器标识和完整排行榜响应；移除容器时未使用删除数据卷的参数。')
picture('04-data-before.png','重建前的容器标识 成绩与数据卷',width=16.0)
table(['对比项','重建前的实际值'],[
 ['容器标识前 12 位',RESULT['beforeContainerId'][:12]],['成绩编号 / 昵称',f'{SCORE["id"]} / {SCORE["nickname"]}'],
 ['步数 / 用时',f'{SCORE["moves"]} / {SCORE["durationMs"]} ms'],['数据卷',RESULT['volume']]
],[5.2,11.3])
h('7.2 使用拉取镜像创建新容器',2,page=True)
code('docker run -d --name memory-game6085-pulled -p 127.0.0.1:18085:8080 -e DATA_DIR=/app/data --mount type=volume,source=memory-game6085-data,target=/app/data localhost:5000/memory-game6085:1.0.0')
p(f'新容器标识前 12 位为 {RESULT["afterContainerId"][:12]}，与原容器不同。新容器直接使用拉取的仓库镜像，并继续挂载 memory-game6085-data 到 /app/data。')
picture('08-run-pulled-image.png','使用拉取镜像创建新容器并确认容器标识',width=16.0)
h('7.3 对比重建后的成绩',2,page=True)
p(f'新容器启动后，成绩编号、昵称、难度、步数、用时和创建时间均与重建前一致。程序对重建前后的完整排行榜 JSON 比较，结果为 LeaderboardPreserved=True。记录仍为 {SCORE["nickname"]}、{SCORE["moves"]} 步、{SCORE["durationMs"]} ms。')
picture('09-data-after.png','重建后榜单一致 数据卷仍挂载到同一目录',width=16.0)

h('八 实验结果与问题分析',page=True)
table(['实验环节','实际结果'],[
 ['Docker 环境','Client / Server 正常，Linux 引擎可用'],['应用与镜像构建','前端构建、后端测试和 Spring Boot JAR 打包成功'],
 ['容器运行','页面和 API 可访问，健康检查 UP'],['镜像发布','本机 Registry push 成功，可查询标签 1.0.0'],
 ['镜像拉取','删除本地镜像后 pull 成功，摘要与推送一致'],['容器重建','新容器使用拉取镜像，容器标识与原容器不同'],
 ['SQLite 数据卷','完整榜单对比一致，保存成绩保留'],['实验截图','真实终端窗口与容器浏览器页面均已采集']
],[4.5,12.0])
h('8.1 启动与端口问题',2)
p('Docker Desktop 最初因遗留 socket 无法访问而退出。原运行时目录改名被 Windows 拒绝，最终通过仅为 Docker Desktop 子进程设置独立运行时缓存目录恢复启动，系统级环境变量未修改。恢复后以 Client 与 Server 响应以及实际容器结果验证环境可用。')
p('首次构建遇到基础镜像下载中断；重新拉取所需基础镜像后完成构建。现有课堂项目占用 8080，因此将本实验宿主机端口调整为 18085，同时保留容器内部端口 8080。')
h('8.2 实验总结',2)
p('本实验完成了应用打包、镜像构建、容器访问、镜像发布与拉取，以及数据卷跨容器保留的完整验证。镜像用于分发应用程序，容器是运行实例，Registry 用于保存和分发镜像，数据卷用于保存独立于容器生命周期的数据库文件。')
p('重建前后容器标识发生变化，但保存的成绩没有变化，说明 SQLite 文件与应用容器已经通过命名数据卷实现生命周期分离。后续复现实验时，应保持仓库地址、镜像版本、应用端口和数据卷名称一致。')

h('九 参考资料与证据来源',page=True)
for item in [
 '原始作业要求：raw/要求.png；身份信息、技术栈和本机 Registry 方式由用户确认。',
 '项目源代码：Code/memory-game6085/；实验结果：docs/docker-evidence/results.json；各图来自同目录的真实终端和浏览器截图。',
 '技术资料查阅日期：2026年10月21日。',
 'Vue 官方文档：https://vuejs.org/guide/essentials/reactivity-fundamentals.html',
 'Vite 官方文档：https://vite.dev/guide/',
 'Spring Boot 官方文档：https://docs.spring.io/spring-boot/maven-plugin/packaging.html',
 'SQLite JDBC 官方仓库：https://github.com/xerial/sqlite-jdbc',
 'Docker 数据卷官方文档：https://docs.docker.com/engine/storage/volumes/',
 'CNCF Distribution 官方部署文档：https://distribution.github.io/distribution/about/deploying/'
]: p(item,size='9.5pt',spaceAfter='5pt')

h('9.1 截图来源索引',2)
table(['图号','内容','来源文件'],[
 ['1','容器首页','04-container-home.png'],['2','环境与项目命名','01-environment.png'],
 ['3','容器中完成游戏并保存成绩','05-container-completed.png'],['4','镜像构建成功','02-build.png'],
 ['5','容器运行与健康检查','03b-container-run.png'],['6','本机仓库推送','05-registry-push.png'],
 ['7','本地镜像移除','06-remove-local.png'],['8','从仓库重新拉取','07-registry-pull.png'],
 ['9','重建前成绩','04-data-before.png'],['10','拉取镜像创建新容器','08-run-pulled-image.png'],
 ['11','重建后榜单与数据卷','09-data-after.png']
],[1.2,7.0,8.3])
p('截图源文件统一位于 docs/docker-evidence/。终端图片采集自专用 Windows 控制台窗口，浏览器图片采集自实际运行的应用容器。完整实验标识、镜像摘要和成绩对比保存在同目录 results.json。',size='10pt')


def run(*args):
    result=subprocess.run(['officecli',*map(str,args)],capture_output=True,text=True,encoding='utf-8')
    if result.returncode:
        print(result.stdout[-6000:]); print(result.stderr[-2000:]); raise SystemExit(result.returncode)
    return result.stdout


if FILE.exists(): raise SystemExit('Refusing to overwrite an existing report build: '+str(FILE))
run('create',FILE); run('open',FILE)
setup=[{'command':'set','path':'/','props':dict(pageWidth='21cm',pageHeight='29.7cm',marginTop='2cm',marginBottom='2cm',marginLeft='2.2cm',marginRight='2.2cm',marginHeader='1cm',marginFooter='1cm')},
       {'command':'set','path':'/styles/Normal','props':dict(font='宋体',size='11pt',color='000000')}]
setup_path=WORK/'setup.json'; setup_path.write_text(json.dumps(setup,ensure_ascii=False),encoding='utf-8')
run('batch',FILE,'--input',setup_path,'--stop-on-error'); run('get',FILE,'/')
body_path=WORK/'body.json'; body_path.write_text(json.dumps(commands,ensure_ascii=False),encoding='utf-8')
(WORK/'authoring.log').write_text(run('batch',FILE,'--input',body_path,'--stop-on-error'),encoding='utf-8')
run('add',FILE,'/body','--type','toc','--before',toc_anchor,'--prop','levels=1-2','--prop','hyperlinks=true')
run('set',FILE,'/settings','--prop','updateFields=true')
run('add',FILE,'/','--type','header','--prop','text=2026云计算技术与架构  Docker实验报告','--prop','font=宋体','--prop','size=9pt')
run('add',FILE,'/','--type','footer','--prop','text=周宇斌  20246085  第 ','--prop','field=page','--prop','font=宋体','--prop','size=9pt')
run('set',FILE,'/footer[1]/p[1]','--prop','align=center')
run('save',FILE); run('close',FILE)
(ROOT/'docs/report-final-content.md').write_text('\n\n'.join(notes),encoding='utf-8')
print('Created',FILE,'with',figure_count,'figures,',table_count,'tables and',paragraph_count,'body paragraphs.')
