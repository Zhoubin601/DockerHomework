# v5 配套包制作与验证记录

日期：2026-10-22。此目录为过程工作区；`packages/` 是等待 Word 报告一起验收的候选文件，尚未复制到 `output/`。

## 输入与范围

- `output/v4/20261021-memory-game6085-v4.zip`：上版源码和唯一可执行 JAR。
- `output/v4/20261021-docker-evidence-v4.zip`：上版 Windows 原实验与 Linux 补充实验的全部原件。
- `docs/local-test-20261022/`：本轮真实本机源码构建、交付 JAR 浏览器及 UI 检查、Docker 发布与删除后拉取、独立数据卷持久化结果。
- `Code/memory-game6085/README.md`：本轮交付说明修订。本任务不修改应用源码、部署配置、JAR、`raw/` 或历史 `output/`。

本轮没有查阅新的外部资料。原始作业要求仍来自 `raw/要求.png`；本记录只描述打包，不增加原图未规定的评分条件。

## 确切变动

源码包仍为 34 项，仅 `memory-game6085/README.md` 更新为 v5 说明；其余 33 项与 v4 逐字节一致。JAR 摘要保持 `2e97ff46f2acfc1bfe0411a22f3f61a3ef4b8958e4ba5fff609d0350853852a0`。README 区分 2026-10-21 Windows `1.0.0`、Linux `1.0.1-v3`、2026-10-22 本机 `localtest-20261022` 三轮事实，说明 18087 / 15086 端口、缓存复用及两个 JAR 的 61 项 `BOOT-INF/` 一致、整包摘要不同。

证据包共 132 项。Windows、Linux 历史目录不变。v4 根 README 和旧根清单各自原字节存入 `history-v4/`；新根 README 和摘要清单更新。v4 的 77 个原件均有逐字节保留检查；新增的 53 份真实本机日志、JSON、PNG 和脚本从 `docs/local-test-20261022/` 按明确白名单直接读取，来源逐项记录于 `package-validation.json`。新清单覆盖除清单自身外的 131 项。

没有放入运行数据库、Docker 镜像中提取的重复 JAR、完整原有/最终容器清单或完整镜像 inspect；`docker-roundtrip.log` 因末尾含与本作业无关的课堂容器信息未入包，相应单步原始命令日志及归一化前后 JSON 保留。没有修改原始日志或把文本绘制为截图。

v5 桌面、手机预览分别为 `docker-roundtrip/browser-before/desktop-ready.png` 和 `mobile-ready.png` 的直接字节副本。这两张图均于 2026-10-22 本轮新建独立测试容器中采集，处于 push / pull 重建前；重建后的真实榜单图另以 `after-recreate-ui.png` 收入证据包，未混淆采集阶段。

## 验证

运行 `python docs/v5-work/build-v5-packages.py` 可重建候选 ZIP 和预览。脚本固定成员顺序、2026-10-22 的 ZIP 时间戳及压缩参数。连续两次运行产生完全相同的四个候选文件摘要，详见 `package-reproducibility.json`。

两份 ZIP 的 CRC、唯一成员名、完整载荷回读均通过。证据包 131 项大小 / SHA-256 清单全部通过；53 份新证据与来源字节相同；源码包只改 README 的断言通过。120 个文本成员的常见密码、私钥、Token 模式扫描未发现命中；PNG 原件用摘要追溯。

| 候选文件 | SHA-256 |
| --- | --- |
| `20261022-memory-game6085-v5.zip` | `1bfbf5399a7344ebc78f874b30c8e97dc52d9f111740437244417d296b05964c` |
| `20261022-docker-evidence-v5.zip` | `35455609c9a986f1bc448794140d05053e9a032354a9027cf6124a7be5ec82b3` |
| `20261022-memory-game6085-desktop-v5.png` | `9b2455fd4982a04dd3f8c3b6a7e80a0193df6377323e2423196e90fbb1e2fd00` |
| `20261022-memory-game6085-mobile-v5.png` | `7ee823e8976e292d740ca533acf63df196c35608984dd22e5af07b5fe8a7272a` |

## 交接

这四份候选等待主任务完成 Word 修复和全套验收后，由主任务复制进 `output/v5/`，不覆盖 v1—v4。此子任务没有执行 git add、commit 或 push。

教师是否另有原图以外的限定，以及未提供的原 Windows 安装 / 首次配置全过程截图仍由主任务按已有口径说明，不编造历史凭证。
