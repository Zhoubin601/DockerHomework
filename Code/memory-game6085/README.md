# 记忆花园 · memory-game6085

一个可以放松片刻的植物主题记忆翻牌小游戏，也是用于云计算 Docker 作业的 Spring Boot 项目。

技术栈：Vue3 + Vite + Spring Boot + SQLite + Java 21。项目名以学号后四位 `6085` 结尾。

## v4 交付与实验版本

`v4` 是本次报告与交付资料的修订版本号，本次没有重新执行 Docker 实验。配套 JAR 沿用 v2 已验证、并在 v3 Linux 实验中实际使用的干净构建，应用源码和功能未变；预构建镜像直接复制这个交付 JAR。桌面和手机预览沿用 v3 截图原始字节，UI 未改，也没有重新采集。JAR 的 SHA-256 为：

```text
2e97ff46f2acfc1bfe0411a22f3f61a3ef4b8958e4ba5fff609d0350853852a0
```

报告区分两次于 2026-10-21 完成的真实实验，镜像标签不随交付资料版本变更：

| 实验 | 镜像版本 | 本机仓库 | 应用端口 |
| --- | --- | --- | --- |
| 原 Windows 实验 | `memory-game6085:1.0.0` | `localhost:5000` | `18085` |
| v3 Linux 补充实验 | `memory-game6085:1.0.1-v3` | `localhost:15085` | `18086` |

原 Windows 实验使用此前已安装的 Docker Desktop；v3 Linux 补充实验使用云工作区已经部署的 Docker Engine，记录该轮实际环境准备、镜像打包和运行操作。v4 报告将 Linux 资源实际创建截图与随后配置验证截图分别列为图 A1a、A1b，保留其他实验截图及日志。Linux 截图不能说明原 Windows 安装过程。两套仓库都仅用于各自本机实验，不能作为其他机器直接拉取镜像的地址；本项目没有提供公开镜像仓库。

源码包内的可执行文件位于 `dist-artifacts/memory-game6085.jar`。解压后可用 Java 21 直接运行：

```text
java -jar dist-artifacts/memory-game6085.jar
```

重新从源码构建的方法见下文；本地构建结果仍输出到 `backend/target/`。完整的多阶段构建 `Dockerfile` 和复制交付 JAR 的 `Dockerfile.prebuilt` 同时保留。

## 游戏功能

- 轻松（6 对）、标准（8 对）、挑战（12 对）三种难度。
- 服务端随机生成牌局、判断配对、统计步数和时间；未翻开的牌面不会发给浏览器。
- 暂停 / 继续、重新开局确认、可选音效、键盘翻牌。
- 完成后提交 1–16 字昵称，SQLite 保存成绩；相同牌局重复提交只保存一条。
- 排行榜按难度区分，先比步数，再比用时，展示前 10 名；不预置虚构玩家。
- 桌面、平板和手机布局，原生对话框、焦点提示、减少动态效果。

正在进行的牌局存在服务端内存，最多保留两小时。刷新页面需重新开局，重启服务也会清空未完成牌局；**已经提交的成绩保存在数据库中**。不含账号系统，排行榜是所有玩家共享榜单。

## 项目结构

```text
memory-game6085/
├─ frontend/             Vue3 + Vite 页面、图案和浏览器测试
├─ backend/              Spring Boot API、SQLite 和后端测试
├─ scripts/build.ps1     Windows 本地干净构建脚本
├─ scripts/start-docker-runtime.ps1  原实验机器的 Docker 启动排障脚本
├─ scripts/package-prebuilt.ps1     从源码干净构建并更新交付 JAR
├─ Dockerfile            多阶段构建：前端 → JAR → JRE
├─ Dockerfile.prebuilt   将已验证 JAR 打包到 JRE 镜像
├─ dist-artifacts/       可执行 JAR 与 SHA-256 清单
├─ compose.yaml          单容器部署和持久化数据卷
└─ README.md
```

