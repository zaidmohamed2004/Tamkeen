"""Checks M2 traceability coverage. Run: python3 docs/traceability/check_traceability.py (from repo root).
Fails (exit 1) when a QAS from M1 has no row, an element is not in docs/elements.yaml, an element never appears
in any diagram source, a tactic is not in the catalog, an ADR file is missing, an ADR is never traced,
or an M3 test id is missing or duplicated."""
import csv, glob, os, re, sys
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def ylist(path):
    out = {}
    key = None
    for line in open(path):
        if line.strip().startswith('#') or not line.strip(): continue
        m = re.match(r'^(\w+):\s*(\[.*\])?\s*$', line)
        if m:
            key = m.group(1); out[key] = []
            if m.group(2): out[key] = [x.strip() for x in m.group(2)[1:-1].split(',')]
            continue
        m = re.match(r'^\s+-\s+(.+)$', line)
        if m and key: out[key].append(m.group(1).strip())
    return out
vocab = {n for v in ylist(os.path.join(root, 'docs/elements.yaml')).values() for n in v}
tactics = {n for v in ylist(os.path.join(root, 'docs/traceability/tactics.yaml')).values() for n in v}
diagrams = ''.join(open(f).read() for f in glob.glob(os.path.join(root, 'docs/diagrams/*.mmd')))
adr_files = {re.match(r'(adr-\d{3})', os.path.basename(f)).group(1).upper() for f in glob.glob(os.path.join(root, 'docs/adr/adr-*.md'))}
rows = list(csv.DictReader(open(os.path.join(root, 'docs/traceability/traceability.csv'))))
errors = []; seen_tests = set(); traced_adrs = set()
expected = [f'QAS-{i}' for i in range(1, 9)]
for q in expected:
    if q not in [r['qas'] for r in rows]: errors.append(f'{q}: no traceability row')
for r in rows:
    q = r['qas']
    for col in ['elements', 'tactics', 'adrs', 'm3_test_id', 'm3_test']:
        if not r[col].strip(): errors.append(f'{q}: empty {col}')
    for e in [x.strip() for x in r['elements'].split(';')]:
        if e not in vocab: errors.append(f'{q}: element "{e}" not in elements.yaml')
        elif e not in diagrams: errors.append(f'{q}: element "{e}" not shown in any diagram')
    for t in [x.strip() for x in r['tactics'].split(';')]:
        if t not in tactics: errors.append(f'{q}: tactic "{t}" not in tactics.yaml')
    for a in [x.strip() for x in r['adrs'].split(';')]:
        traced_adrs.add(a)
        if a not in adr_files: errors.append(f'{q}: {a} has no file in docs/adr')
    if r['m3_test_id'] in seen_tests: errors.append(f'{q}: duplicate test id {r["m3_test_id"]}')
    seen_tests.add(r['m3_test_id'])
for a in sorted(adr_files - traced_adrs): errors.append(f'{a}: not traced to any QAS')
unused = sorted(n for n in vocab if n not in diagrams)
print(f'rows: {len(rows)}  QAS covered: {len([q for q in expected if q in [r["qas"] for r in rows]])}/8  ADRs traced: {len(traced_adrs & adr_files)}/{len(adr_files)}  tests: {len(seen_tests)}')
print('vocabulary elements missing from diagrams:', unused if unused else 'none')
if errors:
    print('FAIL'); [print(' -', e) for e in errors]; sys.exit(1)
print('PASS: every QAS traces to elements, tactics, ADRs and an M3 test')
