"""Promote only verified v5 candidates and write a release manifest."""
from pathlib import Path
import hashlib, json, re, shutil, zipfile
from lxml import etree as E

root=Path(__file__).resolve().parents[2]
work=Path(__file__).resolve().parent
report=root/'docs/v5-report-work/20261022-docker-lab-report-v5.docx'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((work/'baseline-sha256.json').read_text(encoding='utf-8'))
assert all((root/p).is_file() and sha(root/p)==h for p,h in baseline.items()),'Original files changed'
assert 'Validation passed: no errors found.' in (root/'docs/v5-report-work/schema-final.txt').read_text(encoding='utf-8-sig')
audit=json.loads((work/'independent-docx-audit.json').read_text(encoding='utf-8'))
assert audit['sha256']==sha(report),'Independent review is stale'
assert not audit['crcError'] and not audit['xmlErrors'] and not audit['missingRelationshipTargets']
assert not audit['historicalMediaMissing'] and not audit['unresolvedMarkerLines'] and not audit['revisionCount']
assert audit['inlineImageCount']==22 and audit['tableCount']==9 and all(audit['expectedLocalEvidenceKeys'].values())
assert all(item['source'] for item in audit['media'])
pages=json.loads((root/'docs/v5-report-work/native-pagination-verification.json').read_text(encoding='utf-8'))
assert pages['pages']==31 and pages['tocEntries']==42 and pages['allTOCPagesVerifiedInPDF']
independent=(work/'independent-final-review.md').read_text(encoding='utf-8')
assert '通过' in independent
package=json.loads((work/'package-validation.json').read_text(encoding='utf-8'))
for key in ['sourcePackage','evidencePackage']:
    item=package[key]
    candidate=work/'packages'/item['filename']
    assert sha(candidate)==item['sha256']
    with zipfile.ZipFile(candidate) as z:assert z.testzip() is None
sources=[report,*sorted((work/'packages').iterdir())]
assert len(sources)==5
destination=root/'output/v5'
destination.mkdir(exist_ok=True)
for p in sources:
    dest=destination/p.name
    assert not dest.exists(),'Refusing to overwrite '+str(dest)
    shutil.copyfile(p,dest)
    assert sha(p)==sha(dest)
manifest={'date':'2026-10-22','version':'v5','pages':31,'figures':22,'tables':9,'tocEntries':42,
          'strictOOXMLValidation':'passed, 0 errors','nativeWordRender':'31 pages; TOC pages verified',
          'historicalFilesUnchanged':len(baseline),'files':[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(destination.iterdir())]}
(work/'release-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
