# UI 与功能验证记录

日期：2026-10-21。使用 ui-ux-pro-max 本地技能设计、定向检索和审核。

## 已实现

- 源码：Code/memory-game6085/。
- 记忆花园，奶油白与森林绿，项目内植物 SVG 与统一 Lucide 图标。
- 6 / 8 / 12 对难度，服务端随机牌局、匹配、计时、暂停，SQLite 成绩榜。
- Vue 静态资源已打入 Spring Boot JAR，一个本地服务提供页面和接口。
- Docker 多阶段构建文件与命名数据卷配置，操作说明和真实截图清单。

## 审核后修正

- 压缩桌面牌桌高度，突出“开始翻牌”按钮。
- 加深辅助文本，以及提交成绩后高亮行的排名数字，修正实际测出的对比度问题。
- 原生 dialog、明显的键盘焦点、隐藏牌面不泄露答案、动态提示、音效默认关闭。
- 窄屏重排、挑战模式手机使用四列、减少动态效果。
- 榜单加载失败显示真实错误和重试入口；重开游戏先确认。
- 暂停保留翻牌状态，停止计时；恢复后继续配对和剩余翻回延迟。

## 验证结果

| 检查 | 结果 |
|---|---|
| npm run build | 通过 |
| Maven 后端测试 | 3 项通过，0 失败、0 错误 |
| Spring Boot 可执行 JAR 打包与启动 | 通过 |
| /api/health | UP，SQLite 可读 |
| 浏览器端到端测试 | 3 项全部通过 |
| 完整配对、暂停、昵称验证、保存榜单 | 通过 |
| 排行榜刷新、接口失败与重试 | 通过 |
| SQLite 服务重启 | 同一难度榜单完整内容与重启前一致 |
| 桌面 1440×1100 | 无横向溢出；axe 扫描 0 项违规 |
| 平板 768×1024 | 无横向溢出；axe 扫描 0 项违规 |
| 手机 375×812 | 无横向溢出；axe 扫描 0 项违规 |
| 横屏 812×375 | 无横向溢出；axe 扫描 0 项违规 |
| 小屏 320×740 | 无横向溢出；axe 扫描 0 项违规 |
| 规则弹窗、游戏中、暂停 | axe 扫描 0 项违规 |
| 成绩弹窗、保存后的排行榜 | 端到端测试内 axe 检查通过 |
| Compose 配置解析 | docker compose config --quiet 通过 |
| Maven Docker 基础镜像标签 | manifest inspect 可解析，OCI image index |
| raw/要求.png | SHA-256 与读取前一致 |

axe 使用 WCAG A / AA 相关自动规则；人工检查了真实页面截图。自动扫描通过不代表完整 WCAG 合规认证，未进行真人读屏全流程或多浏览器专项验证。

## 验证证据

- 后端：Code/memory-game6085/backend/target/surefire-reports/。
- 浏览器：Code/memory-game6085/frontend/tests/garden.spec.js 与 test-results/。
- UI：Code/memory-game6085/frontend/test-results/review/ui-audit.json 及真实页面截图。
- 测试成绩保存在独立 .qa/ 数据目录；交付运行实例使用 data/，未预置测试榜单。
- 原图 SHA-256：12C0240D5DCD5CFE16D4FF241FA28E113B3A5C3ECD8BB08C26DB8C05B7336B1A。

## 后续 Docker 验证（2026-10-21 更新）

- Docker Desktop 的 socket 启动故障已通过子进程独立运行时目录恢复，实际镜像构建、应用容器与健康检查已通过。
- 用户确认本机私有 Registry；真实 push、移除本地镜像后 pull、新容器挂载同一命名数据卷已完成，排行榜完整 JSON 前后一致。
- 真实终端与容器网页截图见 docs/docker-evidence/；正式 Word 已在确认大纲后生成，包含 11 张截图。

原始依据：raw/要求.png、用户确认的 6085 / 技术栈 / Code 目录要求。技术文档来源记录在 docs/source-notes.md。
