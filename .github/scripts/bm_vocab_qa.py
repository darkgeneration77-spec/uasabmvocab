from pathlib import Path
import re

ROOT = Path('.')
files = sorted(ROOT.glob('t*.html')) + [ROOT / 'index.html']

# 统一学生可见语言。保留 MPT4 / UASA / SPM 等官方缩写。
generic = [
    ('BM Vocabulary Full Master', '马来文词汇'),
    ('BM Vocabulary Master', '马来文词汇'),
    ('Bahasa Melayu Vocabulary Master', 'Bahasa Melayu｜马来文词汇'),
    ('Vocabulary Full Master', '马来文词汇'),
    ('Vocabulary Master', '马来文词汇'),
    ('BM + 华语义', '马来文 + 华语'),
    ('Form 4–5', 'Tingkatan 4–5'),
    ('Form 1–5', 'Tingkatan 1–5'),
    ('Form 1', 'Tingkatan 1'),
    ('Form 2', 'Tingkatan 2'),
    ('Form 3', 'Tingkatan 3'),
    ('Form 4', 'Tingkatan 4'),
    ('Form 5', 'Tingkatan 5'),
]

# 第二轮课程词汇 QA：删除不必要的专业术语，改成更符合学校 Bahasa Melayu
# 阅读、理解与写作语境的标准表达。不是把这些词宣称为“DSKP 官方逐词表”。
specific = {
    't07-kesihatan-full-master.html': [
        ('diagnosis', 'pengenalpastian masalah kesihatan'),
        ('诊断', '识别健康问题'),
        ('tingkah laku sedentari', 'gaya hidup kurang aktif'),
        ('久坐行为', '缺少活动的生活方式'),
        ('kecergasan kardiorespiratori', 'kecergasan jantung dan paru-paru'),
        ('心肺适能', '心肺体能'),
        ('sokongan psikososial', 'sokongan emosi dan sosial'),
        ('心理社会支持', '情绪与社会支持'),
        ('intervensi awal', 'tindakan awal'),
        ('早期干预', '及早采取行动'),
        ('literasi pemakanan', 'pengetahuan pemakanan'),
        ('营养素养', '营养知识'),
        ('kesihatan populasi', 'kesihatan masyarakat'),
        ('群体健康', '社会健康'),
        ('beban penyakit', 'kesan penyakit terhadap masyarakat'),
        ('疾病负担', '疾病对社会的影响'),
    ],
    't08-kebersihan-full-master.html': [
        ('ekonomi kitaran', 'guna semula dan kitar semula'),
        ('循环经济', '重复使用与回收'),
    ],
    't09-keselamatan-full-master.html': [
        ('mitigasi risiko', 'pengurangan risiko'),
        ('降低风险', '降低风险'),
        ('kerangka keselamatan', 'panduan keselamatan'),
        ('安全框架', '安全指南'),
        ('pengurusan risiko bersepadu', 'pengurusan risiko menyeluruh'),
        ('综合风险管理', '全面风险管理'),
        ('ketahanan keselamatan', 'kesiapsiagaan keselamatan'),
        ('安全韧性', '安全应对能力'),
    ],
    't10-makanan-pemakanan-full-master.html': [
        ('penilaian sensori', 'penilaian rasa dan tekstur'),
        ('感官评价', '味道与口感评价'),
        ('kualiti sensori', 'kualiti rasa dan tekstur'),
        ('感官品质', '味道与口感品质'),
        ('literasi pemakanan', 'pengetahuan pemakanan'),
        ('营养素养', '营养知识'),
        ('identiti kulinari', 'identiti makanan tempatan'),
        ('饮食身份', '本地饮食特色'),
        ('industri gastronomi', 'industri makanan tempatan'),
        ('美食产业', '本地食品产业'),
        ('malpemakanan', 'pemakanan tidak seimbang'),
        ('营养不良', '营养失衡'),
        ('sistem makanan mampan', 'pengurusan makanan secara mampan'),
        ('可持续食物系统', '可持续食品管理'),
    ],
    't11-alam-sekitar-full-master.html': [
        ('perkhidmatan ekosistem', 'manfaat ekosistem'),
        ('生态系统服务', '生态系统带来的益处'),
        ('daya tampung alam', 'keupayaan alam'),
        ('环境承载力', '自然环境承受能力'),
        ('ekonomi kitaran', 'guna semula dan kitar semula'),
        ('循环利用概念', '重复使用与回收'),
        ('koridor ekologi', 'laluan hidupan liar'),
        ('生态走廊', '野生动物通道'),
    ],
    't12-haiwan-tumbuhan-full-master.html': [
        ('fragmentasi habitat', 'pemecahan habitat'),
        ('栖息地破碎化', '栖息地被分割'),
        ('konservasi biodiversiti', 'pemuliharaan biodiversiti'),
        ('生物多样性保育', '生物多样性保育'),
        ('pusat konservasi', 'pusat pemuliharaan'),
        ('保育中心', '保育中心'),
        ('spesies invasif', 'spesies asing yang mengancam'),
        ('入侵物种', '具威胁性的外来物种'),
        ('eksploitasi sumber', 'penggunaan sumber secara berlebihan'),
        ('资源过度开发', '过度使用资源'),
    ],
    't13-cuaca-alam-full-master.html': [
        ('mitigasi risiko', 'pengurangan risiko'),
        ('mitigasi perubahan iklim', 'usaha mengurangkan kesan perubahan iklim'),
        ('减缓气候变化', '减少气候变化影响的措施'),
        ('adaptasi iklim', 'penyesuaian terhadap perubahan iklim'),
        ('气候适应', '适应气候变化'),
        ('dinamik atmosfera', 'perubahan atmosfera'),
        ('大气变化', '大气变化'),
        ('interpretasi data', 'tafsiran data'),
        ('数据解读', '数据解读'),
    ],
    't15-kemudahan-awam-full-master.html': [
        ('standard aksesibiliti', 'standard kebolehcapaian'),
        ('无障碍标准', '无障碍使用标准'),
        ('pengurusan fasiliti', 'pengurusan kemudahan'),
        ('设施管理', '设施管理'),
    ],
    't16-pengangkutan-jalan-raya-full-master.html': [
        ('pengoptimuman trafik', 'penambahbaikan aliran trafik'),
        ('优化交通', '改善交通流动'),
    ],
    't18-teknologi-komunikasi-full-master.html': [
        ('keterangkuman digital', 'akses digital untuk semua'),
        ('数字包容', '让所有人获得数字资源'),
        ('akauntabiliti dalam talian', 'tanggungjawab dalam talian'),
        ('网络责任', '网络责任'),
        ('kewarganegaraan digital', 'tanggungjawab sebagai pengguna digital'),
        ('数字公民意识', '数字使用者责任'),
        ('kendiri digital', 'pembelajaran kendiri secara digital'),
        ('数字自主能力', '数字自主学习能力'),
    ],
    't19-pekerjaan-full-master.html': [
        ('ekosistem pekerjaan', 'dunia pekerjaan'),
        ('就业生态', '职场环境'),
        ('kebertanggungjawaban', 'tanggungjawab'),
        ('责任意识', '责任'),
        ('mobiliti kerjaya', 'pergerakan kerjaya'),
        ('职业流动', '职业变化与发展'),
    ],
    't21-kebudayaan-warisan-full-master.html': [
        ('identiti kulinari', 'identiti makanan tempatan'),
        ('饮食文化身份', '本地饮食特色'),
        ('pelancongan gastronomi', 'pelancongan makanan'),
        ('美食旅游', '饮食旅游'),
        ('pentauliahan', 'pengiktirafan'),
    ],
}

