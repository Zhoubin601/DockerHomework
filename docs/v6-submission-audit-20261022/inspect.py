from pathlib import Path
from io import BytesIO
import hashlib
import json
import posixpath
import zipfile
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def sha(data):
    return hashlib.sha256(data).hexdigest()

result = {'date': '2026-10-22', 'files': {}}
for file in [ROOT/'raw/要求.png', *sorted((ROOT/'output/v6').glob('*'))]:
    result['files'][str(file.relative_to(ROOT))] = {'bytes': file.stat().st_size, 'sha256': sha(file.read_bytes())}

evidence = {}
with zipfile.ZipFile(ROOT/'output/v5/20261022-docker-evidence-v5.zip') as z:
    for name in z.namelist():
        if name.lower().endswith('.png'):
            evidence.setdefault(sha(z.read(name)), []).append(name)

with zipfile.ZipFile(ROOT/'output/v6/memory-game6085.docx') as z:
    root = ET.fromstring(z.read('word/document.xml'))
    body = root.find('w:body', NS)
    paragraphs = [''.join(p.itertext()) if False else ''.join(t.text or '' for t in p.findall('.//w:t', NS)) for p in body.findall('w:p', NS)]
    rels = {r.get('Id'): r for r in ET.fromstring(z.read('word/_rels/document.xml.rels'))}
    images = []
    for index, blip in enumerate(root.findall('.//a:blip', NS), 1):
        rid = blip.get('{'+NS['r']+'}embed')
        rel = rels[rid]
        name = posixpath.normpath(posixpath.join('word', rel.get('Target')))
        data = z.read(name)
        im = Image.open(BytesIO(data))
        images.append({'index': index, 'member': name, 'dimensions': im.size, 'sha256': sha(data), 'evidence_matches': evidence.get(sha(data), [])})
        (WORK/f'figure-{index:02}.png').write_bytes(data)
    text = '\n'.join(' | '.join(''.join(t.text or '' for t in cell.findall('.//w:t', NS)) for cell in el.findall('w:tr/w:tc', NS)) if el.tag.endswith('}tbl') else ''.join(t.text or '' for t in el.findall('.//w:t', NS)) for el in body)
    (WORK/'document-text.txt').write_text(text, encoding='utf-8')
    result['word'] = {'crc_error': z.testzip(), 'paragraphs': len(paragraphs), 'tables': len(body.findall('w:tbl', NS)), 'images': images, 'appendix_headings': [p for p in paragraphs if p.startswith('附录')], 'appendix_references': [line for line in text.splitlines() if '附录' in line or '均嵌入' in line], 'external_image_links': [dict(r.attrib) for r in rels.values() if r.get('Type', '').endswith('/image') and r.get('TargetMode') == 'External']}

with zipfile.ZipFile(ROOT/'output/v6/memory-game6085.zip') as z:
    names = z.namelist()
    differences = []
    for name in names:
        if name.endswith('/'):
            continue
        local = ROOT/'Code'/name
        if not local.exists():
            differences.append({'member': name, 'status': 'not_in_Code'})
        elif z.read(name).replace(b'\r\n', b'\n') != local.read_bytes().replace(b'\r\n', b'\n'):
            differences.append({'member': name, 'status': 'content_differs'})
    jar = z.read('memory-game6085/dist-artifacts/memory-game6085.jar')
    result['source_zip'] = {'crc_error': z.testzip(), 'members': names, 'member_count': len(names), 'differences_from_Code_ignoring_line_endings': differences, 'same_bytes_as_v5_zip': sha((ROOT/'output/v6/memory-game6085.zip').read_bytes()) == sha((ROOT/'output/v5/20261022-memory-game6085-v5.zip').read_bytes()), 'jar_sha256': sha(jar), 'jar_manifest': z.read('memory-game6085/dist-artifacts/SHA256SUMS').decode(), 'pom': z.read('memory-game6085/backend/pom.xml').decode(), 'dockerfile': z.read('memory-game6085/Dockerfile').decode(), 'compose': z.read('memory-game6085/compose.yaml').decode()}

for start in [1, 7]:
    sheet = Image.new('RGB', (1440, 1170), '#dddddd')
    draw = ImageDraw.Draw(sheet)
    for offset, index in enumerate(range(start, min(start+6, 12))):
        im = Image.open(WORK/f'figure-{index:02}.png').convert('RGB')
        im.thumbnail((700, 350))
        x, y = (offset % 2)*720+10, (offset // 2)*390+30
        draw.text((x, y-22), f'Figure {index}: {images[index-1]["dimensions"]}', fill='black')
        sheet.paste(im, (x, y))
    sheet.save(WORK/f'figures-{start:02}.jpg', quality=90)

(WORK/'inspection.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'word_images': len(images), 'tables': result['word']['tables'], 'all_images_match_evidence': all(i['evidence_matches'] for i in images), 'appendix_headings': result['word']['appendix_headings'], 'source_zip_members': result['source_zip']['member_count'], 'source_zip_differences': differences, 'source_zip_equals_v5': result['source_zip']['same_bytes_as_v5_zip']}, ensure_ascii=False, indent=2))
