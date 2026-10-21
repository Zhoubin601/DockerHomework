# GitHub 提交记录

## 2026-10-21 v4 推送

- 用户明确授权“修改生成v4，然后推送”，目标沿用origin的Zhoubin601/DockerHomework，分支main。远端复核基线为14a2cbb，本地工作分支为work。
- 本次提交v3独立核查记录、v4五份正式交付物、README及新增报告生成／目录更新脚本、v4来源与验证记录、最终29页渲染及视觉检查记录。
- 不改写raw或v1—v3，不变更应用逻辑、唯一交付JAR和历史实验标签；v4预览沿用v3原字节。
- 工作副本ZIP/DOCX及早期渲染按新增规则忽略，保留本地文件；正式文件以output/v4为准，最终渲染仅作为docs核查记录。
- 推送前核对完整差异、常见凭据模式、文件大小和release-manifest；使用普通快进HEAD:main推送，完成后核对远端main与本地HEAD及五份交付物。

## 2026-10-21 v3 推送

- 用户在v3生成后明确要求“推送”，目标沿用项目origin：Zhoubin601/DockerHomework，远端分支main。
- 提交v3五份正式交付物、当前源码及预构建JAR、真实Linux补充实验截图和原始日志、报告生成及目录更新脚本、最终28页视觉检查图及验证记录。
- 保留raw、v1、v2的原字节；推送前重新核对release-manifest中的五份v3文件及11份旧文件基线。
- 新增v3本地工作副本和图形运行状态忽略规则：不提交重复ZIP/DOCX、早期渲染、进程PID或图形启动日志；文件仍保留在本地。
- 推送采用普通快进方式，不强制覆盖远端；完成后核对本地HEAD与远端main的提交标识以及v3五份交付物是否进入远端提交。

日期：2026-10-21。

## 2026-10-21 v2 更新提交

用户在 v2 交付后明确要求“提交至远端”。本轮目标为现有 origin 的 main 分支：
https://github.com/Zhoubin601/DockerHomework 。

- 推送前远端 main 与本地基线均为 `2a7be0c844975a68d95c47effd1be7ecbb0cfaf7`；当前工作分支名为 work，使用显式 `HEAD:main` 推送，不强制改写远端历史。
- 提交 v2 五个交付文件、README 与干净构建脚本修改、可复用报告修订脚本、v1复核与v2变更记录、最终渲染及验证记录。
- raw 与 output/v1 保持原字节；v2 文件与 release-manifest.json 核对。
- 新增针对 v2 重复打包副本及试排版图片的 Git 忽略规则；文件继续保存在本地。正式成品以 output/v2 为准，最终 render-release 图片与 PDF 作为检查记录入库。
- 沿用已有后端3项测试及隔离启动验证结果，不为本轮 Git 提交重新执行 Docker 实验。
- 提交前检查差异、暂存文件体积与常见凭据；推送后核对远端 main 与本地提交，以及 output/v2 是否进入远端提交。

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
