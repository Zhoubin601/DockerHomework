# v4 独立证据与来源核查

日期：2026-10-21。范围：对既有 v3 真实实验材料做文档改版来源核查，不重新运行 Docker、不改写原始截图或日志。v4 为交付文档版本；Windows 镜像仍为 `1.0.0`，Linux 补充实验镜像仍为 `1.0.1-v3`。

## 首次资源创建截图

直接查看 `docs/v3-evidence/01-resource-creation.png` 后确认：适合原字节嵌入 Word，三条首次创建命令、资源名称及成功返回均完整可读：

```sh
docker network create --label course=memory-game6085-v3 memory-game6085-v3-net
docker volume create --label course=memory-game6085-v3 memory-game6085-v3-data
docker volume create --label course=memory-game6085-v3 memory-game6085-v3-registry-data
```

对应原始记录：`docs/v3-evidence/01-linux-config.txt` 第 16、19、22 行（以文件 LF 换行计数）。原始记录中的 `6085-v3$` 为终端命令显示前缀，不是命令参数。

图片顶部日期命令行略有裁切，不影响关键的创建操作及成功返回。建议在“环境配置验证”图之后添加此原图，图题可写“首次创建独立网络及数据卷（沿用平台 Docker 引擎）”。该图片不证明安装 Docker 引擎，也不能补作历史 Windows 安装或首次配置截图。

## 关键正文命令与结果的来源

以下命令及返回来自既有 transcript；正文可为排版换行，但必须保留实际参数、资源名称、端口和版本。命令文本用于改善阅读，截图继续保留为原始凭证。

### 容器运行页（v3 第 21 页）

来源：`docs/v3-evidence/03-container-run.txt` 第 5、7、9、11、13、15、17 行。

建议展示完整应用启动命令，以及健康检查和 JAR 一致性的简洁结果：

```sh
docker run -d --name memory-game6085-v3-app --network memory-game6085-v3-net -p 127.0.0.1:18086:8080 -e DATA_DIR=/app/data --mount type=volume,source=memory-game6085-v3-data,target=/app/data memory-game6085:1.0.1-v3
curl --fail --silent http://127.0.0.1:18086/api/health
docker exec memory-game6085-v3-app id
docker exec memory-game6085-v3-app sha256sum /app/app.jar
```

- 宿主机端口：`127.0.0.1:18086`；容器端口：`8080`。
- 健康结果：`status=UP`、`database=SQLite`、`application=memory-game6085`。
- 进程用户：`uid=999(garden) gid=999(garden)`。
- 交付 JAR 与容器 JAR 的 SHA256 均为：

```text
2e97ff46f2acfc1bfe0411a22f3f61a3ef4b8958e4ba5fff609d0350853852a0
```

原容器完整 ID：`263d322a4f4c7b1a2a211d61429d0e6ac18fb5e5fa77c5fb4f783871004577d1`。

### 发布页（v3 第 23 页）

来源：`docs/v3-evidence/04-registry-push.txt` 第 5、16、17、27–32 行。第 27 行含终端进度的 ANSI 控制码，引用其最终 digest 结果即可，不需把控制码移入 Word。

建议展示标记和发布命令：

```sh
docker tag memory-game6085:1.0.1-v3 localhost:15085/memory-game6085:1.0.1-v3
docker push localhost:15085/memory-game6085:1.0.1-v3
curl --fail --silent http://127.0.0.1:15085/v2/memory-game6085/tags/list
```

实际标签查询：`{"name":"memory-game6085","tags":["1.0.1-v3"]}`。

实际发布仓库摘要（与 `08-registry-pull.txt` 第 15 行的 pull 摘要相同）：

```text
sha256:fe814da12f1ebd9dbbfc85dcab5af55d9ef098b9261bc706f0df362746f78c85
```

Registry 只绑定本机 `127.0.0.1:15085`；不能写成公网发布或异机拉取。

### 重建验证页（v3 第 26 页）

来源：`docs/v3-evidence/09-recreate-verify.txt` 第 5、7、9、11、13、15–17 行；比较对象为 `before-leaderboard.json`、`after-leaderboard.json`、`before-container.txt`、`after-container.txt`。

建议展示从已拉取的仓库镜像重建命令：

```sh
docker run -d --name memory-game6085-v3-pulled --network memory-game6085-v3-net -p 127.0.0.1:18086:8080 -e DATA_DIR=/app/data --mount type=volume,source=memory-game6085-v3-data,target=/app/data localhost:15085/memory-game6085:1.0.1-v3
curl --fail --silent 'http://127.0.0.1:18086/api/leaderboard?difficulty=easy'
```

- 新容器完整 ID：`50fb7d90259a8f7b690edbd591711676d26021e46deacd99c72682293b5b2c91`。
- 容器前缀由 `263d322a4f4c` 变为 `50fb7d90259a`。
- 仍挂载 `memory-game6085-v3-data` 到 `/app/data`。
- 重建后 `/app/app.jar` 的 SHA256 与交付 JAR 相同。
- 完整榜单一致，比较输出为 `LeaderboardPreserved=True ContainerChanged=True`。
- 实际保留成绩：编号 `1`、昵称 `6085v3实验`、难度 `easy`、`11` 步、`7268 ms`；不要随 v4 文档改版更改此真实历史昵称。

镜像 ID 为 `sha256:cd0d87b180cc1916dea642a7d1d5b62988c943de635577dd44f1d0229aae43d9`，不同于上面的仓库摘要和 JAR 摘要，三者不可互换。

## 验收边界

- v4 可补上首次配置资源的 Word 内嵌截图，并改善长命令和关键结果的正文可读性。
- 平台已部署引擎及原 Windows 历史安装/首次配置截图缺失的事实不变，不得写成已补拍安装过程。
- 旧课堂项目、公开仓库或异机拉取的教师额外要求资料未提供。
- 此记录只做文件核查，未执行 Docker 构建、发布、删除、拉取或应用启动测试。

## 最终交付复核

最终独立核查已通过，详细数据见 `docs/v4-work/final-evidence-verification.json`。

- 待交付 Word：`docs/v4-report-work/20261021-docker-lab-report-v4.docx`。共有 21 张图且全部与既有原图逐字节一致；图 A1a 确实对应 `01-resource-creation.png`，图 A1b 确实对应 `01-config-review.png`，图题与图像关系正确。
- 证据 ZIP：77 项，CRC 通过；与 v3 条目集合一致，仅根目录 README 和 manifest 改动。其余 75 项原始内容保留，47 项 Linux 文件与 `docs/v3-evidence/` 原件一致；76 项摘要清单均通过。
- 源码/JAR ZIP：34 项，CRC 通过；与 v3 条目集合一致，仅 README 改动。唯一 JAR 原字节未改，JAR 内部 CRC 通过，摘要与工作区交付 JAR、原 Linux 两个容器的记录一致。
- Word 及源码包 README 保留 Linux 实验版本 `1.0.1-v3`，没有将真实实验标签改成 `1.0.1-v4`。
- 本复核只读取成品并新增核查记录，未重建或打包成品，未运行 Docker 或应用。
