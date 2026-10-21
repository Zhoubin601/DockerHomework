# GitHub 提交记录

日期：2026-10-21。

用户明确要求：将当前项目根目录下的所有文件提交至 https://github.com/Zhoubin601/DockerHomework 。

## 提交范围

- 保留现有目录结构，提交 AGENTS.md、Code/ 中的源码与脚本、raw/ 原始要求、docs/ 过程资料、memory-bank/ 项目背景、output/v1/ 全部正式交付物。
- 保留项目原有 .gitignore 规则，不提交 node_modules、前端 dist、后端 target、运行数据库、.qa、test-results 和 playwright-report 等可重新生成的本地内容；可执行 JAR 已随 output/v1/ 的源码交付 ZIP 保存。
- 增加根目录 .gitignore，忽略环境凭据、操作系统临时文件和 Python 缓存。未删除本地文件。
- 正式 Word 与 raw/要求.png 保持原字节，未修改报告内容。

## 执行与验证

- 通过 GitHub 连接器核实仓库为空、默认分支为 main，当前账户有 push 权限。
- 原目录没有 Git 仓库；本轮初始化本地 main 分支并配置 origin。
- 使用本机已登录的 Git/GitHub 凭据，通过 Git 批量上传本地二进制与文本文件。
- 推送前检查暂存文件清单、单文件体积及常见凭据模式；不把凭据值写入文档。
- 推送后核对远端 main 的提交标识与本地 HEAD、工作区状态以及关键交付文件是否进入提交。
- 不在此次提交中重新构建应用或修订报告；此前报告复核建议仍见 docs/20261021-v1-report-review.md。

## 提交前核对结果

- 暂存区共 118 个文件，约 48.53 MiB，包含 output/v1/ 中全部 5 个交付文件；没有单文件超过 50 MiB。
- 对待提交文件及 ZIP/DOCX 内 81 个文本条目进行常见凭据模式扫描，未检出凭据模式。HTML 内嵌图片的 Base64 数据不作为文本密钥判断。
- raw/要求.png、正式 Word 的暂存内容与本地原文件逐字节一致，SHA-256 与既有验证记录相同。
- 原文件已有的空白格式提示未做改写，保留本次上传前的文件内容。
