from pathlib import Path
import re, subprocess, tempfile

ROOT=Path('.')
themes=sorted(ROOT.glob('t*.html'))
errors=[]
print('THEME COUNT',len(themes))
if len(themes)!=30: errors.append(f'expected 30 theme files, found {len(themes)}')

# 基础壳、主页链接、可见残留。
for p in themes:
    t=p.read_text(encoding='utf-8')
    if 'href="index.html"' not in t: errors.append(p.name+': no home link')
    if '<html' not in t.lower() or '</html>' not in t.lower(): errors.append(p.name+': bad html shell')
    for bad in ['Vocabulary Master','Vocabulary Full Master','Form 1','Form 2','Form 3','Form 4','Form 5','Food：','Nutrition：','Consumer：','�']:
        if bad in t: errors.append(p.name+': residue '+bad)

# 首页 30 个主题链接必须全部存在，而且不能指向不存在文件。
idx=(ROOT/'index.html').read_text(encoding='utf-8')
hrefs=re.findall(r'href=["\']([^"\']+\.html)',idx)
linked={Path(x).name for x in hrefs if Path(x).name.startswith('t')}
actual={p.name for p in themes}
print('INDEX THEME LINKS',len(linked))
for x in sorted(actual-linked): errors.append('index missing link: '+x)
for x in sorted(linked-actual): errors.append('index broken theme link: '+x)

# Inline JavaScript syntax check。DOM 是否存在是浏览器层面；这里先抓引号/模板字串等语法破损。
print('JAVASCRIPT SYNTAX')
for p in themes+[ROOT/'index.html']:
    t=p.read_text(encoding='utf-8')
    scripts=re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',t,re.S|re.I)
    for n,s in enumerate(scripts,1):
        if not s.strip(): continue
        with tempfile.NamedTemporaryFile('w',suffix='.js',encoding='utf-8',delete=False) as f:
            f.write(s); name=f.name
        r=subprocess.run(['node','--check',name],capture_output=True,text=True)
        Path(name).unlink(missing_ok=True)
        if r.returncode:
            errors.append(f'{p.name}: script {n} syntax error: '+r.stderr.splitlines()[-1])
print('JS checked')

# raw-string 型页面：10 个 A-J 主题，每个主题 8 个等级。
print('RAW STRUCTURE')
for p in themes:
    t=p.read_text(encoding='utf-8')
    m=re.search(r'const raw=`(.*?)`;',t,re.S)
    if not m: continue
    lines=[ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
    bad=[]
    for ln in lines:
        parts=ln.split('|')
        if len(parts)!=11: bad.append(parts[0] if parts else '?')
    print(p.name,len(lines),'sections','bad=',','.join(bad) or 'none')
    if len(lines)!=10 or bad: errors.append(p.name+': raw structure incomplete')

# T06 静态页覆盖。
t06=ROOT/'t06-sekolah-pendidikan-full-master.html'
if t06.exists():
    t=t06.read_text(encoding='utf-8')
    starts=list(re.finditer(r'<details class="section" id="([A-J])"',t))
    if len(starts)!=10: errors.append('T06: section count != 10')
    for i,m in enumerate(starts):
        letter=m.group(1); end=starts[i+1].start() if i+1<len(starts) else len(t)
        block=t[m.start():end]
        lv=set(re.findall(r'class="level l([1-8])"',block))
        req={'7','8'} if letter=='J' else set('12345678')
        if not req.issubset(lv): errors.append('T06-'+letter+': missing '+','.join(sorted(req-lv)))

# T30 的 DSKP peribahasa umbrella categories 必须保留。
t30=ROOT/'t30-ungkapan-peribahasa-full-master.html'
if t30.exists():
    low=t30.read_text(encoding='utf-8').lower()
    for term in ['simpulan bahasa','perumpamaan','pepatah','bidalan','perbilangan','kata-kata hikmat']:
        if term not in low: errors.append('T30 missing '+term)
    if 'contoh pembelajaran' not in low: errors.append('T30 missing teaching-example disclaimer')

# 仅报告可能过度专业的词，人工判断，不做词越简单越好的机械清洗。
watch=['psikososial','kardiorespiratori','mitigasi','sensori','gastronomi','kulinari','ekonomi kitaran','daya tampung','aksesibiliti','pengoptimuman','keterangkuman','kewarganegaraan digital','kebertanggungjawaban','fragmentasi','konservasi','invasif','eksploitasi','dinamik atmosfera','interpretasi','ekosistem pekerjaan','malpemakanan','proksimal','korelasi','sistemik','sinergi','trade-off','causality','fair play','register']
print('WATCH TERMS')
for p in themes:
    low=p.read_text(encoding='utf-8').lower()
    hits=[w for w in watch if w in low]
    if hits: print(p.name+': '+', '.join(hits))

if errors:
    print('QA ERRORS')
    print('\n'.join('- '+x for x in errors))
    raise SystemExit(1)
print('FINAL MECHANICAL QA PASS: 30 themes')
