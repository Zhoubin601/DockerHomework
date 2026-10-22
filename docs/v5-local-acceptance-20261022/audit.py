from pathlib import Path
from zipfile import ZipFile
import hashlib, json, re
from lxml import etree as E

W = Path(__file__).resolve().parent
R = W.parents[1]
sha = lambda b: hashlib.sha256(b).hexdigest()
def save(name, obj):
    (W/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

baseline = {str(p.relative_to(R)): sha(p.read_bytes()) for folder in ['raw', 'output'] for p in (R/folder).rglob('*') if p.is_file()}
save('baseline-sha256.json', baseline)
manifest = json.loads((R/'docs/v5-work/release-manifest.json').read_text(encoding='utf-8'))
release=[]
for item in manifest['files']:
    p=R/item['path']
    release.append({'path': item['path'], 'sha256':sha(p.read_bytes()), 'matches':sha(p.read_bytes())==item['sha256'] and p.stat().st_size==item['bytes']})
assert all(i['matches'] for i in release)
src=R/'output/v5/20261022-memory-game6085-v5.zip'
with ZipFile(src) as z:
    assert z.testzip() is None
    dest=(W/'unpacked').resolve()
    for name in z.namelist():
        target=(dest/name).resolve()
        assert target.is_relative_to(dest)
    z.extractall(dest)
    diffs=[]
    for name in z.namelist():
        actual=z.read(name)
        local=R/'Code'/name
        if not local.exists() or actual.replace(b'\r\n',b'\n')!=local.read_bytes().replace(b'\r\n',b'\n'):
            diffs.append(name)
    jar=z.read('memory-game6085/dist-artifacts/memory-game6085.jar')
    source={'entries':len(z.namelist()),'crcValid':True,'workspaceDifferences':diffs,'jarSha256':sha(jar)}
    assert not diffs
with ZipFile(R/'output/v5/20261022-docker-evidence-v5.zip') as z:
    assert z.testzip() is None
    em=json.loads(z.read('manifest-sha256.json'))
    bad=[name for name, meta in em.items() if sha(z.read(name))!=meta['sha256'] or len(z.read(name))!=meta['bytes']]
    assert not bad
    assert set(em)==set(z.namelist())-{'manifest-sha256.json'}
    evidence={'entries':len(z.namelist()),'crcValid':True,'manifestEntries':len(em),'manifestFailures':bad}
    pngs={sha(z.read(n)):n for n in z.namelist() if n.endswith('.png')}
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(R/'output/v5/20261022-docker-lab-report-v5.docx') as z:
    assert z.testzip() is None
    for n in z.namelist():
        if n.endswith(('.xml','.rels')): E.fromstring(z.read(n))
    doc=E.fromstring(z.read('word/document.xml'))
    text='\n'.join(''.join(p.xpath('.//w:t/text()',namespaces=N)) for p in doc.xpath('.//w:p',namespaces=N))
    (W/'report-text.txt').write_text(text,encoding='utf-8')
    media=[{'part':n,'evidenceSource':pngs.get(sha(z.read(n)))} for n in z.namelist() if n.startswith('word/media/')]
    assert len(media)==22 and all(m['evidenceSource'] for m in media)
    markers=[line for line in text.splitlines() if any(x in line for x in ['待确认：','TODO','TBD','lorem ipsum','{{'])]
    assert not markers
    report={'images':len(media),'tables':len(doc.xpath('./w:body/w:tbl',namespaces=N)),'mediaSources':media,'unresolvedMarkerLines':markers,'trackedChanges':len(doc.xpath('.//w:ins | .//w:del',namespaces=N))}
save('package-audit.json',{'release':release,'sourcePackage':source,'evidencePackage':evidence,'report':report})
print(json.dumps({'releaseHashes':len(release),'source':source,'evidence':evidence,'reportImages':len(media),'reportTables':report['tables'],'allImagesMatchEvidence':True},ensure_ascii=False,indent=2))
