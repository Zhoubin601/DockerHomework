# 资料来源

## 2026-10-22 v7安装补图与远端交接

- 用户明确授权清除失效引用并补安装、首次配置及资源创建配置图，随后要求先提交远端，剩下远端完成。
- 实测来源：`docs/v7-work/01-before-install.txt`、`02-official-repository.txt`、`03-install-engine.txt`，对应result.json均退出码0；apt完整日志同步保存。5张PNG是实际日志浏览器显示截屏，不冒充历史Windows安装界面。
- Docker CE/CLI实际安装29.9.2、Compose5.6.1；配置启动和后续阶段未执行，Word尚未修改。详情见远端交接文档。
- 来源名称：Docker官方文档 Install Docker Engine on Ubuntu；链接：https://docs.docker.com/engine/install/ubuntu/；引用日期：2026-10-22；用途：核对官方APT源、GPG及安装包。
- 来源名称：Docker官方文档 Install Docker Engine from binaries；链接：https://docs.docker.com/engine/install/binaries/；引用日期：2026-10-22；用途：比较安装方式，实际未采用静态二进制流程。

## 2026-10-22 当前 v6 两文件提交核查

- 教师原始依据：`raw/要求.png`，本轮直接查看，明确“所有过程进行截屏放在一个Word文件里上交”。
- 被检实物：`output/v6/memory-game6085.docx`（SHA-256 `fd4787b33ed40fede5c035b55a4779e346cedf982fe68c61b702d91409d8b28f`）、`output/v6/memory-game6085.zip`，不使用旧版本统计替代。
- 本机Word只读副本原生分页为18页、11图、6表；11图逐字节匹配v5证据ZIP。第3页表格及第4/5页引用附录A/B，但当前文件没有附录与相应11图。
- 源码ZIP与v5对应ZIP字节一致，34项CRC通过，包内文件与Code对应内容一致，JAR摘要匹配。历史运行验收仅作背景，本轮未运行构建/Docker测试。
- 检查记录：`docs/20261022-v6-submission-review.md`；机器结果：`docs/v6-submission-audit-20261022/`。没有查询外部资料，没有修改raw/output。

## 2026-10-21 v4 修订来源

- 最终独立核查：docs/v4-work/content-review.md验证11条新增命令与原脚本／日志一致；final-evidence-verification.json验证21张图与源PNG、两个ZIP及旧证据字节一致。全部29页视觉检查分别记录于docs/v4-report-work/visual-qa-pages1-15.md和visual-qa-pages16-29.md，两份均绑定最终DOCX摘要。
- 正式文件已写入output/v4；最终Word SHA256为b994d30b27959cf9c6eec6446077be4f7cef66015b736571f9b1fed375db3ebd；原始图及v1—v3共16份文件摘要保持不变，最终清单见docs/v4-work/release-manifest.json。

- 用户明确授权“修改生成v4，然后推送”；范围以docs/20261021-v3-output-review.md为依据，沿用既有九章结构、姓名和学号。
- Word新增图源为docs/v3-evidence/01-resource-creation.png：真实网络和应用／仓库数据卷创建过程，配套首次日志01-linux-config.txt；现有01-config-review.png继续证明随后配置检查。
- 可复制命令与结果来源：docs/v3-evidence/03-container-run.txt、04-registry-push.txt、09-recreate-verify.txt及results.json；Linux镜像仍为1.0.1-v3，不将资料改版写成新实验。
- 旧原始图及v1—v3共16份文件摘要保存于docs/v4-work/baseline-sha256.json；v4预览沿用v3截图，业务源码与交付JAR不变。
- 原Windows历史安装、首次配置及启动恢复操作截图仍未提供，Linux也沿用平台已有Docker引擎；保持如实说明，不伪造缺失材料。

## 2026-10-21 最新 v3 独立复查

