from pathlib import Path
import subprocess, sys, json, datetime, os

work = Path(__file__).resolve().parent
stage = sys.argv[1]
container = os.environ.get('GARDEN_INSTALL_CONTAINER', 'memory-game6085-v7-install-20261022')
script = work / (stage + '.sh')
subprocess.run(['docker', 'exec', container, 'mkdir', '-p', '/lab'], check=True)
subprocess.run(['docker', 'cp', str(script), container+':/lab/'+script.name], check=True)
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (work/(stage+'.txt')).open('w',encoding='utf-8') as out:
    out.write('Actual command: docker exec '+container+' bash /lab/'+script.name+'\n')
    out.write('Started UTC: '+start+'\n\n'); out.flush()
    proc = subprocess.run(['docker','exec',container,'bash','/lab/'+script.name],stdout=out,stderr=subprocess.STDOUT)
    out.write('\nActual exit code: '+str(proc.returncode)+'\n')
(work/(stage+'-result.json')).write_text(json.dumps({'stage':stage,'exit_code':proc.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2),encoding='utf-8')
print(stage,'exit code',proc.returncode)
sys.exit(proc.returncode)