changed = []
for path in files:
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    old = text
    for a, b in generic:
        text = text.replace(a, b)
    for a, b in specific.get(path.name, []):
        text = text.replace(a, b)

    # 可见首页的 Level 改成马来文/华语；内部 JS 变量名不动。
    if path.name == 'index.html':
        text = text.replace('学习的 Level', '学习的等级（L1–L8）')
        text = text.replace('Level。', '等级（L1–L8）。')

    if text != old:
        path.write_text(text, encoding='utf-8')
        changed.append(path.name)

# 静态完整性检查。人类喜欢把网页做成一团线，所以至少让机器先抓最明显的坑。
errors = []
for path in sorted(ROOT.glob('t*.html')):
    text = path.read_text(encoding='utf-8')
    if 'href="index.html"' not in text:
        errors.append(f'{path.name}: missing home link')
    if '<html' not in text.lower() or '</html>' not in text.lower():
        errors.append(f'{path.name}: incomplete html shell')
    # 不允许这些明显裸英文学生标签残留。
    for bad in ['Vocabulary Master', 'Vocabulary Full Master', 'Form 1', 'Form 2', 'Form 3', 'Form 4', 'Form 5']:
        if bad in text:
            errors.append(f'{path.name}: visible/embedded label remains: {bad}')

print('CHANGED:', ', '.join(changed) if changed else 'none')
if errors:
    print('QA ERRORS:')
    for e in errors:
        print('-', e)
    raise SystemExit(1)
print('QA PASS:', len(list(ROOT.glob('t*.html'))), 'theme files checked')
