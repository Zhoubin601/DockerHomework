from pathlib import Path
import re
import subprocess
import sys

p = Path(__file__).resolve().parent
stage = sys.argv[1]
log = (p / (stage + '.txt')).read_text()
assert 'Script done on ' in log and 'COMMAND_EXIT_CODE="0"' in log, stage + ' is not complete'
tree = subprocess.check_output(['xwininfo', '-display', ':99', '-root', '-tree'], text=True)
match = re.search(r'(0x[0-9a-f]+) "memory-game6085 v3 \| ' + re.escape(stage) + '"', tree)
assert match, 'Live terminal window missing'
subprocess.run(['import', '-display', ':99', '-window', match.group(1), str(p / (stage + '.png'))], check=True)
print(stage + ': actual terminal window captured')
