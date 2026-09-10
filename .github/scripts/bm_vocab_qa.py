from pathlib import Path
import re

ROOT = Path('.')
theme_files = sorted(ROOT.glob('t*.html'))
changed = []

# T06 第二轮内容补齐：原页 B/C/E/F/G/H/I 从 Tahun 5–6 直接跳到 Tingkatan 2。
# 这里补上 Tingkatan 1，保持原版式，不重做页面。
t06 = ROOT / 't06-sekolah-pendidikan-full-master.html'
if t06.exists():
    text = t06.read_text(encoding='utf-8')
    old = text
    additions = {
        'B': '<div class="level l4"><h3>L4｜Tingkatan 1</h3><div class="grid"><div class="item"><div class="bm">mencatat isi penting</div><div class="zh">记录重点</div></div><div class="item"><div class="bm">membuat ringkasan</div><div class="zh">作摘要</div></div><div class="item"><div class="bm">mengemukakan soalan</div><div class="zh">提出问题</div></div><div class="item"><div class="bm">memberikan penjelasan</div><div class="zh">给予说明</div></div><div class="item"><div class="bm">membentangkan maklumat</div><div class="zh">呈现资料</div></div><div class="item"><div class="bm">berbincang dalam kumpulan</div><div class="zh">小组讨论</div></div><div class="item"><div class="bm">membuat rujukan</div><div class="zh">查阅参考资料</div></div><div class="item"><div class="bm">menyusun maklumat</div><div class="zh">整理资料</div></div></div></div>',
        'C': '<div class="level l4"><h3>L4｜Tingkatan 1</h3><div class="grid"><div class="item"><div class="bm">artikel</div><div class="zh">文章</div></div><div class="item"><div class="bm">bahan digital</div><div class="zh">数字材料</div></div><div class="item"><div class="bm">sumber dalam talian</div><div class="zh">线上资源</div></div><div class="item"><div class="bm">kamus digital</div><div class="zh">电子词典</div></div><div class="item"><div class="bm">infografik</div><div class="zh">信息图</div></div><div class="item"><div class="bm">persembahan digital</div><div class="zh">数字演示</div></div><div class="item"><div class="bm">bahan multimedia</div><div class="zh">多媒体材料</div></div><div class="item"><div class="bm">sumber rujukan</div><div class="zh">参考资源</div></div></div></div>',
        'E': '<div class="level l4"><h3>L4｜Tingkatan 1</h3><div class="grid"><div class="item"><div class="bm">sasaran pembelajaran</div><div class="zh">学习目标</div></div><div class="item"><div class="bm">kemajuan diri</div><div class="zh">个人进步</div></div><div class="item"><div class="bm">kekuatan diri</div><div class="zh">个人强项</div></div><div class="item"><div class="bm">kelemahan diri</div><div class="zh">个人弱项</div></div><div class="item"><div class="bm">usaha yang konsisten</div><div class="zh">持续努力</div></div><div class="item"><div class="bm">mencapai matlamat</div><div class="zh">达到目标</div></div><div class="item"><div class="bm">memperbaiki prestasi</div><div class="zh">改善表现</div></div><div class="item"><div class="bm">menilai kemajuan</div><div class="zh">评估进展</div></div></div></div>',
        'F': '<div class="level l4"><h3>L4｜Tingkatan 1</h3><div class="grid"><div class="item"><div class="bm">disiplin diri</div><div class="zh">自律</div></div><div class="item"><div class="bm">mematuhi peraturan sekolah</div><div class="zh">遵守校规</div></div><div class="item"><div class="bm">menepati masa</div><div class="zh">守时</div></div><div class="item"><div class="bm">bertanggungjawab terhadap tindakan</div><div class="zh">为自己的行为负责</div></div><div class="item"><div class="bm">menghormati warga sekolah</div><div class="zh">尊重学校成员</div></div><div class="item"><div class="bm">menjaga harta benda sekolah</div><div class="zh">爱护学校财物</div></div><div class="item"><div class="bm">mengelakkan salah laku</div><div class="zh">避免不当行为</div></div><div class="item"><div class="bm">menerima teguran</div><div class="zh">接受劝告与纠正</div></div></div></div>',
        'G': '<div class="level l4"><h3>L4｜Tingkatan 1</h3><div class="grid"><div class="item"><div class="bm">bimbingan akademik</div><div class="zh">学业指导</div></div><div class="item"><div class="bm">nasihat guru</div><div class="zh">教师劝导</div></div><div class="item"><div class="bm">sokongan pembelajaran</div><div class="zh">学习支持</div></div><div class="item"><div class="bm">galakan</div><div class="zh">鼓励</div></div><div class="item"><div class="bm">maklum balas</div><div class="zh">反馈</div></div><div class="item"><div class="bm">pemantauan perkembangan</div><div class="zh">跟进学习进展</div></div><div class="item"><div class="bm">kaunseling</div><div class="zh">辅导</div></div><div class="item"><div class="bm">bantuan pembelajaran</div><div class="zh">学习援助</div></div></div></div>',
        'H': '<div class="level l4"><h3>L4｜Tingkatan 1</h3><div class="grid"><div class="item"><div class="bm">kurang tumpuan</div><div class="zh">专注不足</div></div><div class="item"><div class="bm">kurang motivasi</div><div class="zh">缺乏动力</div></div><div class="item"><div class="bm">pengurusan masa yang lemah</div><div class="zh">时间管理不佳</div></div><div class="item"><div class="bm">tekanan pembelajaran</div><div class="zh">学习压力</div></div><div class="item"><div class="bm">kesukaran memahami pelajaran</div><div class="zh">难以理解课业</div></div><div class="item"><div class="bm">gangguan media sosial</div><div class="zh">社交媒体干扰</div></div><div class="item"><div class="bm">kurang sokongan</div><div class="zh">缺少支持</div></div><div class="item"><div class="bm">mendapatkan bantuan</div><div class="zh">寻求帮助</div></div></div></div>',
        'I': '<div class="level l4"><h3>L4｜Tingkatan 1</h3><div class="grid"><div class="item"><div class="bm">kepentingan pendidikan</div><div class="zh">教育的重要性</div></div><div class="item"><div class="bm">menambah pengetahuan</div><div class="zh">增加知识</div></div><div class="item"><div class="bm">meningkatkan kemahiran</div><div class="zh">提升技能</div></div><div class="item"><div class="bm">membentuk sahsiah</div><div class="zh">塑造品格</div></div><div class="item"><div class="bm">mengembangkan potensi diri</div><div class="zh">发展个人潜能</div></div><div class="item"><div class="bm">membina keyakinan diri</div><div class="zh">建立自信</div></div><div class="item"><div class="bm">membuka peluang</div><div class="zh">创造机会</div></div><div class="item"><div class="bm">membina masa depan</div><div class="zh">建设未来</div></div></div></div>'
    }
    starts = list(re.finditer(r'<details class="section" id="([A-J])"', text))
    # 倒序处理，避免插入后索引位移。
    for idx in range(len(starts)-1, -1, -1):
        m = starts[idx]
        letter = m.group(1)
        if letter not in additions:
            continue
        end = starts[idx+1].start() if idx+1 < len(starts) else len(text)
        block = text[m.start():end]
        if 'class="level l4"' in block:
            continue
        pos_rel = block.find('<div class="level l5">')
        if pos_rel == -1:
            continue
        pos = m.start() + pos_rel
        text = text[:pos] + additions[letter] + text[pos:]
    if text != old:
        t06.write_text(text, encoding='utf-8')
        changed.append(t06.name)

