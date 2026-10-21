# Docker 实验过程记录

2026-10-21，用户确认先补齐实验再生成提交版报告；镜像仓库使用本机私有 Registry。

## 启动恢复

- 原 Docker Desktop 因 docker-secrets-engine/engine.sock 失效而退出。
- Move-Item / Rename-Item 原运行时目录均未成功；未删除原 socket。第一次 Move-Item 创建了一个空的备份目标目录，原目录仍在。
- 启动 Docker Desktop 子进程时，仅为该子进程设置 LOCALAPPDATA 为用户目录下 docker6085-runtime，绕开旧 socket；未修改系统级环境变量。
- 读取到原有自定义 WSL 数据目录为 E:/DockerData/DockerDesktopWSL，继续沿用。
- 恢复后 docker version 实际返回 Client 29.8.2 和 Server 29.8.2，Server 为 Docker Desktop 4.95.0、linux/amd64。
- 可复现启动脚本：Code/memory-game6085/scripts/start-docker-runtime.ps1。

## 证据方式

- 使用专用真实 Windows 控制台执行命令，并捕获该窗口实际像素。
- 终端截图及原始 transcript 放在 docs/docker-evidence/，截图不通过 HTML 或绘图工具模拟。
- 截图程序与实验命令文件位于 Code/memory-game6085/scripts/ 和 .qa/terminal-queue/。
- 后续按实际构建、运行、仓库 push/pull、容器重建结果追加记录。

## 实验完成

- 多阶段构建成功，镜像 memory-game6085:1.0.0，实际 Docker CLI 磁盘占用约 469 MB。
- 为避免占用已有课堂项目的 8080，宿主机改为 18085，容器内部仍为 8080。
- Registry 容器 memory-game6085-registry，127.0.0.1:5000。
- 真实容器内完成游戏并保存：6085实验，轻松，12 步，6950 ms，记录编号 1。
- push localhost:5000/memory-game6085:1.0.0 成功；删除本地两个实验镜像标签后 pull 成功。
- 推送、拉取摘要：sha256:e4eb4cb25dd64d18b05daac257940e3f15115d2cbe62d5c748bc351cd7a15e66。
- 原容器 c247b7360b52…；新容器 dd8b4bb17b50…；新容器直接使用拉取镜像。
- 两个容器使用同一数据卷 memory-game6085-data；完整排行榜 JSON 比较一致。
- 结构化事实及完整标识：docs/docker-evidence/results.json。
- 所有成功步骤均有真实终端截图，容器页面另有浏览器截图；03-container-run.png 是端口冲突的早期失败截图，不纳入正式报告。
