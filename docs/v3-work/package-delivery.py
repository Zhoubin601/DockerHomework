from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
import hashlib
import json

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'docs/v3-work'
CODE=ROOT/'Code/memory-game6085'
EVIDENCE=ROOT/'docs/v3-evidence'
sha=lambda b:hashlib.sha256(b).hexdigest()
baseline=json.loads((WORK/'baseline-sha256.json').read_text())
for name, record in baseline.items():
    assert sha((ROOT/name).read_bytes())==record['sha256'],name

# Preserve the independently useful v2 source selection, adding v3 deployment files.
with ZipFile(ROOT/'output/v2/20261021-memory-game6085-v2.zip') as seed:
    names=[n.split('/',1)[1] for n in seed.namelist() if not n.endswith('.jar')]
names+=['Dockerfile.prebuilt','scripts/package-prebuilt.ps1','frontend/scripts/v3-browser-evidence.mjs','dist-artifacts/SHA256SUMS','dist-artifacts/memory-game6085.jar']
source=WORK/'20261021-memory-game6085-v3.zip'
with ZipFile(source,'w',ZIP_DEFLATED) as z:
    for name in sorted(set(names)):z.write(CODE/name,'memory-game6085/'+name)
with ZipFile(source) as z:
    assert z.testzip() is None
    for name in z.namelist():assert z.read(name)==(CODE/name.split('/',1)[1]).read_bytes()
    jars=[n for n in z.namelist() if n.endswith('.jar')]
    assert len(jars)==1
    jb=z.read(jars[0])
    jar_sha=sha(jb)
    with ZipFile(BytesIO(jb)) as jar:
        assert jar.testzip() is None
        assets=[n for n in jar.namelist() if n.startswith('BOOT-INF/classes/static/assets/') and not n.endswith('/')]
        assert len(assets)==2
result=json.loads((EVIDENCE/'results.json').read_text())
assert jar_sha==result['jarSha256']==result['containerJarSha256']

entries={}
with ZipFile(ROOT/'output/v2/20261021-docker-evidence-v2.zip') as seed:
    for name in seed.namelist():entries['windows-original/'+name]=seed.read(name)
for p in sorted(EVIDENCE.iterdir()):
    if p.suffix in ['.png','.json','.sh','.py','.txt'] and '-pid.' not in p.name:
        entries['linux-v3/'+p.name]=p.read_bytes()
readme='''Docker作业 v3 证据说明

windows-original/ 原Windows实验凭证，来自v2证据包，字节未改。
linux-v3/ 2026-10-21真实Linux补充实验，使用平台已部署Docker，引擎28.4.0、Compose2.40.3。
本轮创建独立网络与数据卷，构建并运行配套JAR镜像、发布到本机15085端口Registry，
删除v3应用容器和本地镜像后拉取，使用同一数据卷创建新容器并校验完整榜单。

原Windows镜像版本1.0.0、应用端口18085、仓库5000；Linux补充版本1.0.1-v3、应用18086、仓库15085。
两者分别记录摘要及容器标识。本轮Linux截图不表示原Windows安装或首次配置过程。
本轮沿用已提供的Docker引擎，没有声称重新安装Docker。仓库地址仅在各自实验机器可访问。

Word正文图1至图11对应windows-original/，附录图A1至图A9对应linux-v3/。
01-linux-config.txt保存首次创建资源命令，01-config-review.png为随后实际复核的终端截图。
02-image-build.txt保存首次构建，02-build-review.png保存可复现的再次构建及交付JAR校验。
原始终端transcript含ANSI控制码，未将日志绘制为截图。PNG为真实终端窗口或浏览器像素采集。
results.json、before/after-leaderboard.json与saved-score.json记录实际结果，未虚构成绩。
日志和脚本中的路径反映实际执行工作区，迁移复现实验时需调整路径。

manifest-sha256.json列出本包除摘要清单自身以外每个条目的字节数和SHA256。
'''
entries['README.txt']=readme.encode('utf-8')
entries['manifest-sha256.json']=json.dumps({n:{'bytes':len(b),'sha256':sha(b)} for n,b in entries.items()},ensure_ascii=False,indent=2).encode()
evidence=WORK/'20261021-docker-evidence-v3.zip'
with ZipFile(evidence,'w',ZIP_DEFLATED) as z:
    for name,data in sorted(entries.items()):z.writestr(name,data)
with ZipFile(evidence) as z:
    assert z.testzip() is None
    m=json.loads(z.read('manifest-sha256.json'))
    for name,x in m.items():assert sha(z.read(name))==x['sha256'] and len(z.read(name))==x['bytes']
verification={'sourceZipEntries':len(names),'sourceZipSha256':sha(source.read_bytes()),'evidenceZipEntries':len(entries),'evidenceZipSha256':sha(evidence.read_bytes()),'jarSha256':jar_sha,'jarAssets':assets,'jarMatchesActualContainer':True,'baselineUnchanged':True,'zipCRC':'passed'}
(WORK/'package-verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(verification,ensure_ascii=False,indent=2))
