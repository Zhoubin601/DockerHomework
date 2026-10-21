# v1 实验证据独立复核

检查日期：2026-10-21。范围：`raw/要求.png`、`output/v1/20261021-docker-evidence-v1.zip`、`docs/docker-evidence/`。本轮只读核验既有证据，没有重新运行 Docker 实验，也没有修改 raw/ 或 output/。

## 结论

核心证据链基本满足原始图中的 Docker 构建、发布后拉取及过程截屏要求。没有发现摘要、镜像名、顺序、容器标识或成绩数据相互矛盾的问题。环境部署过程展示不足、Word 使用的构建图未显示 JAR 打包过程，仍应补强。

## 已直接验证

- ZIP `testzip()` 返回 None；内含 11 个 PNG、`results.json` 和 `README.txt`。全部 11 个 PNG 与结果 JSON 的字节均与 docs/docker-evidence 中对应文件相同。
- 直接查看了原始要求图，以及环境、构建结果、构建过程、push、移除、pull、重建后数据截图。截图内容与相应 transcript 一致。
- Docker 环境可用：`01-environment.txt:20` 的 `docker version` 返回 Client/Server 29.8.2、linux/amd64；`01-environment.txt:23` 有 Compose v5.6.0。
- Spring Boot 打包实际完成：`02-build.txt:594` 有 Building jar，`:596` 有 spring-boot:4.1.1:repackage，`:601` 有 BUILD SUCCESS，`:626` 有镜像 Built。
- 发布：`05-registry-push.txt:29` 为实际 push；`:41` 返回摘要 `sha256:e4eb4cb25dd64d18b05daac257940e3f15115d2cbe62d5c748bc351cd7a15e66`。
- 移除本地镜像：`06-remove-local.txt:25` 同时移除本地与仓库标签，`:28` 返回 Deleted，后续镜像列表为空；`:35` 明确保留数据卷。
- 拉取：`07-registry-pull.txt:20` 为 docker pull，`:27` 摘要与 build/push 一致，`:28` 返回 Downloaded newer image。
- 拉取后运行：`08-run-pulled-image.txt:20` 直接用仓库镜像启动新容器并挂载同一数据卷；`:28` 的完整新容器 ID 与 `04-data-before.txt:21` 原容器 ID 不同。
- 数据保留：原始 before-leaderboard.json 和 after-leaderboard.json 解析后完全一致（编号 1、6085实验、12 步、6950 ms）；`09-data-after.txt:31` 的完整 JSON 比较结果为 True，`:34` 挂载为 memory-game6085-data -> /app/data，`:38` 可见 garden.db。

## 修改建议

1. **提交前优先补强环境部署过程。** `01-environment.png` 能证明环境已经可用，不能展示 Docker Desktop 安装、WSL2 配置或启动恢复的过程。依据实际情况补部署/配置说明和真实截图；已安装则如实写沿用现有环境，不能补造历史安装画面。
2. **提交前优先补入现存打包截图。** `02-build.png` 仅显示镜像导出结果；`02-build-progress.png` 同时显示 JAR、repackage、BUILD SUCCESS 与镜像导出，但没有被纳入当前 v1 证据 ZIP。Word 补图后应同步更新证据包和图索引；保留 v1，另产 v2。
3. **可选增强可核查性。** 现证据 ZIP 的 README 如实说明它只包含 Word 中的 11 张图和结构化结果，因此未含 transcript 不构成错误；若制作 v2，可把对应原始 transcript 与 before/after 榜单 JSON 一并收入，便于核对长命令和完整摘要。该项不是原图强制要求。

## 范围边界

- 原图没有指定 Docker Hub、公开仓库或异机拉取。`localhost:5000` 的 push/pull 是有效的本机 Registry 发布/拉取实验，不能仅据“本机仓库”判不合格。若教师另有跨机器要求，才需要补做。
- 原图的“已有 SpringBoot 项目”是否专指以前课程项目，仅靠现有证据不能确定；不在本次证据审计中自行认定。
- 本轮核对的是留存日志与图像之间的一致性，没有据此声称重新复现了历史实验。