- 按用户“拉取最新，检查v3”的要求，将当前仓库从ef396fe快进到origin/main的14a2cbb；原始要求仍为raw/要求.png，已直接查看。
- 直接读取output/v3五个交付文件，对照docs/v3-evidence、docs/docker-evidence及Code/memory-game6085；未只沿用历史自检结论，未查询外部技术资料。
- 重新渲染DOCX 28页，与既有最终页面逐页像素一致；20张图与原PNG字节匹配，39项目录页码独立核对通过。记录：docs/v3-audit-work/docx-checks.json、render-comparison.json、final-checks.json。
- 新发现：Word附录A1只嵌入01-config-review.png；真实创建过程图01-resource-creation.png已在来源和证据ZIP，但未放Word。Docker安装、首次配置及Windows恢复过程截图仍未提供，见docs/20261021-v3-changes.md:36。
- ZIP/JAR、摘要与现有Docker凭证一致；抽取交付JAR隔离启动通过，记录docs/v3-audit-work/package/verification.json。判断与建议见docs/20261021-v3-output-review.md；未改正式交付物。

## 2026-10-21 v3 修复来源

- 本轮实际成功证据位于docs/v3-evidence，包含真实终端PNG、transcript、命令脚本、results.json、前后完整榜单与浏览器截图。新实验为Linux，Docker28.4.0/Compose2.40.3，镜像1.0.1-v3、本机仓库15085、应用18086；原Windows事实未替换。
- 实际交付JAR与容器内JAR哈希一致，push/pull摘要一致，重建后完整榜单保留；记录为6085v3实验、11步、7268ms。最终28页Word和各文件摘要见docs/v3-work/release-manifest.json。

- 用户当前指令：“修复所有生成v3”。修复范围以本轮v2核查记录和raw/要求.png为依据，保持已确认的项目与报告结构。
- 基线：最新远端ef396fe的output/v2，旧版本与原图哈希见docs/v3-work/baseline-sha256.json。
- 当前实际环境：Debian GNU/Linux 13云工作区，Docker已由运行平台部署；无法访问原Windows桌面，不能提供原机器历史安装或首次配置画面。
- 本轮计划新增真实Linux环境配置、构建、运行与发布/拉取证据，记录实际命令、时间和结果；与既有Windows证据分别保存，不把Linux结果改写成Windows实验结果。

## 2026-10-21 最新 v2 输出复核来源

- 本地原工作区仍为 `2a7be0c`；经 GitHub 连接器读取最新 main，确认新增提交 `ef396feb359c338f0fec442facc5ea368fafeef5` 及 `output/v2/`，随后 fetch 并独立检出到 `/workspace/DockerHomework-v2-review/`。
- 来源链接：https://github.com/Zhoubin601/DockerHomework/commit/ef396feb359c338f0fec442facc5ea368fafeef5 ；读取日期：2026-10-21。未查询外部技术资料。
- 直接查看 `raw/要求.png`，核查最新检出的 v2 Word、两个ZIP、对应源码及原始实验PNG/TXT/JSON；未将本地旧v1代作v2。
- 最终Word哈希 `ea45f858c2230140c93bc059cad3d782c8e92ca3ede9e81b3aae423a77919f09` 与提交内release记录一致；实际图4已换成 `02-build-progress.png`。
- 历史安装/首次配置截图仍未提供，新增第5页为环境沿用、恢复与验证说明。详细结论和修改建议见 `docs/20261021-v2-output-review.md`。

## 2026-10-21 v2 修订来源

- 用户在 v1 复核后明确要求“修改生成v2”，沿用已确认大纲和身份信息。
- 环境恢复说明来源：`docs/docker-experiment-notes.md` 第7–12行、`Code/memory-game6085/scripts/start-docker-runtime.ps1`、`docs/docker-evidence/01-environment.txt`；WSL2/Linux 引擎还可由 `results.json` 的内核与引擎信息核实。
- 图4使用已有原图 `docs/docker-evidence/02-build-progress.png`，与 v2 Word 嵌入字节一致；历史安装/首次配置截图资料仍未提供，没有补造。
- 新构建与启动验证来源：`docs/v2-code-work/maven-package.log`、`backend-test-results.txt`、`validation.json`；这些记录不替代原 Windows Docker 发布/拉取日志。
- v2 变更与边界：`docs/20261021-v2-changes.md`；Word结构、目录、图片匹配与原文件保留检查：`docs/v2-report-work/structural-validation.json`。

