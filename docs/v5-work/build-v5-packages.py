"""Build v5 ZIP/PNG candidates from immutable v4 packages and real 2026-10-22 evidence.

Run from anywhere: python docs/v5-work/build-v5-packages.py
Only writes this directory's packages/ and package-validation.json; never output/ or raw/.
ZIP timestamps and member ordering are fixed so identical inputs reproduce identical ZIP bytes.
"""
from pathlib import Path
import hashlib
import io
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
DEST = WORK / 'packages'
LOCAL = ROOT / 'docs/local-test-20261022'
DATE = (2026, 10, 22, 0, 0, 0)
DEST.mkdir(exist_ok=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def load_zip(path):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None, f'Bad input CRC: {path}'
        assert len(z.namelist()) == len(set(z.namelist()))
        return {n: z.read(n) for n in z.namelist()}


def write_zip(path, members):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(members):
            assert not name.startswith('/') and '..' not in Path(name).parts
            info = zipfile.ZipInfo(name, DATE)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, members[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    actual = load_zip(path)
    assert actual == members
    return {'entries': len(actual), 'crcValid': True, 'bytes': path.stat().st_size,
            'sha256': sha(path.read_bytes())}


source_input = ROOT / 'output/v4/20261021-memory-game6085-v4.zip'
evidence_input = ROOT / 'output/v4/20261021-docker-evidence-v4.zip'
source = load_zip(source_input)
old_source = source.copy()
source['memory-game6085/README.md'] = (ROOT / 'Code/memory-game6085/README.md').read_bytes()
changed = [n for n in source if source[n] != old_source[n]]
assert changed == ['memory-game6085/README.md']
assert len(source) == 34
jar = source['memory-game6085/dist-artifacts/memory-game6085.jar']
assert sha(jar) == '2e97ff46f2acfc1bfe0411a22f3f61a3ef4b8958e4ba5fff609d0350853852a0'
source_path = DEST / '20261022-memory-game6085-v5.zip'
source_result = write_zip(source_path, source)

evidence = load_zip(evidence_input)
old_evidence = evidence.copy()
evidence['history-v4/README.txt'] = evidence['README.txt']
evidence['history-v4/manifest-sha256.json'] = evidence.pop('manifest-sha256.json')
evidence['README.txt'] = '''Docker作业 v5 证据说明（2026-10-22）

v5修复报告结构并补入本机真实复测记录。原Windows和Linux两轮实验不改写：
windows-original/ 为2026-10-21原Windows实验：镜像1.0.0，应用18085，Registry5000。
linux-v3/ 为2026-10-21 Linux补充实验：镜像1.0.1-v3，应用18086，Registry15085。
这两个目录的全部文件均与v4证据ZIP逐字节一致；v4顶层README和摘要清单的原件
另外存于history-v4/，不覆盖历史说明，且不把原说明中的v4结论当作v5现状。

windows-localtest-20261022/ 为2026-10-22用户恢复Docker Desktop后的真实本机复测。
Docker Client/Server29.8.2；源码镜像标签localtest-20261022；应用18087、Registry15086。
原始源码构建日志显示BuildKit缓存复用；不声称在容器内重新执行Maven测试。
本机源码干净构建成功、后端3项测试通过；实际交付JAR的浏览器3项测试通过，
8个UI自动审核场景通过；独立Docker容器上的浏览器3项测试通过。
实际push、移除本轮应用容器和两个镜像标签、确认标签不存在、pull、创建新容器，
完整榜单一致；推送/拉取目标仓库digest一致。详见results.json及对应原始命令日志。
本轮使用独立数据卷，没有把测试成绩混入原作业数据库；新容器页面无pageerror。

交付JAR继续沿用v4原字节，SHA256为
2e97ff46f2acfc1bfe0411a22f3f61a3ef4b8958e4ba5fff609d0350853852a0。
源码镜像内JAR的整包SHA256为
6126a1faf7e80ec948c5be2b50d834c7f3a4ef9f65089fcd49431f532a1b1389。
两个整包摘要不同，但BOOT-INF下61项的应用、资源和依赖内容完全相同，
参见source-image-vs-delivery.json；未把ZIP元数据差异称为应用内容变更。

本轮browser-before/的desktop-ready.png与mobile-ready.png就是v5独立预览的原件，
均为2026-10-22新建独立测试容器的真实页面像素，采集于发布和拉取重建之前。
after-recreate-ui.png为同日拉取后新容器的真实榜单页面截图。PNG未作编辑或合成。
历史终端截图保留原图，本轮命令过程提供日志，不把日志绘制成截图。

最初脚本比较完整RepoDigests数组，因推送前另有源仓库别名而触发断言；
改为比较目标Registry仓库的digest后，使用同一轮原始结果重新核验通过。
保留results-before-repository-normalization.json与results.json及recheck日志，
不隐瞒这次验证脚本修正，也未因此重做或改写实际Docker操作结果。

本包不重复加入JAR、运行数据库或与作业无关的完整容器清单；完整过程保存在
项目docs/local-test-20261022/。本轮所选原始日志、JSON、PNG、脚本字节不改。
路径和浏览器可执行文件反映采集机器；迁移复现时需调整本机路径并检查端口。
所有Registry均只对各自本机开放，不是其他机器可以直接访问的公开镜像地址。
未取得的Windows安装/首次配置全过程历史截图没有补造，需按教师实际口径复核。

manifest-sha256.json覆盖本包除该清单自身之外全部条目的大小和SHA256。
'''.encode('utf-8')

files = [
    'docker-version-restored.txt', 'docker-compose-version.txt',
    'source-build.log', 'docker-source-build.log',
    'playwright.log', 'docker-browser-tests.log', 'docker-browser-after.log',
    'ui-audit.log', 'ui-evidence/ui-audit.json',
    'health.json', 'before-restart.json', 'after-restart.json',
    'docker-roundtrip.py', 'capture-pulled-ui.cjs', 'docker-roundtrip-recheck.log',
]
roundtrip_files = [
    'network-create.txt', 'data-create.txt', 'registry-data-create.txt', 'registry-run.txt',
    'run-memory-game6085-localtest-20261022-app.txt', 'container-user.txt',
    'container-jar.txt', 'before-container.txt', 'initial-health.json',
    'tag.txt', 'push.txt', 'registry-tags.json', 'image-after-push.txt',
    'validate-owned-app.txt', 'app-stop.txt', 'app-remove.txt', 'image-remove.txt',
    'check-image-absent-remote.txt', 'check-image-absent-source.txt',
    'volume-retained.txt', 'pull.txt', 'image-after-pull.txt',
    'run-memory-game6085-localtest-20261022-pulled.txt',
    'pulled-container-jar.txt', 'pulled-container-mounts.txt', 'after-container.txt',
    'before-leaderboard.json', 'after-leaderboard.json', 'browser-after.json',
    'source-image-vs-delivery.json', 'results.json',
    'results-before-repository-normalization.json', 'after-recreate-ui.png',
    'browser-before/desktop-ready.png', 'browser-before/desktop-playing.png',
    'browser-before/desktop-completed.png', 'browser-before/mobile-ready.png',
    'browser-before/mobile-landscape.png',
]
mapping = {}
for name in files:
    target = 'windows-localtest-20261022/' + name
    mapping[target] = LOCAL / name
for name in roundtrip_files:
    target = 'windows-localtest-20261022/' + name
    mapping[target] = LOCAL / 'docker-roundtrip' / name
for name, path in mapping.items():
    evidence[name] = path.read_bytes()

manifest = {n: {'bytes': len(data), 'sha256': sha(data)} for n, data in sorted(evidence.items())}
evidence['manifest-sha256.json'] = dump(manifest)
evidence_path = DEST / '20261022-docker-evidence-v5.zip'
evidence_result = write_zip(evidence_path, evidence)
preserved = {}
for name, data in old_evidence.items():
    target = 'history-v4/' + name if name in ('README.txt', 'manifest-sha256.json') else name
    assert evidence[target] == data, name
    preserved[name] = target
assert all(len(evidence[n]) == item['bytes'] and sha(evidence[n]) == item['sha256']
           for n, item in manifest.items())
assert len(manifest) == len(evidence) - 1
assert not any(n.lower().endswith(('.jar', '.db', '.sqlite')) for n in evidence)
assert all(evidence[n] == p.read_bytes() for n, p in mapping.items())

previews = {}
for kind, filename in [('desktop', 'desktop-ready.png'), ('mobile', 'mobile-ready.png')]:
    origin = LOCAL / 'docker-roundtrip/browser-before' / filename
    target = DEST / f'20261022-memory-game6085-{kind}-v5.png'
    target.write_bytes(origin.read_bytes())
    previews[target.name] = {'source': origin.relative_to(ROOT).as_posix(),
                             'captureDate': '2026-10-22',
                             'stage': 'isolated Docker container before push/pull',
                             'bytes': target.stat().st_size, 'sha256': sha(target.read_bytes()),
                             'originalBytesUnchanged': True}

result = {
    'date': '2026-10-22', 'candidatesDirectory': DEST.relative_to(ROOT).as_posix(),
    'sourceInput': {'path': source_input.relative_to(ROOT).as_posix(),
                    'sha256': sha(source_input.read_bytes())},
    'evidenceInput': {'path': evidence_input.relative_to(ROOT).as_posix(),
                      'sha256': sha(evidence_input.read_bytes())},
    'sourcePackage': {**source_result, 'filename': source_path.name,
                      'changedEntries': changed, 'unchangedEntries': 33,
                      'deliveryJarSha256': sha(jar), 'appAndJarUnchanged': True},
    'evidencePackage': {**evidence_result, 'filename': evidence_path.name,
                        'manifestEntries': len(manifest), 'manifestValid': True,
                        'v4OriginalEntriesRetained': len(preserved),
                        'v4OriginalPaths': preserved,
                        'newOriginalFiles': {n: p.relative_to(ROOT).as_posix() for n, p in mapping.items()},
                        'allSelectedLocalFilesUnchanged': True,
                        'excludedLocalFiles': ['Docker JAR', 'running database',
                                               'full inspect/original/final unrelated container lists',
                                               'docker-roundtrip.log (contains unrelated final-containers output)']},
    'previews': previews,
    'reproducibility': 'sorted entries, fixed 2026-10-22 ZIP timestamp, ZIP_DEFLATED level 9; rerun and compare SHA256',
}
(WORK / 'package-validation.json').write_bytes(dump(result))
print(json.dumps({k: v for k, v in result.items() if k not in ('evidencePackage',)}, ensure_ascii=False, indent=2))
print(json.dumps({'evidencePackage': {k: v for k, v in result['evidencePackage'].items()
                                      if k not in ('v4OriginalPaths', 'newOriginalFiles')}}, ensure_ascii=False, indent=2))
