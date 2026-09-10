from pathlib import Path
import re

ROOT = Path('.')
theme_files = sorted(ROOT.glob('t*.html'))
changed = []

# 第二轮剩余术语清理：T11 统一采用学校教材更常见的“pemuliharaan”。
t11 = ROOT / 't11-alam-sekitar-full-master.html'
if t11.exists():
    text = t11.read_text(encoding='utf-8')
    old = text
    text = text.replace('konservasi', 'pemuliharaan')
    if text != old:
        t11.write_text(text, encoding='utf-8')
        changed.append(t11.name)

errors = []
for path in theme_files:
    text = path.read_text(encoding='utf-8')
    if 'href="index.html"' not in text:
        errors.append(f'{path.name}: missing home link')
    if '<html' not in text.lower() or '</html>' not in text.lower():
        errors.append(f'{path.name}: incomplete html shell')
    for bad in ['Vocabulary Master', 'Vocabulary Full Master', 'Form 1', 'Form 2', 'Form 3', 'Form 4', 'Form 5', '�']:
        if bad in text:
            errors.append(f'{path.name}: forbidden residue: {bad}')

# 高阶词只报告，不机械删除。literasi 在 KPM 当前教育语境中可保留。
suspects = [
    'psikososial','kardiorespiratori','mitigasi','sensori','gastronomi','kulinari',
    'ekonomi kitaran','daya tampung','aksesibiliti','pengoptimuman','keterangkuman',
    'kewarganegaraan digital','kebertanggungjawaban','fragmentasi','konservasi','invasif',
    'eksploitasi','dinamik atmosfera','interpretasi','ekosistem pekerjaan','malpemakanan',
    'proksimal','korelasi','sistemik','sinergi','trade-off','Causality','fair play','register'
]
print('SUSPECT TERM REPORT')
for path in theme_files:
    low = path.read_text(encoding='utf-8').lower()
    hits = sorted({t for t in suspects if t.lower() in low})
    if hits:
        print(path.name + ': ' + ', '.join(hits))

# T30 只检查 DSKP 中 peribahasa 的主要类别是否齐全。
t30 = ROOT / 't30-ungkapan-peribahasa-full-master.html'
if t30.exists():
    low = t30.read_text(encoding='utf-8').lower()
    for item in ['simpulan bahasa','perumpamaan','pepatah','bidalan','perbilangan','kata-kata hikmat']:
        if item not in low:
            errors.append(f'{t30.name}: missing peribahasa category: {item}')

# T06 是静态大页，逐 A-J 检查是否缺失 L1-L8。J 本来专注高阶议题，允许只出现 L7-L8。
t06 = ROOT / 't06-sekolah-pendidikan-full-master.html'
if t06.exists():
    text = t06.read_text(encoding='utf-8')
    print('T06 LEVEL COVERAGE')
    starts = list(re.finditer(r'<details class="section" id="([A-J])"', text))
    for idx, m in enumerate(starts):
        letter = m.group(1)
        end = starts[idx+1].start() if idx+1 < len(starts) else len(text)
        block = text[m.start():end]
        levels = sorted(set(re.findall(r'class="level l([1-8])"', block)))
        print(letter + ': ' + ','.join('L'+x for x in levels))
        if letter != 'J':
            missing = [str(i) for i in range(1,9) if str(i) not in levels]
            if missing:
                print('MISSING ' + letter + ': ' + ','.join('L'+x for x in missing))

# JS raw-string pages：每一主题行通常为 id + 标题 + 华语 + 8 个等级，共 11 栏。
print('RAW PAGE COVERAGE')
for path in theme_files:
    text = path.read_text(encoding='utf-8')
    m = re.search(r'const raw=`(.*?)`;', text, re.S)
    if not m:
        continue
    bad = []
    lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
    for ln in lines:
        parts = ln.split('|')
        if len(parts) != 11:
            bad.append(parts[0] if parts else '?')
    print(f'{path.name}: {len(lines)} sections; malformed={",".join(bad) if bad else "none"}')

print('CHANGED:', ', '.join(changed) if changed else 'none')
if errors:
    print('QA ERRORS:')
    for e in errors:
        print('-', e)
    raise SystemExit(1)
print('QA PASS:', len(theme_files), 'theme files checked')