## 2026-10-21 当前 v1 全交付物复核

- 原始依据仍为 `raw/要求.png`；本次重新直接查看原图，并读取 `output/v1/` 内 Word 与两个 ZIP，未仅沿用历史结论。
- Word 正文有7个表格、11张嵌入截图；图片与 `docs/docker-evidence/` 中对应 PNG 字节一致。正式报告及原始要求图 SHA-256 与先前检查记录一致。
- 图4实际使用 `02-build.png`，已有 `02-build-progress.png` 含 `Building jar`、`repackage`、`BUILD SUCCESS`，可直接用于后续补强；现有证据包未包含这张补充图。
- 新增交付完整性发现：源码包 README 第113行引用的 `scripts/start-docker-runtime.ps1` 未收入该 ZIP；项目 `Code/` 中存在对应文件。
- 当前判断及分级建议：`docs/20261021-v1-delivery-audit.md`；配套独立核查：`docs/v1-audit-20261021-code.md`、`docs/v1-audit-20261021-evidence.md`。
- 本次不修改原始要求、v1成品或应用源代码，不重新执行 Docker 实验，不查阅外部资料。

## 2026-10-21 v1 报告复查来源

- 原始要求：raw/要求.png。本轮重新查看原图，要求为部署 Docker 环境、已有 Spring Boot 项目、项目名末尾加学号后四位、打包发布、发布后演示拉取、所有过程截图汇总一个 Word。
- 被查文件：output/v1/20261021-docker-lab-report-v1.docx。直接读取正文、7 个表格及图像关系，并用其检查副本进行 Word 原生页面渲染；不是仅依据历史验证结论。
- 对照证据：docs/docker-evidence/01-environment.png、02-build.png、02-build-progress.png、05-registry-push.txt、06-remove-local.txt、07-registry-pull.txt、08-run-pulled-image.txt、02-build.txt、results.json，以及 Word 内引用的其他截图。
- 本地实现对照：Code/memory-game6085/Dockerfile、compose.yaml、backend/pom.xml、backend/target/surefire-reports/cn.memorygarden.GardenTests.txt。
- 既有范围确认记录：docs/questions.md、docs/report-outline.md、memory-bank/project-context.md。它们证明此前项目选择及本机 Registry 方式的用户确认，不构成教师额外规则的来源。
- 新发现：报告第 6 页图4嵌入 02-build.png，仅显示镜像导出和镜像列表；未显示 Maven BUILD SUCCESS。现有 02-build-progress.png 明确包含 JAR 打包、Spring Boot repackage 和 BUILD SUCCESS，可用于后续修订，不需要补造证据。
- 环境部署安装/首次配置过程截图、教师对新项目或公开仓库的额外规定：资料未提供。当前图2可证明 Docker Client/Server 可用，但不能展示安装或配置过程。
- 本轮没有联网查资料，没有重新执行 Docker 构建、删除或发布操作。详细结果见 docs/20261021-v1-report-review.md。

## 正式报告事实核对（2026-10-21）

- 来源名称：本机真实 Docker 实验及截图。
- 链接或文件名：docs/docker-evidence/results.json 与正式报告第九章列出的 11 个 PNG 文件。
- 引用日期：2026-10-21。
- 结果：镜像构建成功，本机 Registry push 成功，删除本地镜像后 pull 成功；新旧容器标识不同，同一数据卷内完整排行榜一致。
- 正式 Word 使用 officecli-docx 制作并经本机 Word 原生渲染检查，共 15 页，11 张截图与原 PNG 字节一致；TOC、PAGE 字段有效，7 个表格结构检查通过。
- raw/要求.png 的 SHA-256 在交付前复核一致，未改写原始资料。

## raw/要求.png

