from pathlib import Path
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
REPORT = ROOT / 'output/v7/20261022-docker-lab-report-v7.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'w14': 'http://schemas.microsoft.com/office/word/2010/wordml'}

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def snapshot():
    return {str(p.relative_to(ROOT)).replace('\\', '/'): digest(p)
            for folder in ('raw', 'output')
            for p in sorted((ROOT / folder).rglob('*')) if p.is_file()}

def content(p):
    return ''.join(n.text or '' for n in p.iter() if n.tag == f"{{{NS['w']}}}t")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'verify':
        before = json.loads((WORK / 'baseline-sha256.json').read_text(encoding='utf-8'))
        after = snapshot()
        changes = [k for k in sorted(before.keys() | after.keys()) if before.get(k) != after.get(k)]
        result = {'checked_files': len(before), 'unchanged': not changes, 'changed_paths': changes,
                  'report_sha256': digest(REPORT)}
        (WORK / 'integrity-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(bool(changes))
    baseline = WORK / 'baseline-sha256.json'
    if baseline.exists():
        raise SystemExit('Baseline already exists; do not overwrite it.')
    baseline.write_text(json.dumps(snapshot(), ensure_ascii=False, indent=2), encoding='utf-8')
    with zipfile.ZipFile(REPORT) as archive:
        doc = ET.fromstring(archive.read('word/document.xml'))
        body = doc.find('w:body', NS)
        paragraphs = [{'index': i, 'paraId': p.get(f"{{{NS['w14']}}}paraId"), 'text': content(p)}
                      for i, p in enumerate(body.findall('w:p', NS), 1)]
        tables = [{'index': i, 'rows': [[content(cell) for cell in row.findall('w:tc', NS)]
                                       for row in table.findall('w:tr', NS)]}
                  for i, table in enumerate(body.findall('w:tbl', NS), 1)]
        all_text = '\n'.join(p['text'] for p in paragraphs) + '\n' + '\n'.join(' | '.join(row) for table in tables for row in table['rows'])
        all_parts = []
        for name in archive.namelist():
            if name.startswith('word/') and name.endswith('.xml'):
                try:
                    tree = ET.fromstring(archive.read(name))
                    all_parts.append({'part': name, 'text': ' '.join(tree.itertext())})
                except ET.ParseError:
                    pass
        marker = re.compile(r'ChatGPT|Codex|OpenAI|作为\s*AI|人工智能生成|由\s*AI\s*(生成|编写)', re.I)
        marker_hits = [{'part': part['part'], 'matches': marker.findall(part['text'])}
                       for part in all_parts if marker.search(part['text'])]
        metadata = ET.fromstring(archive.read('docProps/core.xml')) if 'docProps/core.xml' in archive.namelist() else None
        metadata_hits = marker.findall(' '.join(metadata.itertext())) if metadata is not None else []
        counts = {term: all_text.count(term) for term in ['实际', '真实', '本轮', '补充实验', '完整', '验证']}
        comment_count = sum(len(ET.fromstring(archive.read(name)).findall('w:comment', NS))
                            for name in archive.namelist() if name == 'word/comments.xml')
        result = {'report': str(REPORT), 'sha256': digest(REPORT), 'paragraph_count': len(paragraphs),
                  'table_count': len(tables), 'image_count': len(doc.findall('.//w:drawing', NS)),
                  'paragraphs': paragraphs, 'tables': tables, 'word_counts': counts,
                  'marker_hits_in_word_parts': marker_hits, 'marker_hits_in_core_metadata': metadata_hits,
                  'comments': comment_count, 'insertions': len(doc.findall('.//w:ins', NS)),
                  'deletions': len(doc.findall('.//w:del', NS))}
        (WORK / 'document-inspection.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({k: v for k, v in result.items() if k not in ('paragraphs', 'tables')}, ensure_ascii=False, indent=2))
        print(json.dumps(tables, ensure_ascii=False, indent=2))
