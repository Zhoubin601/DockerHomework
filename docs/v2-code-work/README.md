# v2 源码包制作与验证

日期：2026-10-21。

依据：`raw/要求.png`、`docs/20261021-v1-delivery-audit.md`、v1 源码交付包与当前 `Code/memory-game6085/`。本次不修改 raw、v1 交付物或历史 Docker 实验，不重新推送镜像。

## 修改

- `Code/memory-game6085/README.md` 改为实验报告口吻，并将“当前运行中”改为“实验结束时”，避免将历史状态写成当前状态。
- `scripts/build.ps1` 使用 `clean package`，避免旧静态资源混入后续 JAR。
- 源码 ZIP 在原有29个条目基础上加入 `scripts/start-docker-runtime.ps1`，共30个条目。README 说明该脚本只用于原 Windows 实验机器排障，普通 Docker 部署不依赖它。
- Dockerfile、Compose、应用业务源码保持不变；交付版本 v2 与应用/实验镜像版本 `1.0.0` 含义不同。

## 实际构建

使用工作区已有的 Node.js/npm、JDK 21 与 Maven 3.9.9、Maven 离线缓存，不联网、不安装工具。复制源码到独立临时工作目录，使用前端现有依赖执行 `npm run build`；随后在全新、无 target 目录的后端执行：

```text
mvn -o -B -ntp -Dmaven.repo.local=/workspace/.cloud-tools/m2 package
```

由于离线缓存不含 clean 插件，本轮采用从空目录构建来确保没有旧文件。交付脚本则已经改为标准 `clean package`，供通常联网环境使用。

Vite 构建成功；Maven 打包成功，3项后端测试全部通过。新 JAR 仅包含当前首页引用的一个 JS 和一个 CSS，不再保留6个历史前端 bundle。全部后端应用 class 与 v1 JAR 逐字节一致，见 `jar-comparison.json`。临时构建副本已清理，构建日志及测试结果保留。

## 验证

- ZIP CRC 和 JAR CRC 均通过；ZIP含完整源码、两个部署文件、两个脚本及可执行 JAR。
- 使用新 JAR，在随机空闲回环端口与独立临时 SQLite 目录启动：健康接口 UP、首页及其 JS/CSS 返回成功、easy 牌局创建成功且12张牌的答案全部隐藏。
- 验证完成后已停止进程并删除本轮自建临时数据库，没有使用或改动原实验数据库。
- v1五个交付物的 SHA-256 与本轮修改前完全一致，基线见 `v1-sha256-before.txt`。

产物：`20261021-memory-game6085-v2.zip`。

SHA-256：`ad99d1e6bdadaaa0783670d9a4dc350bd02c020d69ea7a87fb9cbb9c6bfdb570`。

详细结果：`validation.json`、`maven-package.log`、`backend-test-results.txt`、`smoke-startup.log`。

本包重新生成的是独立运行 JAR；Word 中的镜像摘要、容器标识、推送/拉取日志仍指原 Windows Docker 实验，并未声称本轮重新发布了该 JAR。
