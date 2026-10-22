"""Check the exact staged update without printing possible secret values."""
from pathlib import Path
import hashlib, io, json, re, subprocess, zipfile

root=Path(__file__).resolve().parents[2]
work=Path(__file__).resolve().parent
run=lambda *args:subprocess.check_output(['git',*args],cwd=root)
names=[p for p in run('diff','--cached','--name-only','-z','--diff-filter=ACMR').decode('utf-8').split('\0') if p]
assert names
forbidden=['/unpacked/','/deliverable-db/','/ui-generated-original/','source-image-app.jar','v4-review.docx','/v5-work/packages/','/render-pass']
assert not [p for p in names if any(x in p for x in forbidden)]
assert not any(p.startswith(('raw/','output/v1/','output/v2/','output/v3/','output/v4/')) for p in names)
rules={
 'private-key':re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'github-token':re.compile(rb'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{25,}\b'),
 'openai-key':re.compile(rb'\bsk-(?:proj-)?[A-Za-z0-9_-]{28,}\b'),
 'aws-access':re.compile(rb'\bAKIA[0-9A-Z]{16}\b'),
 'credential-assignment':re.compile(rb'''(?i)\b(?:password|api[_-]?key|access[_-]?token|secret[_-]?key)\s*[:=]\s*["'][^"'\r\n]{8,}["']'''),
}
failures=[]
scanned=0
sizes=[]
def scan(label,data):
 global scanned
 if b'\0' in data[:8000]:return
 scanned+=1
 for name,pattern in rules.items():
    if pattern.search(data):failures.append({'path':label,'rule':name})
for name in names:
 data=run('show',':'+name)
 sizes.append({'path':name,'bytes':len(data)})
 assert len(data)<50*1024*1024,name
 if zipfile.is_zipfile(io.BytesIO(data)):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None,name
        for entry in z.namelist():
            if entry.endswith(('.txt','.md','.json','.xml','.rels','.js','.mjs','.cjs','.java','.ps1','.py','.yaml','.yml','.properties','.html')):
                scan(name+'!'+entry,z.read(entry))
 elif Path(name).suffix.lower() in {'.txt','.md','.json','.xml','.js','.mjs','.cjs','.java','.ps1','.py','.yaml','.yml','.properties','.html','.log'}:
    scan(name,data)
baseline=json.loads((work/'baseline-sha256.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in baseline.items())
manifest=json.loads((work/'release-manifest.json').read_text(encoding='utf-8'))
for item in manifest['files']:
 path=Path(item['path']).as_posix()
 data=run('show',':'+path)
 assert hashlib.sha256(data).hexdigest()==item['sha256'],path
result={'stagedFiles':len(names),'stagedBytes':sum(x['bytes'] for x in sizes),'largestFile':max(sizes,key=lambda x:x['bytes']), 'textEntriesScanned':scanned,'credentialPatternFailures':failures,'rawAndPriorReleasesUnchanged':len(baseline),'releaseManifestMatchesStaging':True,'temporaryFilesExcluded':True}
out=work/'prepush-verification.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
assert not failures,'Credential pattern review required; values intentionally not printed'
