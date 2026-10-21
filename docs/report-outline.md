# Docker 实验报告大纲

题目：Spring Boot 小游戏 Docker 容器化实验报告。

状态（2026-10-21 更新）：用户已确认九部分大纲、身份信息和本机私有 Registry；下面保留最初拟稿时的缺口作为过程记录，这些缺口现均已补齐。正式报告已按实际成功结果更新，共 15 页、11 张真实截图，位于 output/20261021-docker-lab-report-v1.docx。

原始要求：raw/要求.png；项目：Code/memory-game6085/；学号后四位：6085。

## 封面

课程《2026云计算技术与架构》、项目名称、实验日期、学号后四位。姓名、班级、完整学号资料未提供，不编造。

## 正文结构

1. 实验目的与任务要求：Docker 环境、Spring Boot 镜像、发布与拉取、截图提交。
2. 实验环境与项目结构：本机实际版本、Vue3 + Vite + Spring Boot + SQLite、Code 目录。
3. 系统设计与持久化：前后端整合、服务端牌局逻辑、SQLite 成绩表、数据卷设计。
4. 本地构建与功能验证：构建命令、健康检查、真实页面截图、已通过的后端与浏览器测试。
5. Docker 镜像构建与运行：实际 Dockerfile 与 Compose；引擎未运行的状态与拟执行命令必须区分。
6. 镜像发布与拉取：待提供仓库账户，未实际推送和拉取；列出命令及需补的真实截图。
7. 数据持久化验证：已完成的 Java 服务重启验证；容器重建验证尚未完成，不混写。
8. 实验结果与问题分析：已完成与未完成矩阵、本机 Docker socket 错误、后续补齐步骤。
9. 参考资料与截图清单：原始要求、已查阅的官方文档、每张图的来源。

## 现有证据

- output/20261021-memory-game6085-desktop-v1.png。
- Code/memory-game6085/frontend/test-results/review/playing.png。
- Code/memory-game6085/frontend/test-results/desktop-completed.png（独立自动测试实例，昵称和成绩为真实测试数据）。
- 后端测试记录、浏览器测试记录、SQLite 重启前对比记录、UI 审核 JSON。

## 关键缺口

- Docker Client 和 Server 同时可用的真实终端截图。
- Docker 镜像构建、容器运行、推送、拉取成功的真实终端截图。
- 容器重新创建前后的成绩对比截图。
- 姓名、班级、完整学号；镜像仓库账户；大纲确认。

大纲未确认及关键实验未完成时，Word 过程稿仅放 docs/，不作为 output/ 的正式提交文件。
