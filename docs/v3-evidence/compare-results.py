from pathlib import Path
import json
p = Path(__file__).resolve().parent
before = json.loads((p / 'before-leaderboard.json').read_text())
after = json.loads((p / 'after-leaderboard.json').read_text())
old = (p / 'before-container.txt').read_text().strip()
new = (p / 'after-container.txt').read_text().strip()
same = before == after
assert same and old != new
print('LeaderboardPreserved=True ContainerChanged=True')
print('OldContainer=' + old[:12] + ' NewContainer=' + new[:12])
