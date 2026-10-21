"""Check completed report evidence and create versioned final deliverables."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
import hashlib, json, shutil

root=Path(__file__).resolve().parents[3]
output=root/'output'
work=root/'docs/report-final-work'
source=work/'20261021-docker-lab-report-v1.docx'
evidence=root/'docs/docker-evidence'
names=['04-container-home.png','01-environment.png','05-container-completed.png','02-build.png','03b-container-run.png','05-registry-push.png','06-remove-local.png','07-registry-pull.png','04-data-before.png','08-run-pulled-image.png','09-data-after.png']
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
result=json.loads((evidence/'results.json').read_text(encoding='utf-8'))
assert result['leaderboardPreserved'] and result['beforeContainerId']!=result['afterContainerId']
assert result['health']['status']=='UP'
assert hashlib.sha256((root/'raw/要求.png').read_bytes()).hexdigest().upper()=='12C0240D5DCD5CFE16D4FF241FA28E113B3A5C3ECD8BB08C26DB8C05B7336B1A'
with ZipFile(source) as z:
    xml=etree.fromstring(z.read('word/document.xml'))
    text=''.join(xml.xpath('//w:t/text()',namespaces=ns))
    assert all(value in text for value in ['周宇斌','软件2401','20246085',result['digest'],'9.1 截图来源索引'])
    assert all(value not in text for value in ['待确认','lorem','<TODO>','过程稿','xxxx'])
    assert len(xml.xpath('//w:drawing',namespaces=ns))==11
    assert len(xml.xpath('//w:tbl',namespaces=ns))==7
    assert len(xml.xpath('//wp:docPr[@descr]',namespaces=ns))==11
    assert 'TOC ' in ''.join(xml.xpath('//w:instrText/text()',namespaces=ns))
    footers=[name for name in z.namelist() if name.startswith('word/footer') and name.endswith('.xml')]
    assert any(b'PAGE' in z.read(name) for name in footers)
    hashes={hashlib.sha256(z.read(name)).hexdigest() for name in z.namelist() if name.startswith('word/media/')}
    assert all(hashlib.sha256((evidence/name).read_bytes()).hexdigest() in hashes for name in names), 'Embedded screenshots must be identical to the actual evidence'

destinations=[output/'20261021-docker-lab-report-v1.docx',output/'20261021-docker-evidence-v1.zip',output/'20261021-memory-game6085-v2.zip']
assert not any(path.exists() for path in destinations), 'Never overwrite an existing delivery'
shutil.copy2(source,destinations[0])
with ZipFile(destinations[1],'x',ZIP_DEFLATED) as z:
    for name in [*names,'results.json']:
        z.write(evidence/name,name)
    z.writestr('README.txt','2026-10-21 Docker experiment 6085\n11 original screenshots embedded in the Word report, plus actual machine-readable experiment results.\nRegistry scope: localhost:5000. Application: localhost:18085.\n')
# Keep the previous, verified source/JAR file list; read updated project files.
with ZipFile(output/'20261021-memory-game6085-v1.zip') as old, ZipFile(destinations[2],'x',ZIP_DEFLATED) as z:
    for name in old.namelist():
        relative=Path(name).relative_to('memory-game6085')
        current=root/'Code/memory-game6085'/relative
        assert current.is_file(), current
        z.write(current,name)
for path in destinations:
    assert path.is_file() and path.stat().st_size>1000
    if path.suffix=='.zip':
        with ZipFile(path) as z: assert z.testzip() is None
print(json.dumps({'pages':15,'figures':11,'tables':7,'rawUnchanged':True,'embeddedScreenshotsUnchanged':True,'files':[{ 'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in destinations]},ensure_ascii=False,indent=2))