# 基本完整性与残留检查。
errors = []
for path in theme_files:
    text = path.read_text(encoding='utf-8')
    if 'href="index.html"' not in text:
        errors.append(f'{path.name}: missing home link')
    if '<html' not in text.lower() or '</html>' not in text.lower():
        errors.append(f'{path.name}: incomplete html shell')
    for bad in ['Vocabulary Master','Vocabulary Full Master','Form 1','Form 2','Form 3','Form 4','Form 5','�']:
        if bad in text:
            errors.append(f'{path.name}: forbidden residue: {bad}')

# T30 类别完整性。
t30 = ROOT / 't30-ungkapan-peribahasa-full-master.html'
if t30.exists():
    low = t30.read_text(encoding='utf-8').lower()
    for item in ['simpulan bahasa','perumpamaan','pepatah','bidalan','perbilangan','kata-kata hikmat']:
        if item not in low:
            errors.append(f'{t30.name}: missing peribahasa category: {item}')

# T06 覆盖必须补齐；J 是高阶专页，只要求 L7-L8。
if t06.exists():
    text = t06.read_text(encoding='utf-8')
    starts = list(re.finditer(r'<details class="section" id="([A-J])"', text))
    print('T06 LEVEL COVERAGE')
    for idx, m in enumerate(starts):
        letter = m.group(1)
        end = starts[idx+1].start() if idx+1 < len(starts) else len(text)
        block = text[m.start():end]
        levels = sorted(set(re.findall(r'class="level l([1-8])"', block)))
        print(letter + ': ' + ','.join('L'+x for x in levels))
        required = ['7','8'] if letter == 'J' else [str(i) for i in range(1,9)]
        missing = [x for x in required if x not in levels]
        if missing:
            errors.append(f'T06-{letter}: missing ' + ','.join('L'+x for x in missing))

# 所有 raw-string 页面必须有 10 个主题且每主题 8 个等级。
print('RAW PAGE COVERAGE')
for path in theme_files:
    text = path.read_text(encoding='utf-8')
    m = re.search(r'const raw=`(.*?)`;', text, re.S)
    if not m:
        continue
    lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]
    malformed = [ln.split('|')[0] for ln in lines if len(ln.split('|')) != 11]
    print(f'{path.name}: {len(lines)} sections; malformed={",".join(malformed) if malformed else "none"}')
    if len(lines) != 10 or malformed:
        errors.append(f'{path.name}: raw section/level structure incomplete')

print('CHANGED:', ', '.join(changed) if changed else 'none')
if errors:
    print('QA ERRORS:')
    for e in errors:
        print('-', e)
    raise SystemExit(1)
print('QA PASS:', len(theme_files), 'theme files checked')
