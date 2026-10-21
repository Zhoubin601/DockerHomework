"""Revise the verified v1 report without altering historical experiment evidence."""
from copy import deepcopy
from pathlib import Path
import json

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / 'docs/v2-report-work'
WORK.mkdir(exist_ok=True)
SOURCE = ROOT / 'output/v1/20261021-docker-lab-report-v1.docx'
DEST = WORK / '20261021-docker-lab-report-v2.docx'
EVIDENCE = ROOT / 'docs/docker-evidence'


def set_text(p, text):
    """Retain paragraph formatting, replacing only textual runs."""
    rpr = deepcopy(p.runs[0]._r.rPr) if p.runs and p.runs[0]._r.rPr is not None else None
    p.clear()
    r = p.add_run(text)
    if rpr is not None:
        r._r.insert(0, rpr)
    return p


def insert_before(anchor, text, style='Normal', code=False, page=False):
    p = anchor.insert_paragraph_before(text, style)
    f = p.paragraph_format
    f.space_after = Pt(7)
    f.line_spacing = 1.25
    f.page_break_before = page
    if style == 'Heading 2':
        f.space_before, f.space_after, f.keep_with_next = Pt(10), Pt(8), True
        for r in p.runs:
            r.font.name, r.font.size, r.font.bold = '黑体', Pt(14), True
    else:
        f.first_line_indent = Cm(.74) if not code else Cm(0)
        for r in p.runs:
            r.font.name, r.font.size = ('Consolas', Pt(8.5)) if code else ('宋体', Pt(11))
    for r in p.runs:
        r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def bookmark(p, name, idx):
    start = OxmlElement('w:bookmarkStart')
    start.set(qn('w:id'), str(idx)); start.set(qn('w:name'), name)
    end = OxmlElement('w:bookmarkEnd'); end.set(qn('w:id'), str(idx))
    p._p.insert(1 if p._p.pPr is not None else 0, start)
    p._p.append(end)


def build_toc(doc):
    # Rebuild the field's cached paragraphs as well as its actual Word field.
    title = next(p for p in doc.paragraphs if p.text == '目录')
    first = next(p for p in doc.paragraphs if p.text == '一 实验目的与任务要求')
    node = title._p.getnext()
    while node is not first._p:
        nxt = node.getnext(); node.getparent().remove(node); node = nxt
    first.paragraph_format.page_break_before = True
    headings = [p for p in doc.paragraphs if p.style.name in ('Heading 1', 'Heading 2')]
    entries = []
    for idx, p in enumerate(headings, 500):
        name = f'V2Heading{idx}'
        bookmark(p, name, idx)
        level = 1 if p.style.name == 'Heading 1' else 2
        tp = first.insert_paragraph_before()
        tp.style = 'Normal'
        pf = tp.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(0 if level == 1 else .6)
        pf.space_before = Pt(0); pf.space_after = Pt(0)
        pf.line_spacing = 1.05
        pf.tab_stops.add_tab_stop(Cm(16.4 if level == 1 else 15.8), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        if not entries:
            rr = tp.add_run()._r
            begin = OxmlElement('w:fldChar'); begin.set(qn('w:fldCharType'), 'begin'); rr.append(begin)
            instruction = OxmlElement('w:instrText'); instruction.set(qn('xml:space'), 'preserve')
            instruction.text = ' TOC \\o "1-2" \\h \\u '; tp.add_run()._r.append(instruction)
            sep = OxmlElement('w:fldChar'); sep.set(qn('w:fldCharType'), 'separate'); tp.add_run()._r.append(sep)
        hyperlink = OxmlElement('w:hyperlink'); hyperlink.set(qn('w:anchor'), name)
        r = OxmlElement('w:r'); rpr = OxmlElement('w:rPr')
        fonts = OxmlElement('w:rFonts')
        for attr in ('ascii', 'hAnsi', 'eastAsia'): fonts.set(qn('w:'+attr), '宋体')
        rpr.append(fonts)
        sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '21'); rpr.append(sz)
        color = OxmlElement('w:color'); color.set(qn('w:val'), '000000'); rpr.append(color)
        r.append(rpr)
        t = OxmlElement('w:t'); t.text = p.text; r.append(t)
        r.append(OxmlElement('w:tab'))
        hyperlink.append(r)
        field = OxmlElement('w:fldSimple'); field.set(qn('w:instr'), f' PAGEREF {name} \\h ')
        number_run = OxmlElement('w:r'); number_run.append(deepcopy(rpr))
        number = OxmlElement('w:t'); number.text = '1'; number_run.append(number); field.append(number_run)
        hyperlink.append(field); tp._p.append(hyperlink)
        entries.append({'heading': p.text, 'bookmark': name, 'level': level})
    end = OxmlElement('w:fldChar'); end.set(qn('w:fldCharType'), 'end')
    tp.add_run()._r.append(end)
    return entries


