from pathlib import Path
import hashlib
import json
import re

work = Path(__file__).resolve().parent
root = work.parents[1]
review = root / 'docs/20261022-v5-language-review-v1.md'
data = json.loads((work / 'extracted-content.json').read_text(encoding='utf-8'))
baseline = json.loads((work / 'baseline-sha256.json').read_text(encoding='utf-8-sig'))
text_parts = []
for block in data['blocks']:
    if 'text' in block:
        text_parts.append(block['text'])
    else:
        text_parts.extend(cell for row in block['rows'] for cell in row)

quotes = re.findall(r'原文：\s*\n> ([^\n]+)', review.read_text(encoding='utf-8'))
quote_checks = [{'number': i, 'exact_match': any(q in t for t in text_parts)}
                for i, q in enumerate(quotes, 1)]
changed = []
for item in baseline:
    p = Path(item['Path'])
    actual = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    if actual != item['SHA256'].lower():
        changed.append(str(p))
source = Path(data['source'])
source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
result = {
    'review': str(review),
    'source_sha256': source_sha,
    'source_matches_extraction': source_sha == data['sha256'],
    'exact_quote_count': len(quotes),
    'quote_checks': quote_checks,
    'baseline_file_count': len(baseline),
    'changed_raw_or_output_files': changed,
    'passed': len(quotes) == 15 and all(q['exact_match'] for q in quote_checks)
              and not changed and source_sha == data['sha256']
}
(work / 'integrity-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in result.items() if k not in ('review', 'quote_checks')}, ensure_ascii=True, indent=2))
raise SystemExit(0 if result['passed'] else 1)
