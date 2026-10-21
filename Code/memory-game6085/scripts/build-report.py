"""Create an evidence-backed DOCX working report with OfficeCLI; never overwrite raw/ or output/."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / 'Code/memory-game6085'
WORK = ROOT / 'docs/report-work'
WORK.mkdir(parents=True, exist_ok=True)
FILE = ROOT / 'docs/20261021-docker-lab-report-draft-v1.docx'
CLI = 'officecli'
commands = []
paragraph_count = 0
table_count = 0
notes = []


def add(parent, element, **props):
    commands.append({'command': 'add', 'parent': parent, 'type': element, 'props': {k: str(v).lower() if isinstance(v, bool) else str(v) for k, v in props.items()}})


def paragraph(text='', style='Normal', **props):
    global paragraph_count
    paragraph_count += 1
    base = {'text': text, 'style': style, 'font': '宋体', 'size': '11pt', 'color': '000000', 'spaceAfter': '7pt', 'lineSpacing': '1.3x'}
    base.update(props)
    add('/body', 'paragraph', **base)
    notes.append(text)
    return f'/body/p[{paragraph_count}]'


def heading(text, level=1, new_page=False):
    return paragraph(text, f'Heading{level}', font='黑体', size='18pt' if level == 1 else '14pt', bold=True,
                     spaceBefore='12pt', spaceAfter='10pt', keepNext=True, pageBreakBefore=new_page)


def code(lines):
    for line in lines.splitlines():
        paragraph(line, size='9pt', font='Consolas', **{'font.ea': '宋体'}, spaceAfter='2pt', lineSpacing='1.15x', keepLines=True)


def picture(relative, caption, width=14.4):
    from PIL import Image
    path = ROOT / relative
    with Image.open(path) as img:
        height = width * img.height / img.width
    parent = paragraph('', align='center', spaceBefore='5pt', spaceAfter='3pt', keepNext=True)
    add(parent, 'picture', src=str(path), width=f'{width}cm', height=f'{height:.3f}cm', alt=caption)
    paragraph(caption, size='9pt', align='center', spaceAfter='10pt')


def table(headers, rows, widths):
    global table_count
    table_count += 1
    path = f'/body/tbl[{table_count}]'
    add('/body', 'table', rows=len(rows) + 1, cols=len(headers), width='16.5cm', colWidths=','.join(f'{x}cm' for x in widths),
        **{'border.all': 'single;4;D9D9D9', 'border.horizontal': 'single;4;D9D9D9', 'border.vertical': 'single;4;D9D9D9'}, padding='0.14cm')
    commands.append({'command': 'get', 'path': path})
    for row_index, values in enumerate([headers, *rows], 1):
        for col_index, value in enumerate(values, 1):
            commands.append({'command': 'set', 'path': f'{path}/tr[{row_index}]/tc[{col_index}]', 'props': {
                'text': str(value), 'font': '宋体', 'size': '10pt', 'valign': 'center', 'align': 'left',
                'bold': str(row_index == 1).lower(), 'fill': 'E9EDEB' if row_index == 1 else ('FFFFFF' if row_index % 2 == 0 else 'F7F8F6'),
                'color': '000000', 'padding.top': '0.13cm', 'padding.bottom': '0.13cm',
                'padding.left': '0.16cm', 'padding.right': '0.16cm'}})
    notes.extend([' | '.join(map(str, headers)), *[' | '.join(map(str, row)) for row in rows]])


paragraph('Spring Boot 小游戏\vDocker 容器化实验报告', 'Title', font='黑体', size='29pt', bold=True, align='center', spaceBefore='24pt', spaceAfter='20pt', lineSpacing='1.25x')
paragraph('记忆花园 memory-game6085', size='17pt', align='center', spaceAfter='18pt')
paragraph('过程稿  大纲与实验截图待确认', size='12pt', bold=True, align='center', spaceAfter='18pt')
for text in ['课程：2026云计算技术与架构', '实验日期：2026年10月21日', '学号后四位：6085', '姓名、班级、完整学号：资料未提供']:
    paragraph(text, size='12pt', align='center', spaceAfter='8pt')
picture('output/20261021-memory-game6085-desktop-v1.png', '记忆花园本地运行页面  来源为本项目真实浏览器截图', width=9.4)
paragraph('本稿记录已完成的 Vue3、Spring Boot 与 SQLite 应用实现、本地运行和验证结果，并整理 Docker 构建、发布、拉取及数据卷实验的操作方案。目前 Docker Desktop 启动失败，容器构建、镜像推送与拉取尚未成功实测。相关章节明确保留未完成状态，本稿暂不作为完整作业提交版。', size='10.5pt')

paragraph('目录', 'Title', font='黑体', size='20pt', bold=True, pageBreakBefore=True, keepNext=True)
toc_parent = paragraph('', spaceAfter='10pt')
heading('一 实验目的与任务要求')
paragraph('本实验围绕 Spring Boot 项目的 Docker 容器化展开，目标是理解镜像、容器和持久化数据卷之间的关系，完成从项目构建、镜像发布到镜像拉取和运行验证的完整流程。')
paragraph('原始要求来自 raw/要求.png：在机器上部署 Docker 环境，将一个已有 Spring Boot 项目打包发布，项目名称末尾添加学号后四位；发布后演示拉取，并将全过程截图汇总到一个 Word 文件。')
paragraph('本项目按用户确认的方向开发记忆翻牌小游戏，命名为 memory-game6085。若老师限定必须采用此前课程项目，而不接受先开发再容器化的新项目，需要另行确认。')

heading('二 实验环境与项目结构', new_page=True)
table(['项目', '实际配置或版本'], [
    ['操作系统', 'Microsoft Windows 11 家庭版 中文版，64 位，10.0.26300'],
    ['Java', 'OpenJDK 21.0.11'], ['Node.js / npm', 'Node.js 24.14.1 / npm 11.11.0'],
    ['Maven', '3.9.16，使用本机已有 Wrapper 缓存'], ['前端', 'Vue 3.5.44、Vite 7.3.7，以 package-lock.json 为准'],
    ['后端与数据库', 'Spring Boot 4.1.1、SQLite JDBC 3.53.4.0'],
    ['Docker', '客户端 29.8.2；Linux 引擎启动失败，尚无 Server 成功连接记录'],
    ['项目目录', 'Code/memory-game6085/'], ['访问与数据', 'http://localhost:8080；data/garden.db']
], [3.3, 13.2])
paragraph('源码由 frontend、backend 和 scripts 构成。Dockerfile、compose.yaml 和 README.md 位于项目根目录。原始要求保留在 raw/，工作过程和验证结果记录在 docs/。')
heading('三 系统设计与持久化')
paragraph('浏览器页面由 Vue3 实现，Spring Boot 提供牌局、翻牌、暂停、成绩提交和排行榜接口。Vue 构建后的静态资源打入同一个可执行 JAR，部署时只需一个应用容器。SQLite 以数据库文件保存成绩，不需要独立数据库服务。')
paragraph('游戏提供轻松 6 对、标准 8 对和挑战 12 对卡牌。牌面随机顺序、配对判断、步数与计时均由后端处理，未翻开的答案不发给前端。运行中的牌局保存在内存，服务重启后不恢复；已提交成绩保存在 SQLite。')
paragraph('成绩表包含牌局唯一标识、昵称、难度、步数、用时和创建时间。相同牌局重复提交只保留一条记录。排行榜按难度分别查询，优先比较步数，步数相同时比较用时。容器方案将数据库目录 /app/data 挂载到命名数据卷 memory-game6085-data。')

heading('四 本地构建与功能验证', new_page=True)
heading('4.1 构建与启动', 2)
paragraph('以下命令在项目根目录执行。本地构建已成功；构建前应先停止占用目标 JAR 的应用进程。')
code('.\\scripts\\build.ps1\njava -jar backend/target/memory-game6085.jar\ncurl.exe http://localhost:8080/api/health')
paragraph('实际健康检查返回 status 为 UP，application 为 memory-game6085，database 为 SQLite。前端静态页面与 /api 接口由同一个 Spring Boot 实例提供。')
heading('4.2 验证结果', 2)
table(['验证内容', '结果与证据'], [
    ['前端构建', 'npm run build 成功，生成静态资源'],
    ['后端测试', '3 项通过，0 失败、0 错误；见 surefire-reports'],
    ['浏览器端到端测试', '3 项通过；覆盖完整游戏、昵称校验、保存和刷新榜单'],
    ['暂停与重新开始', '暂停不计时，保留已翻牌状态；重开前确认'],
    ['SQLite 服务重启', '重启前后同一难度排行榜的完整内容一致'],
    ['界面自动审核', '5 种尺寸无横向溢出，相关 axe 自动规则未检出违规'],
    ['Compose 配置', 'docker compose config --quiet 解析通过，不能据此认定容器启动成功']
], [4.2, 12.3])
paragraph('自动化测试使用独立 .qa/ 数据目录，避免测试昵称和成绩混入正式试玩实例。自动检查通过不等同于完整人工无障碍认证。')
paragraph('本节已有成功执行记录，但尚未采集真实终端窗口截图。正式提交前需补充构建成功、JAR 启动和健康检查的真实命令行画面。')
heading('4.3 本地首页', 2, new_page=True)
picture('output/20261021-memory-game6085-desktop-v1.png', '图1 本地首页  展示游戏难度 计时 步数与空排行榜')
paragraph('页面采用植物主题卡牌、森林绿与奶油白配色，支持桌面双栏和手机单栏布局。尚未提交成绩时，排行榜显示空状态，不预置虚构玩家。')
heading('4.4 游戏交互与成绩保存', 2, new_page=True)
picture('Code/memory-game6085/frontend/test-results/desktop-completed.png', '图2 完成配对并保存成绩  真实自动测试实例截图')
paragraph('图中昵称“测试花匠6085”及成绩来自真实自动测试运行，仅用于验证功能，不是学生姓名或指定的作业成绩。图中界面证明本地游戏与成绩保存流程可用，不能替代 Docker 容器访问截图。')

heading('五 Docker 镜像构建与运行方案', new_page=True)
paragraph('本节是已经编写并核对的部署方案，尚未在本机 Docker 引擎中成功执行。Dockerfile 采用三个阶段：Node 构建 Vue，Maven 构建 Spring Boot JAR，JRE 运行最终应用。运行阶段使用普通用户，数据库目录为 /app/data。')
heading('5.1 关键构建配置', 2)
code('FROM node:24-bookworm-slim AS frontend\nRUN npm ci --no-audit --no-fund\nRUN npm run build\nFROM maven:3.9.16-eclipse-temurin-21 AS backend\nCOPY --from=frontend /build/frontend/dist /build/frontend/dist\nRUN mvn -B -ntp package\nFROM eclipse-temurin:21-jre-jammy\nUSER garden\nENV DATA_DIR=/app/data PORT=8080\nEXPOSE 8080\nENTRYPOINT ["java", "-jar", "/app/app.jar"]')
paragraph('上述仅为分阶段流程摘录，省略了目录、源码复制、用户创建等命令，不能直接作为完整 Dockerfile 使用。实际可构建文件以 Code/memory-game6085/Dockerfile 为准，运行参数还包含 JVM 内存限制。')
heading('5.2 拟执行命令与证据', 2)
code('docker version\ndocker compose config --quiet\ndocker compose up -d --build\ndocker compose ps\ndocker compose logs --tail 40\ncurl.exe http://localhost:8080/api/health')
paragraph('需补充真实截图：Client 与 Server 同时正常的 docker version、镜像构建成功、容器运行列表、启动日志以及容器提供的健康检查和浏览器页面。目前仅配置解析通过，不能写为“容器已部署成功”。')
paragraph('启动容器前需停止本地占用 8080 的 JAR。Compose 将宿主机 127.0.0.1:8080 映射到容器 8080，并把 memory-game6085-data 数据卷挂载到 /app/data。')

heading('六 镜像发布与拉取方案', new_page=True)
paragraph('镜像仓库账户资料未提供，尚未执行本项目镜像的推送和拉取。下面以 Docker Hub 为示例，用户名应由实际操作者输入，不在报告中虚构账户或成功输出。')
code('$DockerHubUser = Read-Host "输入你的 Docker Hub 用户名"\ndocker login\ndocker tag memory-game6085:1.0.0 "${DockerHubUser}/memory-game6085:1.0.0"\ndocker push "${DockerHubUser}/memory-game6085:1.0.0"\ndocker pull "${DockerHubUser}/memory-game6085:1.0.0"\ndocker image ls')
paragraph('需补充推送成功及拉取成功的真实终端截图，并验证拉取后的镜像可以启动并访问。若本机已有镜像，拉取可能复用已有层；需如实描述，不能写为重新下载了所有镜像层。')
heading('七 数据持久化验证')
heading('7.1 已完成的本地服务重启验证', 2)
paragraph('在独立测试实例中完成游戏并提交成绩，读取轻松难度排行榜；停止该 Java 服务，再使用相同数据库目录启动，重新读取榜单。已对比重启前后的完整榜单内容，结果一致。这验证了 SQLite 成绩文件可以跨应用进程重启保留。')
heading('7.2 尚未完成的容器重建验证', 2)
paragraph('容器实验需先完成一局并截图保存后的榜单，再执行以下命令移除并重新创建本项目容器，最后刷新相同难度榜单，对比同一条成绩是否仍在。')
code('docker compose down\ndocker compose up -d\ndocker volume inspect memory-game6085-data')
paragraph('该演示应保留命名数据卷，不使用 docker compose down -v。当前尚未进行容器重建实验，因此不能将本地 Java 服务重启验证写成 Docker 数据卷实测通过。')

heading('八 实验结果与问题分析', new_page=True)
table(['环节', '当前结果'], [
    ['小游戏开发与本地运行', '已完成，已生成可执行 JAR 和真实页面截图'],
    ['SQLite 成绩持久化', '本地应用重启验证通过'],
    ['Dockerfile 与 Compose', '已编写，Compose 语法解析通过'],
    ['Docker 引擎与镜像构建', '未完成，本机 Docker Desktop 启动失败'],
    ['镜像发布与拉取', '未完成，尚无仓库账户及实际成功记录'],
    ['容器数据卷持久化', '已配置，尚未实测'],
    ['作业提交所需终端截图', '尚未采集完整，必须补齐后再形成提交版']
], [5.1, 11.4])
paragraph('本机 Docker Desktop 启动日志指向 Secrets Engine 的 engine.sock 重命名与系统访问错误，Linux 引擎未能提供连接。本轮未删除或改动用户 Docker 配置及相关文件，未把客户端可用误写为服务端可用。')
paragraph('后续应先排查 Docker 启动问题，取得 Client 与 Server 都正常的证据，再按镜像构建、容器访问、镜像推送、镜像拉取、容器重建的顺序补齐操作与截图。现阶段结论仅限于应用本地运行和 SQLite 持久化成功，完整 Docker 作业尚未完成。')
heading('九 参考资料与截图来源')
for text in [
    '原始要求：raw/要求.png；学号后四位、技术栈、Code 目录由用户于 2026年10月21日确认。',
    '项目证据：docs/ui-review.md、backend/target/surefire-reports/、frontend/test-results/ 和 ui-audit.json。',
    '图1：output/20261021-memory-game6085-desktop-v1.png；图2：frontend/test-results/desktop-completed.png。均为实际浏览器截图。',
    '以下官方资料查阅日期均为 2026年10月21日，使用范围为技术实现和部署说明。',
    'Vue 官方文档 https://vuejs.org/guide/essentials/reactivity-fundamentals.html',
    'Vite 官方文档 https://vite.dev/guide/',
    'Spring Boot 官方文档 https://docs.spring.io/spring-boot/maven-plugin/packaging.html',
    'SQLite JDBC 官方仓库 https://github.com/xerial/sqlite-jdbc',
    'Docker 官方文档 https://docs.docker.com/engine/storage/volumes/',
]: paragraph(text, size='9.5pt', spaceAfter='5pt')


def run(*args):
    result = subprocess.run([CLI, *map(str, args)], capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        print(result.stdout[-6000:]); print(result.stderr[-2000:]); raise SystemExit(result.returncode)
    return result.stdout


if FILE.exists(): raise SystemExit('Refusing to overwrite existing working report: ' + str(FILE))
run('create', FILE)
run('open', FILE)
setup = [
    {'command':'set','path':'/','props':{'pageWidth':'21cm','pageHeight':'29.7cm','marginTop':'2cm','marginBottom':'2cm','marginLeft':'2.2cm','marginRight':'2.2cm','marginHeader':'1cm','marginFooter':'1cm'}},
    {'command':'set','path':'/styles/Normal','props':{'font':'宋体','size':'11pt','color':'000000'}},
]
setup_file = WORK / 'setup.json'
setup_file.write_text(json.dumps(setup, ensure_ascii=False), encoding='utf-8')
run('batch', FILE, '--input', setup_file, '--stop-on-error')
run('get', FILE, '/')
batch_file = WORK / 'body.json'
batch_file.write_text(json.dumps(commands, ensure_ascii=False), encoding='utf-8')
result = run('batch', FILE, '--input', batch_file, '--stop-on-error')
(WORK/'authoring.log').write_text(result, encoding='utf-8')
run('add', FILE, toc_parent, '--type', 'toc', '--prop', 'levels=1-2', '--prop', 'hyperlinks=true', '--prop', 'pageNumbers=false')
run('add', FILE, '/', '--type', 'header', '--prop', 'text=2026云计算技术与架构  Docker实验过程稿', '--prop', 'font=宋体', '--prop', 'size=9pt')
run('add', FILE, '/', '--type', 'footer', '--prop', 'text=过程稿  6085  第 ', '--prop', 'field=page', '--prop', 'font=宋体', '--prop', 'size=9pt')
run('set', FILE, '/footer[1]/p[1]', '--prop', 'align=center')
run('save', FILE)
run('close', FILE)
(ROOT/'docs/report-draft.md').write_text('\n\n'.join(notes), encoding='utf-8')
print('Created', FILE)
print('Body paragraphs:', paragraph_count, 'tables:', table_count, 'batch commands:', len(commands))
