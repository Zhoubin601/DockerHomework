表1：一 实验目的与任务要求
任务要求 | 本实验对应方式
项目名称包含学号后四位 | memory-game6085，学号后四位为 6085
Spring Boot 项目打包发布 | Windows多阶段构建见第五章；Linux配套JAR及镜像见附录A2—A3；10月22日本机复测见附录B1
发布后演示拉取 | Windows仓库localhost:5000见第六章；Linux仓库localhost:15085见附录A5—A8；本机15086见附录B1
全过程截图汇总 | Windows图1—11；Linux图A1a、A1b及A2—A9；本机重建后图B1，均嵌入本Word
Docker 环境部署与验证 | 沿用已装引擎；Windows启动验证见2.2，Linux资源配置见附录A1；10月22日本机复测见B1

表2：2.1 实验配置与项目目录
项目 | 本次实际配置
操作系统 | Windows 11 家庭版 中文版 64 位，10.0.26300
本地开发工具 | Java 21.0.11；Node.js 24.14.1；npm 11.11.0；Maven 3.9.16
应用技术栈 | Vue 3.5.44、Vite 7.3.7、Spring Boot 4.1.1、SQLite JDBC 3.53.4.0
Docker 环境 | Docker Desktop 4.95.0；Client / Server 29.8.2；Compose 5.6.0
构建与运行镜像 | Node 24；Maven 3.9.9 + Java 21；Temurin 21 JRE
源码目录 | Code/memory-game6085/
应用端口 | 宿主机 127.0.0.1:18085 → 容器 8080
镜像仓库 | 本机 Registry，127.0.0.1:5000
持久化目录 | memory-game6085-data → /app/data，数据库 garden.db

表3：3.2 SQLite 数据设计
字段 | 用途
game_id | 牌局唯一标识，防止同一局重复写入
nickname / difficulty | 玩家昵称与难度，按难度分别查询排行榜
moves / duration_ms | 服务端生成的步数与用时，作为排序依据
created_at | 成绩记录创建时间

表4：4.1 本地构建与自动验证
检查项目 | 结果
npm run build | 成功生成前端静态资源
后端测试 | 3 项通过，0 失败，0 错误
浏览器端到端测试 | 3 项全部通过
界面检查 | 1440、768、375、812 横屏及 320 宽度无横向溢出
数据保存 | 完成牌局后可提交昵称并进入对应难度榜单

表5：7.1 记录重建前的数据
对比项 | 重建前的实际值
容器标识前 12 位 | c247b7360b52
成绩编号 / 昵称 | 1 / 6085实验
步数 / 用时 | 12 / 6950 ms
数据卷 | memory-game6085-data

表6：八 实验结果与问题分析
实验环节 | 实际结果
Docker 环境 | Client / Server 正常，Linux 引擎可用
应用与镜像构建 | 前端构建、后端测试和 Spring Boot JAR 打包成功
容器运行 | 页面和 API 可访问，健康检查 UP
镜像发布 | 本机 Registry push 成功，可查询标签 1.0.0
镜像拉取 | 删除本地镜像后 pull 成功，摘要与推送一致
容器重建 | 新容器使用拉取镜像，容器标识与原容器不同
SQLite 数据卷 | 完整榜单对比一致，保存成绩保留
实验截图 | 真实终端窗口与容器浏览器页面均已采集

表7：9.1 原Windows实验截图来源索引
图号 | 内容 | 来源文件
1 | 容器首页 | 04-container-home.png
2 | 环境与项目命名 | 01-environment.png
3 | 容器中保存成绩 | 05-container-completed.png
4 | Spring Boot JAR 打包与镜像导出 | 02-build-progress.png
5 | 容器运行与健康检查 | 03b-container-run.png
6 | 本机仓库推送 | 05-registry-push.png
7 | 本地镜像移除 | 06-remove-local.png
8 | 从仓库重新拉取 | 07-registry-pull.png
9 | 重建前成绩 | 04-data-before.png
10 | 拉取镜像创建新容器 | 08-run-pulled-image.png
11 | 重建后榜单与数据卷 | 09-data-after.png

表8：A10 补充证据来源与版本对应
图号 | 内容 | 来源文件
A1a | 首次资源创建 | 01-resource-creation.png
A1b | 配置检查 | 01-config-review.png
A2 | JAR与镜像构建 | 02-build-review.png
A3 | 运行与JAR一致 | 03-container-run.png
A4 | 游戏成绩保存 | 05-game-saved.png
A5 | 本机仓库发布 | 04-registry-push.png
A6 | 本地镜像移除 | 07-remove-local.png
A7 | 仓库拉取 | 08-registry-pull.png
A8 | 重建与数据比较 | 09-recreate-verify.png
A9 | 重建后页面 | 10-after-recreate-ui.png

表9：B1 2026年10月22日本机验证
验证环节 | 本轮实际结果
源码与容器构建 | 本机Maven测试3/3；Dockerfile多阶段构建成功，复用BuildKit缓存。容器内BOOT-INF的61项与交付JAR一致。
浏览器与用户 | 实际容器Playwright 3/3；应用以garden普通用户运行，健康检查UP。
独立资源 | 应用18087；Registry 15086；资源前缀memory-game6085-localtest-20261022，未复用原实验数据卷。
镜像发布与拉取 | 标签localtest-20261022；push成功后移除本轮容器及两个本地标签；pull返回Downloaded newer image。
新旧容器 | 91b23f11f6da → cdb872c45267；同一命名数据卷，完整排行榜JSON一致。
真实测试成绩 | 测试花匠6085；easy；12步；9271 ms；记录1，仅为独立复测数据。