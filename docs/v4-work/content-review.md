# v4 正文与验收范围独立复核

复核日期：2026-10-21。仅阅读报告、原始要求和既有证据，未改写 DOCX、未重跑 Docker 实验。

被查文件：`docs/v4-report-work/20261021-docker-lab-report-v4.docx`。本次读取时 SHA-256 为 `b994d30b27959cf9c6eec6446077be4f7cef66015b736571f9b1fed375db3ebd`。对照当前同目录 `render-final/20261021-docker-lab-report-v4.pdf`，共29页。

## 结论

正文内容复核通过。v3 审核指出的资源创建截图未入 Word、验收映射表只写 Windows、若干长命令只在终端截图中等问题已落实修订；没有发现需要阻止本轮交付的内容问题。

## 实际检查

- 重新对照 `raw/要求.png`。原图要求 Docker 环境、已有 Spring Boot 项目、项目名末尾学号四位、打包发布、发布后拉取、过程截图汇总一个 Word；原图未要求公开仓库、异机拉取或特定操作系统。
- 第3页验收表已同时映射 Windows 和 Linux 两轮实验，列出各自仓库及附录位置，环境一栏明确写为沿用已装引擎。
- 第19页图A1a为已有的首次网络及数据卷创建原图；第20页图A1b为之后的配置检查。通过 DOCX 嵌入图片关系直接核对，`01-resource-creation.png` 的 SHA-256 为 `ad191a1c8b4d93af6a701671a236f06e6cab9501b042bd02106e654ff4ae26d7`，在 DOCX 中出现一次且原始字节一致。全篇图片引用21张。
- 第19页新增资源创建命令，去除反斜杠续行并按 shell 参数解析后，与 `docs/v3-evidence/01-linux-config.sh` 的三条真实创建命令完全相同。
- 第22页A3中应用运行、健康检查、容器 JAR 摘要命令，与 `03-container-run.sh`、`03-container-run.txt` 对应；容器名、网络、数据卷、18086端口及镜像 `1.0.1-v3` 一致。
- 第24页A5中 tag、push 和仓库标签查询命令，与 `04-registry-push.sh`、`04-registry-push.txt` 对应；15085端口及标签一致。
- 第27页A8中拉取镜像重建和容器 JAR 摘要命令，与 `09-recreate-verify.sh`、`09-recreate-verify.txt` 对应；使用同一数据卷，重建名称为 `memory-game6085-v3-pulled`。
- JAR SHA-256 `2e97ff46f2acfc1bfe0411a22f3f61a3ef4b8958e4ba5fff609d0350853852a0`、仓库摘要 `sha256:fe814da12f1ebd9dbbfc85dcab5af55d9ef098b9261bc706f0df362746f78c85`、容器前缀 `263d322a4f4c` / `50fb7d90259a`、11步 / 7268ms成绩，与 `docs/v3-evidence/results.json` 和原始日志一致。
- 第29页明确写明“v4为报告与交付资料修订，未更改应用JAR、镜像标签或实验结果”；原 Windows `1.0.0` 与 Linux `1.0.1-v3` 没有被改写成虚构的 v4 实验或新镜像。历史昵称 `6085v3实验`、资源名中的 v3 及证据目录 `docs/v3-evidence` 均恰当保留。
- 第29页截图来源索引含A1a及A1b，编号与新增正文一致。

## 保留的事实边界

第20页明确说明两轮沿用已安装 Docker，引擎安装全过程、原 Windows 安装/首次配置/启动恢复的历史操作截图未附。该表述与现有资料一致，没有将 Linux 资源创建当作 Docker 安装，也没有冒充 Windows 历史记录。本轮保留这项边界并完成已授权的资料修订，无需以无法补拍历史过程为由阻止交付。

教师若另行明确限定旧课堂项目、公开仓库、异机拉取或安装截图，需按新的明确要求补充；现有原图没有这些额外规定。

本记录负责正文真实性和范围复核；完整逐页视觉检查、ZIP和最终发布文件检查由配套记录承担。