- 查看日期：2026-10-21。
- 课程显示为《2026云计算技术与架构》，作业主题为 docker。
- 要求原文：请同学们在机器上部署docker环境，并将一个已有的SpringBoot项目（项目名最后加上学号后四位命名）打包到docker上进行发布。发布后再演示拉取。所有过程进行截屏放在一个Word文件里上交。
- 明确要求：部署 Docker 环境、使用已有 Spring Boot 项目、项目名称末尾添加学号后四位、打包发布、发布后演示拉取、过程截图汇总至一个 Word 文件提交。
- 截图数量、指定操作系统、镜像仓库、Word 模板、截止时间：资料未提供。
- 原图没有指定发布平台；用户随后确认本机私有 Registry，已实际推送并删除本地镜像后重新拉取。

## 用户当前消息

- 2026-10-21：用户确认学号后四位为 `6085`，要求记住。
- 用户回忆老师好像要求终端命令行截图；要求图仅明确写“所有过程进行截屏”，未单独限定截图界面类型。

## 2026-10-21 用户补充

- 用户要求从电商项目转为新建轻量小游戏，指定 Vue3 + Vite + Spring Boot + SQLite，使用 SQLite 持久化。
- 用户明确要求使用 ui-ux-pro-max 开始实现并审核、美化 UI；代码放在根目录 Code 文件夹。
- 用户明确允许仅查官方文档，用于核对依赖和部署细节。
- 用户确认报告身份信息：周宇斌／软件2401／20246085，确认九部分报告大纲，并要求先补齐 Docker 实验再制作提交版。
- 用户确认使用本机私有 Registry 完成真实 push/pull 演示。

## 外部技术资料（用户已允许）

### Spring Boot 可执行归档
来源名称：Spring Boot 官方文档，Packaging Executable Archives
链接或文件名：https://docs.spring.io/spring-boot/3.5/maven-plugin/packaging.html
引用日期：2026-10-21
用途：核对 repackage 与 java -jar 的可执行打包方式；具体版本以项目 pom.xml 和实际构建为准。

### Spring Boot Servlet Web
来源名称：Spring Boot 官方文档，Servlet Web Applications
链接或文件名：https://docs.spring.io/spring-boot/reference/web/servlet.html
引用日期：2026-10-21
用途：核对 Spring MVC、RestController 与静态资源服务。

### Vite
来源名称：Vite 官方文档，Getting Started
链接或文件名：https://vite.dev/guide/
引用日期：2026-10-21
用途：核对开发服务器与生产构建；依赖锁定于 package-lock.json。

### SQLite JDBC
来源名称：Xerial SQLite JDBC 官方仓库
链接或文件名：https://github.com/xerial/sqlite-jdbc
引用日期：2026-10-21
用途：核对 JDBC 连接和原生库打包；仓库示例版本为 3.53.4.0。

### Docker 数据卷
来源名称：Docker 官方文档，Volumes
链接或文件名：https://docs.docker.com/engine/storage/volumes/
引用日期：2026-10-21
用途：核对命名数据卷与容器生命周期、持久化目录挂载。

### 补充核对
来源名称：Vue 官方文档，Reactivity Fundamentals
链接或文件名：https://vuejs.org/guide/essentials/reactivity-fundamentals.html
引用日期：2026-10-21
用途：核对 Vue3 响应式状态与组件更新。

来源名称：Spring Boot 官方文档，当前 Maven Packaging
链接或文件名：https://docs.spring.io/spring-boot/maven-plugin/packaging.html
引用日期：2026-10-21
用途：核对当前项目所用 Spring Boot 可执行 JAR 打包。

来源名称：Docker Official Images，Maven 清单
链接或文件名：https://raw.githubusercontent.com/docker-library/official-images/master/library/maven
引用日期：2026-10-21
用途：查看官方 Maven 镜像体系；另用 docker manifest inspect 实测 Dockerfile 中 3.9.16-eclipse-temurin-21 标签可解析，返回 OCI image index。

### 本地 Registry 实验
来源名称：CNCF Distribution 官方文档，Deploy a registry server
链接或文件名：https://distribution.github.io/distribution/about/deploying/
引用日期：2026-10-21
用途：核对 Registry 容器启动、本地标记、push/pull 与删除本地标签后重新拉取的实验方式。仓库仅绑定回环地址，用于课程实验。