doc = Document(SOURCE)
# Remove cached rendered-page boundaries; editors must repaginate the revised file.
for node in doc._element.xpath('.//w:lastRenderedPageBreak'):
    node.getparent().remove(node)

paragraphs = list(doc.paragraphs)
by_text = {p.text: p for p in paragraphs}
env_title = by_text['二 实验环境与项目结构']
environment_table = doc.tables[1]
heading = doc.add_paragraph('2.1 实验配置与项目目录', 'Heading 2')
environment_table._tbl.addprevious(heading._p)
environment_picture = next(p for p in paragraphs if p._p.xpath('.//wp:docPr[@id="2"]'))
insert_before(environment_picture, '2.2 环境启动与验证', 'Heading 2', page=True)
insert_before(environment_picture, '本实验沿用 Windows 上已安装的 Docker Desktop，使用 WSL2 的 Linux 容器引擎。原有 WSL 数据目录继续使用。表中的环境版本取自本次实验机器，图2展示恢复启动后的实际验证结果。')
insert_before(environment_picture, '启动时遇到遗留 socket 故障，Docker Desktop 无法正常提供服务。为恢复启动，在 Docker Desktop 停止时执行下面的辅助脚本，仅为该子进程设置独立的 LOCALAPPDATA 运行时缓存目录，保留系统级环境变量。')
insert_before(environment_picture, '.\\scripts\\start-docker-runtime.ps1', code=True)
insert_before(environment_picture, '引擎启动后，在项目根目录执行版本与命名检查。docker version 同时返回 Client 和 Server 29.8.2，Engine 为 linux/amd64；Compose 返回 5.6.0，项目目录为 memory-game6085。随后执行第五章的构建与运行操作。')
for command in ['docker version', 'docker compose version', 'Get-Item . | Select-Object Name, FullName']:
    insert_before(environment_picture, command, code=True)

old_build_picture = next(p for p in paragraphs if p._p.xpath('.//wp:docPr[@id="4"]'))
build_command = by_text['docker compose --progress plain build']
insert_before(build_command, '5.2 JAR 打包与镜像导出', 'Heading 2', page=True)
for blip in old_build_picture._p.xpath('.//a:blip'):
    doc.part.drop_rel(blip.get(qn('r:embed')))
old_build_picture.clear()
old_build_picture.paragraph_format.line_spacing = 1
run = old_build_picture.add_run()
shape = run.add_picture(str(EVIDENCE/'02-build-progress.png'), width=Cm(16.4))
shape._inline.docPr.set('descr', 'Spring Boot JAR 打包、repackage、BUILD SUCCESS 与 Docker 镜像导出')
shape._inline.docPr.set('name', '真实 Spring Boot 打包与镜像构建日志')
set_text(by_text['图4  Spring Boot 打包成功并导出 Docker 镜像'], '图4  Spring Boot JAR 打包成功并导出 Docker 镜像')
set_text(by_text['5.2 启动容器与接口检查'], '5.3 启动容器与接口检查')
for p in paragraphs:
    if p.text.startswith('本实验使用已确认的本机私有 Registry'):
        set_text(p, p.text.replace('本实验使用已确认的本机私有 Registry', '本实验使用本机私有 Registry'))
    elif p.text.startswith('原始作业要求：raw/要求.png；身份信息'):
        set_text(p, '原始作业要求：raw/要求.png。实验项目为记忆花园 memory-game6085，采用 Vue3、Spring Boot 和 SQLite，镜像仓库为本机 Registry。')
    elif p.text == '.\\\\scripts\\\\build.ps1':
        set_text(p, '.\\scripts\\build.ps1')

# Add the environment evidence to the task matrix, and align figure 4's source.
row = doc.tables[0].add_row()
row.cells[0].text = 'Docker 环境部署与验证'
row.cells[1].text = '沿用已有 Docker Desktop，恢复启动并验证 Client、Server 与 Compose'
for row in doc.tables[-1].rows:
    if row.cells[0].text == '4':
        row.cells[1].text = 'Spring Boot JAR 打包与镜像导出'
        row.cells[2].text = '02-build-progress.png'

# Keep tables readable in both Word and LibreOffice.
for table in doc.tables:
    for index, row in enumerate(table.rows):
        trpr = row._tr.get_or_add_trPr()
        if trpr.find(qn('w:cantSplit')) is None: trpr.append(OxmlElement('w:cantSplit'))
        if index == 0 and trpr.find(qn('w:tblHeader')) is None: trpr.append(OxmlElement('w:tblHeader'))
        for cell in row.cells:
            for p in cell.paragraphs:
                pf = p.paragraph_format
                pf.first_line_indent = Cm(0)
                pf.line_spacing = 1.12
                pf.space_before, pf.space_after = Pt(1), Pt(1)

