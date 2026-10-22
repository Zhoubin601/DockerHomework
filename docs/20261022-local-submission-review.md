# 最新版本本机测试与提交核查

日期：2026-10-22。检查版本：`392870d`（origin/main）。

## 结论

**应用及本机 Docker 全流程均通过，材料覆盖核心容器实验；当前 v4 仍建议修复 Word 结构后提交。**

最初发现 v4 Word 未通过严格 OOXML 结构校验、本机 Docker Desktop 启动失败。随后用户手动打开 Docker，已继续完成本机镜像构建、容器浏览器测试、push、删除后 pull、容器重建和持久化验证。**Docker 阻塞已经解除；Word 结构问题仍在。** 下方保留首次环境故障记录作为过程，不代表当前仍未测试。

## 更新范围

- 在干净的 main 分支执行 `git fetch origin`、`git pull --ff-only origin main`，由 `2a7be0c` 快进到 `392870d`。
- 新增 v2—v4 的历史交付及过程资料；未推送本轮改动。
- 原始要求、历史 output 文件在测试前后 SHA-256 均一致。

## 本轮实测

| 检查 | 结果及证据 |
|---|---|
| 从最新源码构建 | `scripts/build.ps1` 完成 npm ci、Vite build、Maven clean package，BUILD SUCCESS；`local-test-20261022/source-build.log` |
| 后端测试 | 3 项，0 失败、0 错误、0 跳过；涵盖三种难度、牌面隐藏、暂停、非法操作、完成成绩、重复提交和 SQLite 重新打开 |
| 实际交付 JAR | 从 v4 源码 ZIP 解压后以 Java 21 启动在 18080，独立数据库；健康接口 UP |
| 浏览器测试 | Playwright 3/3 通过，使用本机 Chrome；完整游戏、保存、排行榜、暂停、昵称验证、窄屏/横屏/320px、键盘对话框及连接失败重试；`playwright.log` |
| UI 自动审核 | 8 个场景均 0 axe violations，无横向溢出；桌面、平板、手机、横屏、320px、规则弹窗、进行中、暂停；`ui-audit.log` |
| 实际 JAR 重启持久化 | 停止后重启，完整排行榜 JSON 一致；真实浏览器测试成绩 1 条，未混入原作业数据库；`before-restart.json`、`after-restart.json` |
| 源码构建与交付一致性 | 重建 JAR 和交付 JAR 的 BOOT-INF 下 61 项内容全部一致；不要求含时间戳的整个 ZIP 摘要一致；`final-checks.json` |
| ZIP 校验 | 源码 ZIP 34 项、证据 ZIP 77 项 CRC 通过；源码条目与工作区相同（允许 CRLF/LF 差异）；证据清单 76 项摘要/大小通过 |
| Word 内容来源 | 21 张内嵌图全部匹配既有证据原 PNG；8 张表；无草稿、TODO、待确认或修订插入/删除节点；`package-audit.json` |
| Word 本机显示 | 对检查副本使用 OfficeCLI 调用本机 Word 渲染，29 页全页缩略检查，另查看 11、19、20 页大图；未见整页空白或明显分页丢失。图 A1a 与图题之间留白较大，属于排版可改善项 |
| Word 严格结构 | **失败：213 条 schema errors**；详见下文及 `v4-schema-validation.txt` |
| 本机 Docker | **用户恢复后全流程通过**；Docker Client/Server 29.8.2；源码镜像构建复用 BuildKit 缓存，容器浏览器测试 3/3，真实 push/移除/pull/重建/榜单对比通过；`docker-source-build.log`、`docker-browser-tests.log`、`docker-roundtrip/results.json` |

路径说明：表内相对日志位于 `docs/local-test-20261022/`。自动审核是辅助验证，不表示完整人工无障碍认证。

## 对照原始指导要求

唯一原始要求来源：`raw/要求.png`，本轮直接查看。未增加原图没有规定的评分条件。

| 要求 | 当前证据及判断 |
|---|---|
| 在机器上部署 Docker 环境 | 历史 Windows/Linux 引擎与配置图存在，v4 如实说明沿用已装引擎；原 Windows 安装、首次配置、恢复操作的历史过程截图资料未提供。今天用户恢复 Docker 后，Client/Server 及容器实测已通过 |
| 使用已有 Spring Boot 项目 | 项目是可运行的 Spring Boot 应用，先完成后再容器化；本轮源码构建通过。“已有”是否另指旧课堂项目，原图未进一步解释，资料未提供教师额外限定 |
| 项目名末尾为学号后四位 | 满足：目录、artifactId、name 均为 `memory-game6085`，与已确认学号 `20246085` 的后四位一致 |
| 打包到 Docker 发布 | v4 第五、六章和附录 A2/A3/A5 有真实历史证据；今天独立镜像源码构建、容器运行、本机 Registry push 均通过，容器内 BOOT-INF 61 项与交付 JAR 一致 |
| 发布后演示拉取 | 历史两组证据及今天本机独立资源实测均通过；本轮删除应用容器和两个本地标签后执行 pull，返回 Downloaded newer image，再创建新容器且完整榜单保留。各仓库仅绑定本机，未公开发布 |
| 所有过程截图汇总一个 Word | v4 一个 Word 含 21 张原图，核心实验步骤已覆盖；安装/首次配置历史过程图仍缺。Word 能显示，但结构兼容性校验失败，建议修订后交 |

## Word 新发现

命令：`officecli validate output/v4/20261021-docker-lab-report-v4.docx`。退出码 1。

- 128 条：`snapToGrid` 元素顺序不符合 schema。
- 78 条：`color` 元素顺序不符合 schema。
- 3 条：`tcBorders` 元素顺序不符合 schema。
- 3 条：`shd` 缺少必需的 `val` 属性。
- 1 条：`updateFields` 元素顺序不符合 schema。

