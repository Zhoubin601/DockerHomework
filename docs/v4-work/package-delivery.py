"""Prepare v4 delivery archives without changing the v3 experiment evidence."""

from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "docs/v4-work"
CODE = ROOT / "Code/memory-game6085"
V3 = ROOT / "output/v3"


def sha(data):
    return hashlib.sha256(data).hexdigest()


baseline = json.loads((WORK / "baseline-sha256.json").read_text(encoding="utf-8"))
for name, record in baseline.items():
    assert sha((ROOT / name).read_bytes()) == record["sha256"], name

source = WORK / "20261021-memory-game6085-v4.zip"
with ZipFile(V3 / "20261021-memory-game6085-v3.zip") as seed:
    assert seed.testzip() is None
    names = seed.namelist()
    assert len(names) == len(set(names))
    old_source = {name: seed.read(name) for name in names}

new_source = {}
for name in names:
    assert name.startswith("memory-game6085/") and ".." not in Path(name).parts
    relative = name.split("/", 1)[1]
    data = (CODE / relative).read_bytes()
    if relative != "README.md":
        assert data == old_source[name], f"Unexpected source change: {name}"
    new_source[name] = data
assert "v4" in new_source["memory-game6085/README.md"].decode("utf-8")
with ZipFile(source, "w", ZIP_DEFLATED) as archive:
    for name, data in sorted(new_source.items()):
        archive.writestr(name, data)

jar_names = [name for name in new_source if name.endswith(".jar")]
assert jar_names == ["memory-game6085/dist-artifacts/memory-game6085.jar"]
jar_bytes = new_source[jar_names[0]]
jar_hash = sha(jar_bytes)
assert jar_bytes == old_source[jar_names[0]]
with ZipFile(BytesIO(jar_bytes)) as jar:
    assert jar.testzip() is None
    assets = [
        name for name in jar.namelist()
        if name.startswith("BOOT-INF/classes/static/assets/") and not name.endswith("/")
    ]
    assert len(assets) == 2

with ZipFile(V3 / "20261021-docker-evidence-v3.zip") as seed:
    assert seed.testzip() is None
    old_evidence = {name: seed.read(name) for name in seed.namelist()}
entries = {name: data for name, data in old_evidence.items() if name != "manifest-sha256.json"}
entries["README.txt"] = """Docker作业 v4 证据说明

v4是报告与交付资料修订版本，本轮没有重新执行Docker实验，也没有重新采集UI。
windows-original/ 保留原Windows实验凭证，来自v3证据包，文件名和字节均未改。
linux-v3/ 保留2026-10-21的真实Linux补充实验，文件名和字节均未改。
该轮使用平台已部署Docker，引擎28.4.0、Compose2.40.3，创建独立网络与数据卷，
构建并运行配套JAR镜像、发布到本机15085端口Registry，删除v3应用容器和本地镜像后拉取，
使用同一数据卷创建新容器并校验完整榜单。

原Windows镜像版本1.0.0、应用端口18085、仓库5000；Linux补充版本1.0.1-v3、应用18086、仓库15085。
两者分别记录摘要及容器标识。v4没有新建镜像版本，也未将Linux截图用作原Windows安装凭证。
Linux实验沿用平台已提供的Docker引擎，没有声称重新安装Docker；仓库地址仅在各自实验机器可访问。

v4 Word内共21张图：正文图1至图11对应windows-original/，附录图A1a、A1b和A2至A9对应linux-v3/。
图A1a对应01-resource-creation.png，展示实际资源创建；图A1b对应01-config-review.png，展示随后配置验证。
01-linux-config.txt保存首次创建资源命令。A2至A9沿用原图号及来源，不因A1拆分而重新编号。
02-image-build.txt保存首次构建，02-build-review.png保存实际再次构建及交付JAR校验。
原始终端transcript含ANSI控制码，未将日志绘制为截图。PNG为真实终端窗口或浏览器像素采集。
results.json、before/after-leaderboard.json与saved-score.json记录该轮实际结果，未虚构成绩。
日志和脚本中的路径反映当时执行工作区，迁移复现实验时需调整路径。

源码包的唯一JAR沿用v3原始字节，其SHA-256与linux-v3/results.json中的交付JAR、容器JAR一致。
v4桌面和手机预览沿用v3交付PNG原始字节，UI未修改，不表示v4重新采集了页面。
本证据包相对v3仅更新根README.txt与manifest-sha256.json。
manifest-sha256.json列出本包除摘要清单自身以外每个条目的字节数和SHA256。
""".encode("utf-8")
result = json.loads(entries["linux-v3/results.json"])
assert jar_hash == result["jarSha256"] == result["containerJarSha256"]
for name in ("linux-v3/01-resource-creation.png", "linux-v3/01-config-review.png"):
    assert name in entries
entries["manifest-sha256.json"] = (
    json.dumps(
        {name: {"bytes": len(data), "sha256": sha(data)} for name, data in sorted(entries.items())},
        ensure_ascii=False, indent=2,
    ) + "\n"
).encode("utf-8")

evidence = WORK / "20261021-docker-evidence-v4.zip"
with ZipFile(evidence, "w", ZIP_DEFLATED) as archive:
    for name, data in sorted(entries.items()):
        archive.writestr(name, data)

with ZipFile(source) as archive:
    assert archive.testzip() is None
    assert set(archive.namelist()) == set(old_source)
    for name, data in new_source.items():
        assert archive.read(name) == data
source_changes = sorted(name for name in new_source if new_source[name] != old_source[name])
assert source_changes == ["memory-game6085/README.md"]
with ZipFile(evidence) as archive:
    assert archive.testzip() is None
    assert set(archive.namelist()) == set(old_evidence)
    manifest = json.loads(archive.read("manifest-sha256.json"))
    assert set(manifest) == set(archive.namelist()) - {"manifest-sha256.json"}
    for name, record in manifest.items():
        data = archive.read(name)
        assert sha(data) == record["sha256"] and len(data) == record["bytes"]
    for name, data in old_evidence.items():
        if name.startswith(("windows-original/", "linux-v3/")):
            assert archive.read(name) == data
evidence_changes = sorted(name for name in entries if entries[name] != old_evidence[name])
assert evidence_changes == ["README.txt", "manifest-sha256.json"]

preview_sources = {}
for viewport in ("desktop", "mobile"):
    preview = V3 / f"20261021-memory-game6085-{viewport}-v3.png"
    preview_sources[viewport] = {"source": str(preview.relative_to(ROOT)), "sha256": sha(preview.read_bytes())}

for name, record in baseline.items():
    assert sha((ROOT / name).read_bytes()) == record["sha256"], name
verification = {
    "sourceZipEntries": len(new_source),
    "sourceZipSha256": sha(source.read_bytes()),
    "sourceChangesFromV3": source_changes,
    "evidenceZipEntries": len(entries),
    "evidenceZipSha256": sha(evidence.read_bytes()),
    "evidenceChangesFromV3": evidence_changes,
    "allOriginalEvidencePreserved": True,
    "jarSha256": jar_hash,
    "jarUnchangedFromV3": True,
    "jarAssets": assets,
    "jarMatchesRecordedV3Container": True,
    "dockerExperimentRerun": False,
    "baselineUnchanged": True,
    "zipCRC": "passed",
    "previewsToReuse": preview_sources,
}
(WORK / "package-verification.json").write_text(
    json.dumps(verification, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(verification, ensure_ascii=False, indent=2))
