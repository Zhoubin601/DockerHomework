# 项目背景

- 用户于 2026-10-21 确认：学号后四位为 `6085`。
- 根据 `raw/要求.png`，Spring Boot 项目名称末尾需加学号后四位，后续按 `6085` 处理。
- 用户已确认新建轻量小游戏，技术栈 Vue3 + Vite + Spring Boot + SQLite，用 SQLite 持久化成绩。
- 所有应用源码放在根目录 `Code/`，当前项目为 `Code/memory-game6085/`。
- 用户要求使用 ui-ux-pro-max 美化与审核 UI。
- 用户允许仅查官方技术文档；本轮未授权向外部镜像仓库推送。
- 当前应用已实现并完成本地构建、后端 / 浏览器测试、SQLite 服务重启持久化验证和 UI 审核。详细证据见 docs/ui-review.md。
- Docker 启动故障已解决，完成实际构建、本机私有 Registry 推送、删除本地镜像后拉取及新容器数据卷持久化验证。
- 用户确认九部分报告大纲，要求先完成真实 Docker 实验再制作提交版。报告及证据在 output/，完整过程见 docs/docker-experiment-notes.md。
- 实验应用使用宿主机 18085 端口，当前容器为 memory-game6085-pulled；仓库使用回环地址 5000。原有课堂项目的 8080 端口保持不变。