这是 **5 类问题的 213 次报错**，不等于 213 个业务功能缺陷。Word 可打开并渲染，也不能替代严格结构校验。此前记录的 XML 可解析、ZIP CRC 通过仍然属实，但它们不能证明 OOXML schema 合规。本轮未改写 v4，建议下一版规范化这些属性后重新校验及检查分页、目录。

另有 `officecli view ... issues` 的 140 条格式提示，主要涉及图题空格、代码缩进和中英标点，未将其全部当成实质错误。

## 首次 Docker 阻塞详情（现已解除）

1. 初始 `docker version` 仅返回 Client，`dockerDesktopLinuxEngine` 管道不存在。
2. 依 README 执行原排障脚本，固定缓存目录下 `sailor-ingest.sock` 重命名失败，Docker Desktop 退出。
3. 仅停止本轮启动的 Docker 进程后，用全新子进程缓存目录再次启动；新故障为 Volume Backup Scheduler 写入/重命名计划文件失败，错误为 `The system cannot move the file to a different disk drive`，引擎仍不可用。
4. 进一步尝试停止本轮故障实例、预置已有空计划文件并使用新缓存目录启动，被自动审批拒绝，工具仅返回 `blocked by policy`，没有提供更具体理由；该操作未执行，也没有绕过审批继续同一恢复动作。

未执行恢复出厂设置、删除 Docker/WSL 数据、删除原容器或原数据卷等破坏性操作；系统环境变量未修改。

## 用户恢复 Docker 后的实际复测

用户明确表示已打开 Docker 并要求继续，随后 `docker version` 同时返回 Client/Server 29.8.2。未再执行被拒绝的恢复动作。

- 源码构建：`docker build --progress=plain -t memory-game6085:localtest-20261022 Code/memory-game6085`，退出码 0。本次复用 BuildKit 缓存；未声称容器内 Maven 测试重新执行，前一阶段本机 Maven 3 项测试已通过。
- 资源：独立前缀 `memory-game6085-localtest-20261022`，应用端口 18087，Registry 端口 15086，独立网络、应用和仓库数据卷；均带测试标签，未复用原实验数据库。
- 源码镜像内 JAR：SHA-256 `6126a1faf7e80ec948c5be2b50d834c7f3a4ef9f65089fcd49431f532a1b1389`；与交付 JAR 的整包摘要不同，但 BOOT-INF 下 61 项应用类、静态资源及依赖内容完全相同。ZIP 元数据不同不等于应用不同，未声称整包摘要相同。
- 容器以 `uid=999(garden)` 普通用户运行，健康检查 UP；对实际容器运行 Playwright，3/3 通过。
- 浏览器真实保存测试成绩：`测试花匠6085`、轻松难度、12 步、9271ms，记录编号 1，仅用于本轮独立测试。
- 发布到 `localhost:15086/memory-game6085:localtest-20261022` 成功；删除本轮应用容器及两个本地标签，分别 image inspect 确认不存在，数据卷保留。
- pull 返回 `Downloaded newer image`；仓库 push/pull digest 均为 `sha256:1333c043c6b02570c3df12afaa82559359e459bcdd58a69e30ec88a01da2ac38`。
- 原容器前缀 `91b23f11f6da`，新容器 `cdb872c45267`；完整排行榜 JSON 一致，容器内 JAR 摘要相同，仍挂载同一独立数据卷。
- 新容器浏览器复查能显示保存的成绩，无 pageerror，截图为 `local-test-20261022/docker-roundtrip/after-recreate-ui.png`。
- 开始前已存在的全部容器 ID 和运行/停止状态在复测结束后保持一致，包括课堂项目及原作业实验容器。

测试脚本最初直接比较完整 RepoDigests 列表，因为推送前还包含源仓库别名而触发断言。已修正为只比较目标 Registry 仓库的摘要，并利用保留的原始结果重新核验通过；没有为此重复容器操作或更改实验结果。原失败记录与归一化前 JSON 保留，可追溯。

当前保留新拉取的测试容器及 Registry 供本机查看，页面为 `http://127.0.0.1:18087`。本轮日志和截图保存在 `docs/local-test-20261022/`，不写入旧报告，也不覆盖历史 output。

## 提交建议与剩余事项

- **作业内容层面**：按原图，核心 Spring Boot → Docker → Registry 发布 → 删除后拉取流程有历史证据，也已通过今天本机复测；已有 Word 包含核心步骤真实截图。
- **当前验收层面**：应用和 Docker 已通过；v4 Word 严格结构校验仍失败，建议修复并重新检查目录、分页和校验后再提交。无需再重复已经通过的业务/Docker测试，除非修改应用或部署配置。
- 提交前由用户复核教师是否另有课堂限定；原图未指定公开仓库、异机拉取、必须旧课堂项目、安装截图清单或专用模板，不将这些猜测当成既定扣分项。
- 如果教师严格要求 Docker 安装/首次配置全过程，需取得真实操作截图；不补造历史安装凭证。

本轮只做测试与核查，没有生成新的正式 Word 或替换 output 中的历史成品。全部新增记录及检查副本放在 docs/。使用 officecli-docx 技能；项目列出的 minimax-docx 不可用，未冒称使用。

## 后续修复状态：v5

用户随后要求修复所有错误并生成v5推送。本记录的v4问题已在v5解决：严格Word结构校验0错误，图题/参考资料/目录已整理，新增本机复测附录；31页22图9表42项目录经Word原生分页和独立复核通过。最新成品为output/v5，详细变化见docs/20261022-v5-changes.md。本记录保留此前检查时的真实结论，不再将v4的错误视为v5未完成项。
