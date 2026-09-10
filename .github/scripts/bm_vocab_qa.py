from pathlib import Path
import re, subprocess, tempfile

ROOT=Path('.')
themes=sorted(ROOT.glob('t*.html'))
errors=[]
changed=[]

# DBP/PRPM 核对：固定表达应为“bulat air kerana pembetung, bulat kata kerana muafakat”。
t30=ROOT/'t30-ungkapan-peribahasa-full-master.html'
if t30.exists():
    t=t30.read_text(encoding='utf-8')
    old=t
    t=t.replace('bulat air kerana pembetung, bulat manusia kerana muafakat','bulat air kerana pembetung, bulat kata kerana muafakat')
    t=t.replace('圆水因为水渠，圆人因为协商','水因管道而汇聚，意见因协商而一致')
    if t!=old:
        t30.write_text(t,encoding='utf-8')
        changed.append(t30.name)

if len(themes)!=30: errors.append(f'expected 30 theme files, found {len(themes)}')
for p in themes:
    t=p.read_text(encoding='utf-8')
    if 'href="index.html"' not in t: errors.append(p.name+': no home link')
    if '<html' not in t.lower() or '</html>' not in t.lower(): errors.append(p.name+': bad html shell')
    for bad in ['Vocabulary Master','Vocabulary Full Master','Form 1','Form 2','Form 3','Form 4','Form 5','Food：','Nutrition：','Consumer：','�']:
        if bad in t: errors.append(p.name+': residue '+bad)

idx=(ROOT/'index.html').read_text(encoding='utf-8')
hrefs=re.findall(r'href=["\']([^"\']+\.html)',idx)
linked={Path(x).name for x in hrefs if Path(x).name.startswith('t')}
actual={p.name for p in themes}
if linked!=actual:
    for x in sorted(actual-linked): errors.append('index missing link: '+x)
    for x in sorted(linked-actual): errors.append('index broken theme link: '+x)

for p in themes+[ROOT/'index.html']:
    t=p.read_text(encoding='utf-8')
    for n,s in enumerate(re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',t,re.S|re.I),1):
        if not s.strip(): continue
        with tempfile.NamedTemporaryFile('w',suffix='.js',encoding='utf-8',delete=False) as f:
            f.write(s); name=f.name
        r=subprocess.run(['node','--check',name],capture_output=True,text=True)
        Path(name).unlink(missing_ok=True)
        if r.returncode: errors.append(f'{p.name}: script {n} syntax error')

for p in themes:
    t=p.read_text(encoding='utf-8')
    m=re.search(r'const raw=`(.*?)`;',t,re.S)
    if m:
        lines=[ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
        if len(lines)!=10 or any(len(ln.split('|'))!=11 for ln in lines):
            errors.append(p.name+': raw structure incomplete')

t06=ROOT/'t06-sekolah-pendidikan-full-master.html'
if t06.exists():
    t=t06.read_text(encoding='utf-8')
    starts=list(re.finditer(r'<details class="section" id="([A-J])"',t))
    if len(starts)!=10: errors.append('T06 section count')
    for i,m in enumerate(starts):
        letter=m.group(1); end=starts[i+1].start() if i+1<len(starts) else len(t)
        lv=set(re.findall(r'class="level l([1-8])"',t[m.start():end]))
        req={'7','8'} if letter=='J' else set('12345678')
        if not req.issubset(lv): errors.append('T06-'+letter+' missing levels')

if t30.exists():
    low=t30.read_text(encoding='utf-8').lower()
    for term in ['simpulan bahasa','perumpamaan','pepatah','bidalan','perbilangan','kata-kata hikmat','contoh pembelajaran']:
        if term not in low: errors.append('T30 missing '+term)
    if 'bulat manusia kerana muafakat' in low: errors.append('T30 obsolete proverb wording remains')

print('CHANGED:', ', '.join(changed) if changed else 'none')
if errors:
    print('QA ERRORS')
    print('\n'.join('- '+x for x in errors))
    raise SystemExit(1)
print('QA PASS: 30 themes, links, JS, structures, T30 DBP wording')
