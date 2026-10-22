from pathlib import Path
import hashlib, io, json, zipfile
from lxml import etree as E

root = Path(__file__).resolve().parents[2]
work = Path(__file__).resolve().parent
digest = lambda b: hashlib.sha256(b).hexdigest()
result = {'baseline': {str(p.relative_to(root)):digest(p.read_bytes()) for directory in ['raw','output'] for p in (root/directory).rglob('*') if p.is_file()}}
archives = {}
for p in (root/'output/v4').glob('*.zip'):
    with zipfile.ZipFile(p) as z:
        item = {'entries':len(z.namelist()), 'crc':z.testzip(), 'sha256':digest(p.read_bytes())}
        if 'memory-game6085-v4' in p.name:
            differences = []
            for name in z.namelist():
                rel = Path(*Path(name).parts[1:])
                local = root/'Code/memory-game6085'/rel
                if local.is_file() and z.read(name).replace(b'\r\n',b'\n') != local.read_bytes().replace(b'\r\n',b'\n'):
                    differences.append(str(rel))
            item['workspaceDifferencesIgnoringCRLF'] = differences
            jarname = next(n for n in z.namelist() if n.endswith('.jar'))
            jarbytes = z.read(jarname)
            item['jarSha256'] = digest(jarbytes)
            item['jarMatchesWorkspaceDistribution'] = jarbytes == (root/'Code/memory-game6085/dist-artifacts/memory-game6085.jar').read_bytes()
            with zipfile.ZipFile(io.BytesIO(jarbytes)) as j:
                item['jarCRC'] = j.testzip()
                item['jarStaticFiles'] = [n for n in j.namelist() if n.startswith('BOOT-INF/classes/static/') and not n.endswith('/')]
            z.extractall(work/'unpacked')
        else:
            item['readme'] = z.read('README.txt').decode('utf-8')
        archives[p.name] = item
result['archives'] = archives
docx = root/'output/v4/20261021-docker-lab-report-v4.docx'
ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(docx) as z:
    for name in z.namelist():
        if name.endswith('.xml'):
            E.fromstring(z.read(name))
    xml = E.fromstring(z.read('word/document.xml'))
    paragraphs = [''.join(p.itertext()) for p in xml.findall('.//w:p', ns)]
    text = '\n'.join(''.join(p.xpath('.//w:t/text()', namespaces=ns)) for p in xml.findall('.//w:p',ns))
    (work/'v4-body.txt').write_text(text,encoding='utf-8')
    images = [n for n in z.namelist() if n.startswith('word/media/')]
    matches = {}
    pngs = {digest(p.read_bytes()):str(p.relative_to(root)) for folder in ['docs/docker-evidence','docs/v3-evidence'] for p in (root/folder).glob('*.png')}
    for name in images:
        matches[name] = pngs.get(digest(z.read(name)))
    result['word'] = {'sha256':digest(docx.read_bytes()),'zipCRC':z.testzip(),'xmlParse':'pass','tables':len(xml.findall('.//w:tbl',ns)), 'images':len(images), 'mediaSources':matches, 'revisionNodes':len(xml.findall('.//w:ins',ns))+len(xml.findall('.//w:del',ns)), 'markers':[s for s in ['待确认','TODO','草稿','资料未提供'] if s in text]}
    assert all(matches.values())
(work/'package-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k != 'baseline'},ensure_ascii=False,indent=2))