## 本地运行

需要 Java 21、Node.js 22.12+ 或 24，以及 Maven 3.9+。无需另行安装 SQLite 服务。

在本项目根目录打开 PowerShell：

重新构建前，先停止正在运行的本项目 JAR。Windows 下运行中的 JAR 可能被占用，导致重新打包无法重命名文件。

```powershell
.\scripts\build.ps1
java -jar backend/target/memory-game6085.jar
```

构建脚本先构建前端，再执行 Maven `clean package`，避免旧的前端资源残留在 JAR 中。脚本会使用 PATH 中的 Maven，或已有 Maven Wrapper 缓存。找不到时可以指定：

```powershell
.\scripts\build.ps1 -Maven 'C:\你的Maven目录\bin\mvn.cmd'
```

浏览器打开 http://localhost:8080 。默认数据库位于**启动命令的当前目录**下 `data/garden.db`；保持在项目根目录启动，或显式指定 `DATA_DIR`，避免误以为数据丢失。

```powershell
$env:DATA_DIR = Join-Path $PWD 'data'
java -jar backend/target/memory-game6085.jar
```

开发时可分别启动两个终端：

```powershell
# 终端一：项目根目录，已有构建产物时
java -jar backend/target/memory-game6085.jar

# 终端二：项目根目录
cd frontend
npm ci
npm run dev
```

开发页面为 http://localhost:5173 ，`/api` 自动代理到 8080。Java 代码修改后需要重新构建 / 重启后端。

## Docker 构建和启动

先启动 Docker Desktop，使用 Linux 容器。在本项目根目录执行：

```powershell
docker version
docker compose up -d --build
docker compose ps
docker compose logs --tail 40
curl.exe http://localhost:18085/api/health
```

容器页面打开 http://localhost:18085 。宿主机端口默认为 18085，容器内部仍为 8080；可以通过 `GARDEN_PORT` 更改宿主机端口。本机已有课堂项目使用 8080，因此实验采用了这个映射。

Compose 将 `memory-game6085-data` 命名数据卷挂载到 `/app/data`；数据库为 `/app/data/garden.db`。数据库不打包进镜像。容器以普通用户运行，端口只绑定本机。

第一次构建会下载 Node、Maven、JRE 基础镜像，以及 npm / Maven 依赖，需要网络。后续构建可复用缓存。

### v3 预构建 JAR 镜像

在项目根目录使用下列 Linux 命令打包交付 JAR。它不在镜像中重新执行 Maven；所复制的文件就是 `dist-artifacts/` 下经校验的 JAR。

```sh
sha256sum -c dist-artifacts/SHA256SUMS
docker build -f Dockerfile.prebuilt -t memory-game6085:1.0.1-v3 .
docker volume create memory-game6085-v3-data
docker run -d --name memory-game6085-v3-app -p 127.0.0.1:18086:8080 \
  -e DATA_DIR=/app/data \
  --mount type=volume,source=memory-game6085-v3-data,target=/app/data \
  memory-game6085:1.0.1-v3
curl -fsS http://127.0.0.1:18086/api/health
```

`Dockerfile.prebuilt` 使用普通用户 `garden`，容器端口仍为8080；本机18086用于与原实验端口区分。重新执行前，先检查同名的本项目容器和端口占用，避免覆盖既有实验。

若在 Windows 上修改了应用源码，可执行 `.\scripts\package-prebuilt.ps1` 重新构建并复制 JAR。该脚本显示新文件的 SHA-256，并同步更新 `dist-artifacts/SHA256SUMS`，随后应构建新的镜像标签。若需从源码直接构建镜像，继续使用标准 `Dockerfile` 或 Compose。

### v3 Linux 镜像发布与拉取

下列命令使用独立的 v3 仓库、容器和数据卷，保留原实验资源。删除操作仅针对上一节创建的 v3 应用容器及两个 v3 镜像标签，数据卷继续保留。

