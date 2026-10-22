from pathlib import Path
from zipfile import ZipFile
import json,hashlib,shutil,subprocess

WORK=Path(__file__).resolve().parent
ROOT=WORK.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=WORK/'word-final.docx'
target=ROOT/'output/v8/20261022-docker-lab-report-v8.docx'
checks=json.loads((WORK/'final-checks.json').read_text(encoding='utf-8'))
assert sha(source)==checks['sha256']
assert (checks['pages'],checks['images'],checks['tables'],checks['toc_entries'])==(33,31,7,39)
assert '45bd2d4f5efe4b21620b70d2809b96bb1e56633094c38192b0e27fefaaf84212' in (WORK/'visual-review.md').read_text(encoding='utf-8')
baseline=json.loads((WORK/'baseline-sha256.json').read_text(encoding='utf-8'))
assert all(sha(ROOT/p)==h for p,h in baseline.items())
assert not target.exists(),'Do not overwrite an existing delivery.'
validation=subprocess.run(['officecli','validate',str(source)],capture_output=True,text=True,encoding='utf-8')
(WORK/'schema-validation.txt').write_text(validation.stdout+validation.stderr,encoding='utf-8')
assert validation.returncode==0 and 'no errors found' in validation.stdout
target.parent.mkdir(exist_ok=True)
shutil.copyfile(source,target)
assert sha(target)==checks['sha256']
with ZipFile(target) as z:assert z.testzip() is None
assert all(sha(ROOT/p)==h for p,h in baseline.items())
result={'date':'2026-10-22','path':str(target.relative_to(ROOT)).replace('\\','/'),'bytes':target.stat().st_size,'sha256':sha(target),'pages':33,'images':31,'tables':7,'toc_entries':39,'source_v7_sha256':sha(WORK/'source-v7.docx'),'previous_files_unchanged':len(baseline),'strict_validation':'passed','visual_review':'all 33 final PNG pages inspected','code_paragraphs_preserved':checks['code_paragraphs_preserved'],'source_zip_updated':False,'pushed':False}
(WORK/'release-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