# Picture and caption should move together; normalize the tiny line box only.
for p in doc.paragraphs:
    if p.style.name in ('Heading 1', 'Heading 2'):
        for r in p.runs:
            r.font.color.rgb = RGBColor(0, 0, 0)
    if p._p.xpath('.//w:drawing'):
        p.paragraph_format.line_spacing = 1
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(1)

# Keep the completed-game screenshot beside its explanation across renderers.
for shape in doc.inline_shapes:
    if shape._inline.docPr.get('id') == '3':
        ratio = shape.height / shape.width
        shape.width = Cm(13.5)
        shape.height = int(shape.width * ratio)

entries = build_toc(doc)
# Use available CJK fonts explicitly. Missing Windows fonts can otherwise cause
# LibreOffice's fallback shaping to omit Chinese text beside numbers.
for style in doc.styles:
    if style.type == 1:
        family = 'Noto Sans CJK SC' if style.name.startswith('Heading') or style.name == 'Title' else 'Noto Serif CJK SC'
        rpr = style.element.get_or_add_rPr()
        fonts = rpr.find(qn('w:rFonts'))
        if fonts is None: fonts = OxmlElement('w:rFonts'); rpr.insert(0, fonts)
        fonts.attrib.clear()
        for key in ('ascii', 'hAnsi', 'cs'): fonts.set(qn('w:'+key), 'Liberation Sans' if family == 'Noto Sans CJK SC' else 'Liberation Serif')
        fonts.set(qn('w:eastAsia'), family)
for part in [doc.part, *[s.header.part for s in doc.sections], *[s.footer.part for s in doc.sections]]:
    for run in part.element.xpath('.//w:r'):
        rpr = run.find(qn('w:rPr'))
        fonts = rpr.find(qn('w:rFonts')) if rpr is not None else None
        mono = fonts is not None and fonts.get(qn('w:ascii')) == 'Consolas'
        parent = run.getparent()
        while parent is not None and parent.tag != qn('w:p'): parent = parent.getparent()
        pp = parent.find(qn('w:pPr')) if parent is not None else None
        ps = pp.find(qn('w:pStyle')) if pp is not None else None
        heading = ps is not None and ps.get(qn('w:val')) in ('1', '2', 'Heading1', 'Heading2', 'Title')
        if rpr is None: rpr = OxmlElement('w:rPr'); run.insert(0, rpr)
        if fonts is None: fonts = OxmlElement('w:rFonts'); rpr.insert(0, fonts)
        fonts.attrib.clear()
        family = 'DejaVu Sans Mono' if mono else ('Liberation Sans' if heading else 'Liberation Serif')
        for key in ('ascii', 'hAnsi', 'cs'): fonts.set(qn('w:'+key), family)
        fonts.set(qn('w:eastAsia'), 'Noto Sans Mono CJK SC' if mono else ('Noto Sans CJK SC' if heading else 'Noto Serif CJK SC'))

# Set deliberate leading instead of inheriting a font-dependent automatic line
# height, while leaving image line boxes free to expand to the picture height.
from docx.text.paragraph import Paragraph
for element in doc.element.body.xpath('.//w:p'):
    if element.xpath('.//w:drawing'): continue
    p = Paragraph(element, doc)
    sizes = [int(s.get(qn('w:val'))) / 2 for s in element.xpath('./w:pPr/w:rPr/w:sz | ./w:r/w:rPr/w:sz')]
    default_size = p.style.font.size.pt if p.style.font.size else 11
    size = max(sizes, default=default_size)
    is_toc = bool(element.xpath('.//w:fldSimple[contains(@w:instr,"PAGEREF V2Heading")]'))
    mono = bool(element.xpath('.//w:rFonts[@w:ascii="DejaVu Sans Mono"]'))
    in_cell = element.getparent().tag == qn('w:tc')
    factor = 1.3 if p.style.name == 'Title' else (1.35 if mono else 1.5)
    p.paragraph_format.line_spacing = Pt(15 if is_toc else (14 if in_cell else size * factor))
    snap = element.get_or_add_pPr().find(qn('w:snapToGrid'))
    if snap is None: snap = OxmlElement('w:snapToGrid'); element.get_or_add_pPr().append(snap)
    snap.set(qn('w:val'), 'false')
settings = doc.settings.element
update = settings.find(qn('w:updateFields'))
if update is None: update = OxmlElement('w:updateFields'); settings.append(update)
update.set(qn('w:val'), 'true')
doc.core_properties.title = 'Spring Boot 小游戏 Docker 容器化实验报告'
doc.core_properties.author = '周宇斌'
doc.core_properties.revision = 2
doc.save(DEST)
(WORK/'toc-headings.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf8')
print(DEST)
print('Headings:', len(entries), 'Tables:', len(doc.tables), 'Figures:', len(doc.inline_shapes))
