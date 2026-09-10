from pathlib import Path
p=Path('index.html')
t=p.read_text(encoding='utf-8')
old=t
# Make the old box clearly theme-only search.
t=t.replace('Cari tema / 搜索主题，例如 kesihatan、环境、imbuhan、因果','Cari tema / 搜索主题，例如 kesihatan、环境、imbuhan、因果')
# Add external vocabulary search script once, preserving the original page.
tag='<script src="vocab-search.js"></script>'
if tag not in t:
    t=t.replace('</body>',tag+'</body>')
if t==old:
    print('No index change needed')
else:
    p.write_text(t,encoding='utf-8')
    print('Added vocab-search.js to index.html')
