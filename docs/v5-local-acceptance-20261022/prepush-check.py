"""Validate the staged acceptance evidence without printing credential values."""
from pathlib import Path
import hashlib, json, re, subprocess

W=Path(__file__).resolve().parent
R=W.parents[1]
def git(*args):
    return subprocess.check_output(['git',*args],cwd=R)
sha=lambda b:hashlib.sha256(b).hexdigest()
names=[n for n in git('diff','--cached','--name-only','-z','--diff-filter=ACMR').decode('utf-8').split('\0') if n]
assert names
assert not git('diff','--cached','--name-only','--diff-filter=D').strip()
assert not any(n.startswith(('raw/','output/','Code/','memory-bank/')) for n in names)
assert not any('/unpacked/' in n or n.endswith(('.jar','.docx','.html')) or n.endswith(('original-containers.json','original-containers.txt','final-containers.txt','docker-prepare.log','docker-roundtrip.log')) for n in names)
patterns={
    'private-key':rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'github-token':rb'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{25,}\b',
    'openai-key':rb'\bsk-(?:proj-)?[A-Za-z0-9_-]{28,}\b',
    'aws-access':rb'\bAKIA[0-9A-Z]{16}\b',
    'credential-assignment':rb'''(?i)\b(?:password|api[_-]?key|access[_-]?token|secret[_-]?key)\s*[:=]\s*["'][^"'\r\n]{8,}["']''',
}
sizes=[]
findings=[]
scanned=0
for n in names:
    b=git('show',':'+n)
    sizes.append({'path':n,'bytes':len(b)})
    assert len(b)<10*1024*1024,n
    if Path(n).suffix.lower() not in {'.png','.pdf'}:
        scanned+=1
        for label,pattern in patterns.items():
            if re.search(pattern,b): findings.append({'path':n,'rule':label})
assert not findings,'Credential review required; values intentionally not printed'
baseline=json.loads((W/'baseline-sha256.json').read_text(encoding='utf-8'))
assert all(sha((R/n).read_bytes())==h for n,h in baseline.items())
remote=git('rev-parse','origin/main').decode().strip()
head=git('rev-parse','HEAD').decode().strip()
assert remote==head,'Remote moved; inspect before committing'
result={'baseCommit':head,'stagedFiles':len(names),'stagedBytes':sum(s['bytes'] for s in sizes),'largestFile':max(sizes,key=lambda s:s['bytes']),'textFilesScanned':scanned,'credentialPatternFailures':findings,'rawAndOutputUnchanged':len(baseline),'temporaryDuplicatesExcluded':True,'unrelatedContainerDetailsExcluded':True}
(W/'prepush-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True,indent=2))
