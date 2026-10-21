"""Package unmodified historical Docker evidence for the v2 report."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from hashlib import sha256
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/docker-evidence"
WORK = Path(__file__).resolve().parent
OLD = ROOT / "output/v1/20261021-docker-evidence-v1.zip"
DEST = WORK / "20261021-docker-evidence-v2.zip"

def digest(data):
    return sha256(data).hexdigest()

preserved = [ROOT / "raw/要求.png", *(ROOT / "output/v1").iterdir()]
before_hashes = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in preserved}
with ZipFile(OLD) as old:
    assert old.testzip() is None
    originals = [n for n in old.namelist() if n.endswith((".png", ".json"))]
    assert len(originals) == 12
    for name in originals:
        assert old.read(name) == (SOURCE / name).read_bytes(), name

files = sorted(set(originals + ["02-build-progress.png"] + [p.name for p in SOURCE.glob("*.txt")] + ["before-leaderboard.json", "after-leaderboard.json", "saved-score.json"]))
payload = {name: (SOURCE / name).read_bytes() for name in files}
data = {name: json.loads(payload[name].decode("utf-8-sig")) for name in files if name.endswith(".json")}
result = data["results.json"]
assert data["before-leaderboard.json"] == data["after-leaderboard.json"] == result["leaderboard"]
assert data["saved-score.json"] == result["leaderboard"]["scores"][0]
assert result["beforeContainerId"] != result["afterContainerId"]
assert result["leaderboardPreserved"] is True
for name in ["02-build.txt", "05-registry-push.txt", "07-registry-pull.txt"]:
    assert result["digest"] in payload[name].decode("utf-8-sig"), name
assert "BUILD SUCCESS" in payload["02-build.txt"].decode("utf-8-sig")
assert "LeaderboardPreserved=True" in payload["09-data-after.txt"].decode("utf-8-sig")

readme = """Docker 容器化实验原始证据包 v2
实验日期：2026-10-21；项目：memory-game6085；学号后四位：6085。

一、证据来源及范围
本包收录此前在 Windows 主机上实际执行 Docker 实验时采集的真实终端、浏览器截图、PowerShell transcript 和接口返回 JSON。v2 是对现有原始证据的补全整理，本次未重新执行 Docker 构建、推送、删除、拉取或容器重建。所有原始 PNG、TXT、JSON 均按原字节打包，未重绘、模拟或改写。

二、环境说明
实验沿用主机已有的 Docker Desktop 环境，使用 WSL2/Linux 引擎。已有过程记录说明：因遗留 socket 问题无法启动，后通过仅为 Docker Desktop 子进程使用独立 LOCALAPPDATA 运行时缓存目录恢复启动，系统级环境变量未修改。相关启动辅助脚本随 v2 源码包提供。
01-environment.png 和 01-environment.txt 证明恢复后的 Docker Client/Server、Compose 和项目命名可用；results.json 记录 WSL2 内核等环境信息。历史安装及首次配置截图资料未提供，本包不将版本检查画面描述为安装过程截图。

三、与 Word v2 的对应关系
Word 继续使用现有真实截图。图4改用新增收录的 02-build-progress.png，直接展示 Building jar、Spring Boot repackage、BUILD SUCCESS 和镜像导出。原 02-build.png 仍保留为补充证据。
图1：04-container-home.png
图2：01-environment.png
图3：05-container-completed.png
图4：02-build-progress.png
图5：03b-container-run.png
图6：05-registry-push.png
图7：06-remove-local.png
图8：07-registry-pull.png
图9：04-data-before.png
图10：08-run-pulled-image.png
图11：09-data-after.png
本包的日志与 JSON 用于检索和复核，不能替代作业要求的 Word 内嵌过程截图。

四、原始日志和数据
全部现存原始过程 TXT 日志已收入。其中 03-container-run.txt 记录最初端口冲突的失败尝试，03b-container-run.txt 是改为 18085 后的成功结果；勿将早期失败日志当作最终状态。
before-leaderboard.json、after-leaderboard.json 为重建前后完整榜单，saved-score.json 为提交成绩返回值；三者与 results.json 内对应记录一致。
镜像构建、推送、拉取使用同一摘要：
sha256:e4eb4cb25dd64d18b05daac257940e3f15115d2cbe62d5c748bc351cd7a15e66
新旧容器标识不同，继续挂载 memory-game6085-data 到 /app/data，完整榜单保持一致。

五、地址范围
镜像仓库：localhost:5000/memory-game6085:1.0.0，仅绑定本机回环地址；不构成公网仓库或异机拉取入口。
应用：原实验主机 http://localhost:18085，容器内部端口 8080。

六、完整性
manifest-sha256.json 列出本包各项原始证据及本说明的 SHA-256，便于解压后逐项核对。清单不包含自身摘要。
"""
payload["README.txt"] = readme.encode("utf-8")
manifest = {
    "version": "v2",
    "experimentDate": "2026-10-21",
    "sourceDirectory": "docs/docker-evidence/",
    "files": [{"name": name, "bytes": len(content), "sha256": digest(content)} for name, content in sorted(payload.items())],
}
payload["manifest-sha256.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
assert not DEST.exists(), f"Refusing to overwrite {DEST}"
with ZipFile(DEST, "x", ZIP_DEFLATED) as archive:
    for name, content in sorted(payload.items()):
        archive.writestr(name, content)
with ZipFile(DEST) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(payload)
    for name, content in payload.items():
        assert archive.read(name) == content, name
assert all(digest(p.read_bytes()) == before_hashes[str(p.relative_to(ROOT))] for p in preserved)
verification = {
    "archive": str(DEST.relative_to(ROOT)),
    "bytes": DEST.stat().st_size,
    "sha256": digest(DEST.read_bytes()),
    "entries": len(payload),
    "pngCount": len([n for n in payload if n.endswith(".png")]),
    "originalLogCount": len([n for n in files if n.endswith(".txt")]),
    "rawAndV1Unchanged": True,
    "allOriginalEntriesByteIdentical": True,
    "zipCRC": "passed",
    "digestConsistent": True,
    "leaderboardConsistent": True,
    "reportFigure4": "02-build-progress.png",
    "preservedHashes": before_hashes,
}
(WORK / "verification.json").write_text(json.dumps(verification, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(verification, ensure_ascii=False, indent=2))
