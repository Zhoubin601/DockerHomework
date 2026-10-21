# 资料来源

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
