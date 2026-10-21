# v1 源码交付包检查（2026-10-21）

## 范围与来源

- 原始要求：`raw/要求.png`，本次直接查看；要求部署 Docker、已有 Spring Boot 项目、项目名末尾加学号后四位、打包发布、发布后演示拉取，所有过程截图汇总一个 Word。
- 被查包：`output/v1/20261021-memory-game6085-v1.zip`。
- 对照：`Code/memory-game6085/`、`docs/docker-evidence/02-build.txt`、`docs/docker-evidence/results.json`。
- 本次未联网，未修改 raw、output、应用源码或 Code 下生成目录，未执行本地重新构建，也未执行 Docker 构建、删除、推送或拉取。本文“本地 JAR”指审计开始时已存在于 Code/ 下的文件。

## 结论

源码包足以支持当前课程项目的构建与运行，未发现源码缺失或程序无法启动的问题。不能据此替代 Word 的过程截图，也不能替教师确认“已有项目”的具体含义或本机 Registry 的接受范围。

### 已验证

1. ZIP 共 29 个文件，CRC 校验通过。包含完整前后端源码、前端依赖锁文件、Dockerfile、Compose、README、构建脚本、后端/浏览器测试和可执行 JAR；未包含真实数据库。
2. 所有 ZIP 内源码与 Code/ 对应文件逐字节一致。项目目录、Maven artifactId/name/finalName、Spring 应用名、前端包名均为 `memory-game6085`。
3. Dockerfile 多阶段构建前端和后端，运行阶段为 Java 21 JRE；Compose 映射 `127.0.0.1:18085:8080`，挂载 `memory-game6085-data` 到 `/app/data`。README 的发布/拉取命令与本机 Registry、结果记录一致。
4. Dockerfile 第 8 行使用 `maven:3.9.9-eclipse-temurin-21`，与实际 `02-build.txt` 一致。历史资料提到 3.9.16 标签核对不能理解为本包使用的版本。
5. 交付 JAR 结构及 CRC 正常，Manifest 记录 Spring Boot 4.1.1、Java 21、入口 `cn.memorygarden.GardenApplication`。与本地 JAR 对比，当前首页、当前 JS/CSS、后端类内容一致；差别是交付 JAR 额外保留了 6 个历史前端 bundle。
6. 对交付 JAR 进行了隔离运行烟测：使用 Java 21.0.12.1、随机未占用端口和独立临时 SQLite。健康接口返回 UP；首页与引用 JS/CSS 可读取；easy 牌局创建成功，12 张卡片的 symbol 全部隐藏。结束后已停止进程，未触及原实验数据。小型记录见 `docs/v1-code-audit-work/smoke-result.json` 与 `startup.log`。

## 修改建议（均非 Word 作业的主要阻断项）

- **P3／说明与附件一致性**：`Code/memory-game6085/README.md:113` 说明可运行 `scripts/start-docker-runtime.ps1`，但交付 ZIP 未含该脚本。修改时二选一：将已存在的真实脚本纳入下一版源码包；或移除 README 对该脚本的可用性承诺，说明它仅为原机器排障记录。Dockerfile、Compose 与普通本地运行不依赖此脚本。
- **P3／清洁构建**：交付 JAR 含 6 个未被当前首页引用的历史前端 bundle。建议将本地构建命令改为 `mvn -B -ntp clean package`，再重新封装下一版 JAR，以确保只含当前构建产物。当前页面引用的资源存在且烟测正常，不应把该项描述为功能故障。

## 检查边界

未从零安装依赖或重建 Docker 镜像；本次可复现性结论基于包内容、真实历史构建日志与交付 JAR 的隔离烟测。没有把本机 Registry 的发布夸大为公开仓库或异机部署。