### Docker 启动故障对照
来源名称：Docker 官方 GitHub 问题跟踪库，for-win issue 15064（问题报告，非官方修复保证）
链接或文件名：https://github.com/docker/for-win/issues/15064
引用日期：2026-10-21
用途：对照 Windows 遗留 AF_UNIX socket 的启动症状。本机目录改名被拒绝，最终采用子进程独立 LOCALAPPDATA 运行时目录启动；Client/Server 已实际恢复，不将问题报告内容当作本机成功证据。

## 2026-10-22 本机验收来源

- 原始指导要求：raw/要求.png，本轮直接查看原图，六项要求沿用原文。
- 最新代码来源：origin/main，GitHub 仓库 https://github.com/Zhoubin601/DockerHomework ，2026-10-22 拉取到 392870d；由 2a7be0c 快进，无本地修改冲突。
- 被查交付：output/v4/ 下正式 Word、源码/JAR ZIP、证据 ZIP；本轮独立验证结果另记，不将历史结果替代本轮实测。
- 参考过程：docs/20261021-v4-changes.md、docs/v4-work/content-review.md、docs/v4-work/evidence-review.md；项目技术及身份确认见 memory-bank/project-context.md。
- 当前未查询外部技术资料。依赖及镜像下载为执行用户要求的本机测试，不作为新增作业要求来源。

### 本轮直接实测补充

- 本机原生Word渲染v4检查副本29页，21张图片原字节均与docs/docker-evidence或docs/v3-evidence匹配。
- officecli严格OOXML验证213条报错（5类），与XML可解析/ZIP CRC通过是不同检查层次。
- 本机源码构建、3项后端测试、3项浏览器测试、8个UI检查场景、交付JAR重启数据保留均通过；Compose配置校验退出码0。
- Docker本轮原始错误取自两个测试运行时目录的Docker/backend.error.json；仅提取错误记录到docs/local-test-20261022/docker-errors.json。进一步恢复动作被自动审批拒绝，未执行。
- 全部结果及限制见docs/20261022-local-submission-review.md；raw/及output/摘要复核不变。

## 2026-10-22 Docker继续实测来源

- 用户当前消息：已打开Docker，继续验收。
- 直接事实来源：docs/local-test-20261022/docker-source-build.log、docker-browser-tests.log、docker-roundtrip/中的实际命令输出及results.json。
- 实测：源码Docker构建退出码0（复用缓存），容器浏览器3/3，通过独立Registry push、删除本地标签后pull、新容器完整榜单一致。
- 原始要求仍为raw/要求.png，未新增外部规则；Word及raw/output旧文件未修改。

## 2026-10-22 v5修复依据

- 用户已明确要求修复、生成v5并推送。
- raw/要求.png为唯一教师原始指导图，本轮重新查看；报告身份和结构沿用既有确认。
- Word错误来源：docs/local-test-20261022/v4-schema-validation.txt（213条5类）；显示与格式对照：word-contact.png和v4-issues.txt。
- 新增实测来源：docs/local-test-20261022/docker-roundtrip/results.json、source-image-vs-delivery.json、真实浏览器截图及Docker命令日志；测试通过事实已逐项核验，不改写既有Windows/Linux实验版本。
- 本轮使用officecli-docx及本机Word；minimax-docx不可用，无新增外部技术资料。

### v5正式交付来源复核

- output/v5/20261022-docker-lab-report-v5.docx：最终31页22图9表，严格校验0错误，Word原生42目录项全部真实页核验；SHA-256见docs/v5-work/release-manifest.json。
- 21张历史图保持原字节，新图来自docs/local-test-20261022/docker-roundtrip/after-recreate-ui.png；附录B的数字、摘要和容器标识来自results.json原件。
- 源码包及证据包来源、132项证据成员、131项摘要清单、两张预览准确来源见docs/v5-work/package-validation.json和independent-package-audit.json。
- 最终独立复核见docs/v5-work/independent-final-review.md；raw/与历史21份文件基线核验通过。

## 2026-10-22 最新 v5 独立本机验收