```sh
docker volume create memory-game6085-v3-registry-data
docker run -d --name memory-game6085-v3-registry -p 127.0.0.1:15085:5000 \
  -e OTEL_TRACES_EXPORTER=none \
  --mount type=volume,source=memory-game6085-v3-registry-data,target=/var/lib/registry \
  registry:3
docker tag memory-game6085:1.0.1-v3 localhost:15085/memory-game6085:1.0.1-v3
docker push localhost:15085/memory-game6085:1.0.1-v3
curl -fsS http://127.0.0.1:15085/v2/memory-game6085/tags/list
docker rm -f memory-game6085-v3-app
docker image rm localhost:15085/memory-game6085:1.0.1-v3 memory-game6085:1.0.1-v3
docker image ls --filter reference='*memory-game6085*1.0.1-v3'
docker pull localhost:15085/memory-game6085:1.0.1-v3
docker run -d --name memory-game6085-v3-pulled -p 127.0.0.1:18086:8080 \
  -e DATA_DIR=/app/data \
  --mount type=volume,source=memory-game6085-v3-data,target=/app/data \
  localhost:15085/memory-game6085:1.0.1-v3
curl -fsS http://127.0.0.1:18086/api/health
```

仓库容器若已存在，检查后使用 `docker start memory-game6085-v3-registry`，不重复创建同名容器。再次执行本实验前也需检查 v3 应用容器，避免同名或端口冲突。可在原 v3 应用中完成并保存一局，再执行上述移除和拉取流程，对比新容器的排行榜验证成绩保留。

## 原 Windows 镜像发布与拉取

本实验使用本机私有 Registry 完成实际发布与拉取。仓库只绑定本机 5000 端口，无需外部账户。

```powershell
docker run -d --name memory-game6085-registry -p 127.0.0.1:5000:5000 -e OTEL_TRACES_EXPORTER=none --mount type=volume,source=memory-game6085-registry-data,target=/var/lib/registry registry:3
docker tag memory-game6085:1.0.0 localhost:5000/memory-game6085:1.0.0
docker push localhost:5000/memory-game6085:1.0.0
curl.exe -s http://localhost:5000/v2/memory-game6085/tags/list
```

仓库容器若已存在，可用 `docker start memory-game6085-registry` 启动，不重复创建同名容器。

下面的操作只针对本项目实验容器和镜像，保留数据卷，用于证明可以从仓库重新拉取：

```powershell
docker compose down
docker image rm localhost:5000/memory-game6085:1.0.0 memory-game6085:1.0.0
docker pull localhost:5000/memory-game6085:1.0.0
docker run -d --name memory-game6085-pulled -p 127.0.0.1:18085:8080 -e DATA_DIR=/app/data --mount type=volume,source=memory-game6085-data,target=/app/data localhost:5000/memory-game6085:1.0.0
curl.exe http://localhost:18085/api/health
```

报告中的发布与拉取实验已完成，实验结束时应用容器名为 `memory-game6085-pulled`。若要重跑 Compose，先检查并停止该项目容器以释放 18085；若要重新创建同名实验容器，先检查并处理对应旧容器。`docker compose down` 保留命名数据卷。

原实验机器的 Docker Desktop 曾出现遗留 socket 错误。配套的 `scripts/start-docker-runtime.ps1` 用于在 Docker Desktop 未运行时，以独立运行时缓存目录启动该机器上的 Docker Desktop；脚本只改变子进程环境，不修改系统级环境变量。脚本使用 Windows 默认安装路径，仅作为本次排障记录，不是一般部署的必需步骤。

## 验证 SQLite 持久化

1. 完成一局，填写昵称并点击“保存到花园榜单”，拍下排行榜。
2. 运行 `docker compose down`，随后 `docker compose up -d`。这是移除并重新创建容器。
3. 浏览器刷新，选择刚才的难度，确认成绩仍然存在。
4. 运行 `docker volume inspect memory-game6085-data` 查看挂载数据卷的信息。

