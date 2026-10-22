from pathlib import Path
import collections, hashlib, json, re, urllib.request, zipfile, io

root = Path(__file__).resolve().parents[2]
work = Path(__file__).resolve().parent
sha = lambda b:hashlib.sha256(b).hexdigest()
audit = json.loads((work/'package-audit.json').read_text(encoding='utf-8'))
result = {'rawAndOutputUnchanged':all((root/p).is_file() and sha((root/p).read_bytes()) == h for p,h in audit['baseline'].items())}
with zipfile.ZipFile(root/'Code/memory-game6085/backend/target/memory-game6085.jar') as built, zipfile.ZipFile(work/'unpacked/memory-game6085/dist-artifacts/memory-game6085.jar') as release:
    a={p:sha(built.read(p)) for p in built.namelist() if p.startswith('BOOT-INF/') and not p.endswith('/')}
    b={p:sha(release.read(p)) for p in release.namelist() if p.startswith('BOOT-INF/') and not p.endswith('/')}
    result['sourceBuildVsDeliveryBOOT_INF']={'entriesBuilt':len(a),'entriesDelivery':len(b),'differences':[p for p in a.keys()|b.keys() if a.get(p)!=b.get(p)]}
with zipfile.ZipFile(root/'output/v4/20261021-docker-evidence-v4.zip') as z:
    manifest=json.loads(z.read('manifest-sha256.json'))
    result['evidenceManifestEntries']=len(manifest)
    result['evidenceManifestValid']=all(len(z.read(p))==info['bytes'] and sha(z.read(p))==info['sha256'] for p,info in manifest.items())
health=json.load(urllib.request.urlopen('http://127.0.0.1:18080/api/health',timeout=5))
after=json.load(urllib.request.urlopen('http://127.0.0.1:18080/api/leaderboard?difficulty=easy',timeout=5))
before=json.loads((work/'before-restart.json').read_text(encoding='utf-8'))
(work/'after-restart.json').write_text(json.dumps(after,ensure_ascii=False,indent=2),encoding='utf-8')
result['jarRestart']={'health':health,'leaderboardPreserved':after==before,'total':after['total']}
schema=(work/'v4-schema-validation.txt').read_text(encoding='utf-8-sig')
result['wordSchemaErrors']=collections.Counter(re.findall(r'\[Schema\] (.+)',schema))
result['wordSchemaErrorTotal']=sum(result['wordSchemaErrors'].values())
(work/'final-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
