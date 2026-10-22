from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import hashlib
import json

root = Path(__file__).resolve().parents[2]
source = root / 'output/v5/20261022-docker-lab-report-v5.docx'
work = Path(__file__).resolve().parent
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'w14': 'http://schemas.microsoft.com/office/word/2010/wordml'}

def txt(el):
    return ''.join(el.xpath('.//w:t/text()', namespaces=ns))

with ZipFile(source) as z:
    style_tree = etree.fromstring(z.read('word/styles.xml'))
    style_names = {}
    heading_styles = set()
    for st in style_tree.findall('w:style', ns):
        sid = st.get('{%s}styleId' % ns['w'])
        names = st.xpath('./w:name/@w:val', namespaces=ns)
        name = names[0] if names else sid
        style_names[sid] = name
        if name.lower().replace(' ', '') in ('heading1', 'heading2', 'heading3') or st.find('w:pPr/w:outlineLvl', ns) is not None:
            heading_styles.add(sid)
    tree = etree.fromstring(z.read('word/document.xml'))
    body = tree.find('w:body', ns)
    paragraphs, tables, blocks = [], [], []
    section = '封面和目录'
    for el in body:
        if el.tag == '{%s}p' % ns['w']:
            text = txt(el)
            pid = el.get('{%s}paraId' % ns['w14'])
            styles = el.xpath('./w:pPr/w:pStyle/@w:val', namespaces=ns)
            style = styles[0] if styles else ''
            if style in heading_styles:
                section = text
            item = {'paraId': pid, 'style': style, 'style_name': style_names.get(style, ''), 'section': section, 'text': text}
            paragraphs.append(item)
            blocks.append(item)
        elif el.tag == '{%s}tbl' % ns['w']:
            rows = [[txt(cell) for cell in row.findall('w:tc', ns)] for row in el.findall('w:tr', ns)]
            item = {'table': len(tables) + 1, 'section': section, 'rows': rows}
            tables.append(item)
            blocks.append(item)
    props = etree.fromstring(z.read('docProps/core.xml'))
    metadata = {etree.QName(el).localname: el.text for el in props}
    comment_parts = [n for n in z.namelist() if n.startswith('word/comments') and n.endswith('.xml')]
    comment_texts = {n: txt(etree.fromstring(z.read(n))) for n in comment_parts}
    revisions = len(tree.xpath('//w:ins|//w:del', namespaces=ns))
    keywords = ['真实', '实际', '本轮', '交付', 'v5', '分别', '保留', '未', 'AI', '人工智能', 'ChatGPT', 'Codex']
    all_text = '\n'.join([txt(el) for el in body])
    data = {'source': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'metadata': metadata, 'comments': comment_texts, 'revision_count': revisions,
            'keyword_counts': {s: all_text.count(s) for s in keywords},
            'paragraph_count': len(paragraphs), 'table_count': len(tables), 'blocks': blocks}
    (work / 'extracted-content.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    (work / 'tables.md').write_text('\n\n'.join(
        f"表{t['table']}：{t['section']}\n" + '\n'.join(' | '.join(row) for row in t['rows'])
        for t in tables), encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k != 'blocks'}, ensure_ascii=False, indent=2))