- 原始指导图：raw/要求.png，本轮直接查看。历史安装/首次配置截图仍资料未提供，不将环境可用当作安装过程截图齐全。
- 代码来源：origin/main，仓库 https://github.com/Zhoubin601/DockerHomework ，读取日期2026-10-22；fetch及pull --ff-only后本机和远端均80222d5022dbfb6661f0933f98ad71281213ca25，无更新。
- 直接测试output/v5实际源码ZIP，重构建成功，后端3/3；Docker源码构建复用缓存；精确交付JAR容器浏览器3/3，独立15087仓库push、移除本地标签后pull、18088新容器完整榜单保留均通过。三份JAR的BOOT-INF 61项均一致。
- 直接核验v5五份文件摘要、ZIP CRC及131项证据清单；Word严格校验0错误，本机Word只读副本31页，42项目录均对实际PDF页通过。22张内嵌图全部匹配证据ZIP原图。
- 来源日志与结果：docs/v5-local-acceptance-20261022/；提交判断：docs/20261022-v5-local-submission-review.md。raw/output 26份摘要无变化，原有容器ID和状态不变。未查询外部技术资料。

## 2026-10-22 v5 语言审阅来源

- 用户当前要求：检查 v5 报告有无 AI 写作观感或生硬措辞；本轮仅审阅，不改写报告。
- 原始作业图：`raw/要求.png`，本轮直接查看。要求为 Docker 环境、Spring Boot 项目打包发布、项目名末尾加学号后四位、发布后拉取、截图汇总 Word；没有提供所谓 AI 检测标准。
- 直接审阅文件：`output/v5/20261022-docker-lab-report-v5.docx`；SHA-256：`397fd74b20f657f391f26137b13b1c8a2103976a39564b2520ae28156645dc1e`，与 v5 发布清单一致。
- OfficeCLI 全文及独立 XML 提取：`docs/v5-language-review/officecli-text.txt`、`extracted-content.json`、`tables.md`。直接覆盖 261 个正文顶层段落（含目录等）、9 个表格及文档核心属性；OfficeCLI 的普通 text 视图仅提示表格存在，已另行读取全部单元格。
- 定位依据：DOCX 原有 paraId、章节及 `docs/v5-report-work/native-pagination-verification.json` 已核验的原生 Word 页码。本轮没有重新分页或修改成品。
- 事实保留依据：`docs/20261022-v5-changes.md`、`docs/local-test-20261022/docker-roundtrip/results.json` 及既有项目确认记录；保留历史安装图缺失、三轮实验来源及 JAR 整包摘要与应用内容不同层次的说明。
- 使用现有 `officecli-docx`；项目指定的 `minimax-docx` 当前不可用。本轮没有联网、没有使用 AI 检测服务，也不根据措辞反推作者身份或生成概率。

## 2026-10-22 v6 报告语言修订来源

- 用户当前明确要求：“修改生成v6报告即可”；沿用现有大纲，授权落实前轮 15 组语言建议，仅生成报告。
- 原始作业要求仍为 `raw/要求.png`。现行 v5 报告 SHA-256 为 `59dcc175d7ba3cb2a9afb67f68ee3d8b07430d1928c058d64c063337ab16ac87`，已冻结副本到 `docs/v6-report-work/source-v5.docx`；与前轮提取的唯一正文差别为封面去掉复测日期，v6 保留当前写法。
- 修订依据：`docs/20261022-v5-language-review-v1.md`；精确前后文本见 `docs/v6-report-work/applied-changes.json`。未增加实验事实、第一人称经历或外部资料。
- 本轮独立内容及全 31 页视觉检查见 `docs/v6-report-work/independent-content-review.md`、三份 `visual-qa-pages*.md`；42 项目录实际页验证及原图/历史文件保留见同目录 `native-pagination-verification.json`、`final-checks.json`。
- 正式报告：`output/v6/20261022-docker-lab-report-v6.docx`；SHA-256 为 `0e7da8d82e69a5ccc9492cd99ed77d17f3ffe5bb5e0260d05b0de264ac2f4294`。31 页、22 图、9 表、严格校验零错误；配套源码/证据包仍沿用 v5，本轮没有重打包。