不要使用 `docker compose down -v` 做保留数据的演示，它会删除命名数据卷。排行榜的难度筛选要与保存成绩时一致。

## 测试

```powershell
cd backend
mvn test
```

浏览器测试需要独立的测试实例，避免将自动测试成绩混入你的作业数据库。在项目根目录的一个终端启动：

```powershell
$env:PORT = '18080'
$env:DATA_DIR = Join-Path $PWD '.qa/data'
java -jar backend/target/memory-game6085.jar
```

另一个终端执行：

```powershell
cd frontend
npm ci
npx playwright install chromium
npm run test:e2e
```

也可设置 `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` 使用已安装的兼容 Chromium。浏览器测试会保存真实页面截图到 `frontend/test-results/`。完整首轮测试请使用空的测试数据库；再次运行可通过 `DATA_DIR` 指向新的测试目录，不需删除旧数据库。

UI 自动审核可在前端目录执行 `node scripts/audit-ui.mjs`，默认检查 18080。用 `GARDEN_TEST_URL` 指定其他地址；开发服务器用 `GARDEN_API_TARGET` 指定后端地址（默认 8080）。审核结果为自动扫描辅助证据，不等于完整人工无障碍认证。

## 接口

| 方法 | 路径 | 作用 |
|---|---|---|
| GET | `/api/health` | 服务与数据库可读检查 |
| POST | `/api/games` | `{ "difficulty": "easy/normal/hard" }` 创建牌局 |
| GET | `/api/games/{id}` | 当前牌局可见状态 |
| POST | `/api/games/{id}/flip` | `{ "index": 0 }` 翻牌 |
| POST | `/api/games/{id}/pause` | `{ "paused": true }` 暂停 / 继续 |
| DELETE | `/api/games/{id}` | 放弃牌局 |
| POST | `/api/games/{id}/score` | `{ "nickname": "花匠6085" }` 提交已完成牌局 |
| GET | `/api/leaderboard?difficulty=normal` | 对应难度前十名 |

成绩只能从已完成的服务端牌局生成，不接受浏览器传入步数与用时。这是教学项目，未实现面向公网的账号、防自动化和分布式会话功能。

## 作业截图建议

原始要求来自项目上级 `raw/要求.png`：部署 Docker、项目名称末尾加学号后四位、打包发布、演示拉取，全过程截图汇总到一个 Word 文件。

建议在真实操作时截图，终端画面同时包含**输入的命令与执行结果**：

1. `docker version`：同时显示 Client 和 Server，证明引擎可用。
2. 项目目录和 `memory-game6085` 名称、关键 Dockerfile 配置。
3. `docker compose up -d --build` 构建成功。
4. `docker compose ps`、日志以及 `/api/health` 返回结果。
5. 浏览器初始页面、进行中、完成并保存成绩。
6. `docker tag` 和 `docker push` 的实际成功结果。
7. `docker pull` 的实际结果，以及拉取镜像启动后的访问效果。
8. 容器重新创建前后的同一条排行榜记录与数据卷检查。

真实终端截图需在实际实验时采集。不要用示意输出、网页渲染的终端或拼接日志代替真实操作截图。Word 报告需在收集截图并确认大纲后制作。

## 技术来源

查阅日期：2026-10-21；仅查阅官方文档 / 项目仓库。

- [Vue 响应式基础](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)
- [Vite](https://vite.dev/guide/)
- [Spring Boot Servlet Web](https://docs.spring.io/spring-boot/reference/web/servlet.html)
- [Spring Boot Maven 打包](https://docs.spring.io/spring-boot/maven-plugin/packaging.html)
- [Xerial SQLite JDBC](https://github.com/xerial/sqlite-jdbc)
- [Docker Volumes](https://docs.docker.com/engine/storage/volumes/)

UI 使用 ui-ux-pro-max 的相关本地检索建议，植物插图为项目内 SVG，功能图标来自 Lucide；无远程字体、图片依赖。
