# v7 远端继续工作交接

> 后续状态：用户已改为要求在本机完成。本轮 01—11 阶段、Word 补图及交付均已完成，最新状态见 [v7 本机交付记录](20261022-v7-changes.md)。以下内容保留为交接提交时的历史快照，不能作为当前未完成清单。

用户于2026-10-22明确要求：提交至远端仓库，剩余工作在远端完成。本次提交是工作交接，不是v7正式交付完成。

## 最重要的事实

- `output/v6/memory-game6085.docx` 是当前被检查的实际文件，18页11图6表。第3页称附录A/B截图全部嵌入，实际附录不存在；第4/5页也有失效引用。详细依据在 `20261022-v6-submission-review.md`。
- `docs/v6-report-work/20261022-docker-lab-report-v6.docx` 是之前制作的31页22图版本，作为历史恢复来源保留，不要把它的验收结果当作当前output/v6结果。
- 用户授权清除失效引用、补充Docker安装、首次配置、资源创建和配置截图。沿用九章正文，拟在v7新增明确标注日期和环境的补充附录，原v6保留。
- **Word尚未修改；v7正式Word尚未生成。04—11阶段脚本尚未运行或验证，不能将脚本存在描述为实验已完成。**

## 已完成的真实补充实验

本机新建隔离Ubuntu 24.04环境，在其中实际安装Docker Engine。没有挂载宿主机Docker socket，没有重装Windows Desktop。记录的安装是2026-10-22补做的Linux实验，不是原Windows历史安装。

容器：`memory-game6085-v7-install-20261022`，hostname `docker-lab6085`。使用privileged是为了后续启动嵌套引擎；外层端口为 `127.0.0.1:18089 -> 18085`，不复用原实验端口。

| 阶段 | 实际状态 | 证据 |
|---|---|---|
| 01 安装前 | 完成，确认docker/dockerd和socket不存在 | 01脚本、txt、result.json、1张日志窗口截图 |
| 02 官方源 | 完成，依赖、GPG密钥、noble stable源和apt update成功 | 02脚本、txt、result.json、2张日志截图、完整apt日志 |
| 03 安装Engine | 完成，退出码0 | 03脚本、txt、result.json、2张日志截图、03-apt-install-full.log |

实际版本：Docker CE/CLI `29.9.2`，Compose `5.6.1`，Buildx `0.38.1`，containerd.io `2.4.2`。安装脚本使用官方APT源的当时稳定版本；远端重新执行时版本可能变化，报告必须以远端真实输出为准。

已采集5张PNG均在 `docs/v7-work/`。这些是**实际命令日志在浏览器中显示后的截图**，不是伪装的安装向导或历史终端界面；完整原日志和命令脚本同步保留。新增报告须准确说明这一形式。

## 远端环境不能自动继承

Git提交不会搬运本机Docker容器、已安装的软件、宿主机端口或运行状态。本机安装容器目前保留；首次配置和dockerd启动尚未执行。

本机曾执行 `docker save` 导出 `eclipse-temurin:21-jre-jammy`、`registry:3`、`hello-world:latest` 到 `docs/v7-work/base-images.tar`，并复制到隔离容器 `/lab/base-images.tar`。该123,651,584字节镜像运输包超过GitHub普通文件限制，**不提交Git**；它不是截图证据，可在远端重新导出或改为实际pull。配套JAR和 `Dockerfile.prebuilt` 也已复制到本机隔离容器 `/lab/`，远端需要重新复制。

## 远端执行顺序

1. 先阅读AGENTS.md、本交接和v7计划，检查远端Docker权限。新建干净Ubuntu容器以记录完整过程，不将既有环境冒称全新安装。若远端不支持privileged嵌套引擎，应记录限制并改用真实独立Linux/VM环境，不能伪造截图。
2. 在可用Linux终端按实际路径执行以下准备。容器名可通过 `GARDEN_INSTALL_CONTAINER` 环境变量传给run-stage.py；默认名与本机相同。阶段脚本位于 `docs/v7-work/`，运行器只把对应脚本复制到 `/lab`，然后执行并记录退出码。

```bash
docker run -d --name memory-game6085-v7-install-20261022 \
  --hostname docker-lab6085 --privileged \
  -p 127.0.0.1:18089:18085 ubuntu:24.04 sleep infinity
python docs/v7-work/run-stage.py 01-before-install
python docs/v7-work/run-stage.py 02-official-repository
python docs/v7-work/run-stage.py 03-install-engine
```

同名证据是本机实测来源，远端新实测应在新子目录或新版本留存，勿覆盖本轮原始PNG/日志。复用运行器时先复制阶段脚本和run-stage.py到新证据目录。

3. 准备基础镜像、registry、hello-world后导出/导入（或改用真实pull），复制交付JAR与Dockerfile.prebuilt，再执行04配置、05 hello-world验证、06资源创建、07配套JAR镜像构建、08启动容器。04使用vfs存储以适配嵌套环境，具体启动参数须按实际日志调整；尚未验证可运行性。
4. **在08和09之间**，通过 `http://127.0.0.1:18089` 完成一局轻松模式并保存真实成绩，记录浏览器截图和返回JSON。否则后面的空排行榜比较没有数据持久化验证价值。09脚本含nickname非空检查。
5. 执行09 push、10删除本地两个标签后pull、11新容器重建和完整榜单比较。11后再采集实际浏览器榜单截图。所有执行成功后再形成结论。
6. `capture-logs.cjs` 读取真实txt并进行浏览器截屏，可用 `PLAYWRIGHT_MODULE_PATH` 指定playwright模块，`PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` 指定浏览器；Windows默认Edge，Linux默认Playwright Chromium。运行环境路径不能原样套用本机Windows路径。
7. 修改Word所有旧附录引用和第3页对应表，使用实际存在的新章节/图号；将安装前、官方源、安装、首次配置、启动验证、网络/数据卷/Registry创建、应用配置等图嵌入同一个Word。正文原11图保留，Windows历史和本轮Linux补做分开叙述。
8. 用对应技能制作候选，更新目录页码、严格校验并逐页渲染检查。检查通过后才写入 `output/v7/`。沿用源码包原字节即可，用户最终只计划提交源码ZIP及一个Word。

## 文件与验证

正式来源：`raw/要求.png`；当前交付基底：output/v6两文件；已有可恢复截图：v5证据ZIP及v5/历史v6 Word。只使用可追溯实测，禁止用图像生成、重绘或替换文本来制造实验截图。

本机已尝试documents技能的render_docx.py，失败原因为Windows未安装LibreOffice soffice.exe，不是Word文件损坏。此前用本机Word COM只读副本导出PDF检查通过；远端可使用可用的LibreOffice或Word，遵守渲染后逐页检查。

外部依据：Docker官方Ubuntu安装文档 <https://docs.docker.com/engine/install/ubuntu/>（引用2026-10-22）。静态二进制安装文档仅曾用于方案核对，实际采用APT安装。

提交范围包含当前v6及检查/过程文档、v7脚本、已经完成的真实日志截图；不提交本机镜像tar或敏感运行配置。工作区已有v1—v4文件删除以及v5 Word修改，不属于本轮补图操作，本次不暂存这些历史成品差异，也不恢复用户已删除的本地文件。
