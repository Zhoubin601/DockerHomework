from pathlib import Path
from zipfile import ZipFile
import hashlib, json, shutil

work=Path(__file__).resolve().parent
root=work.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((work/'baseline-files.json').read_text(encoding='utf-8-sig'))
for item in baseline:
    assert sha(Path(item['Path'])).lower()==item['Sha256'].lower(),item['Path']
checks=json.loads((work/'final-checks.json').read_text(encoding='utf-8'))
assert checks['pages']==33 and checks['images']==31
assert sha(work/'word-final.docx')==checks['final_sha256']
with ZipFile(root/'output/v6/memory-game6085.zip') as source:
    assert source.testzip() is None
    names=source.namelist()
    assert len(names)==34
    jar=next(n for n in names if n.endswith('dist-artifacts/memory-game6085.jar'))
    assert hashlib.sha256(source.read(jar)).hexdigest()=='2e97ff46f2acfc1bfe0411a22f3f61a3ef4b8958e4ba5fff609d0350853852a0'
target=root/'output/v7'
target.mkdir(exist_ok=True)
files=[(work/'word-final.docx',target/'20261022-docker-lab-report-v7.docx'),
       (root/'output/v6/memory-game6085.zip',target/'20261022-memory-game6085-v7.zip')]
manifest=[]
for source,dest in files:
    assert not dest.exists(),f'Existing delivery must not be overwritten: {dest}'
    shutil.copyfile(source,dest)
    assert sha(source)==sha(dest)
    with ZipFile(dest) as archive: assert archive.testzip() is None
    manifest.append({'path':str(dest.relative_to(root)),'bytes':dest.stat().st_size,'sha256':sha(dest)})
assert len(list(target.iterdir()))==2
result={'date':'2026-10-22','files':manifest,'report':{'pages':33,'images':31,'tables':7,'toc_entries':39},'baseline_files_unchanged':len(baseline),'source_zip_unchanged':True,'source_zip_members':len(names),'jar_sha256':'2e97ff46f2acfc1bfe0411a22f3f61a3ef4b8958e4ba5fff609d0350853852a0'}
(work/'release-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
