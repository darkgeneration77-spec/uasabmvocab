(()=>{
const files=[
['T01','t01-kata-kerja.html'],['T02','t02-kata-adjektif-full-master-v2-unified.html'],['T03','t03-perasaan-emosi-full-master.html'],['T04','t04-perwatakan-full-master.html'],['T05','t05-keluarga-full-master.html'],['T06','t06-sekolah-pendidikan-full-master.html'],['T07','t07-kesihatan-full-master.html'],['T08','t08-kebersihan-full-master.html'],['T09','t09-keselamatan-full-master.html'],['T10','t10-makanan-pemakanan-full-master.html'],['T11','t11-alam-sekitar-full-master.html'],['T12','t12-haiwan-tumbuhan-full-master.html'],['T13','t13-cuaca-alam-full-master.html'],['T14','t14-masyarakat-kejiranan-full-master.html'],['T15','t15-kemudahan-awam-full-master.html'],['T16','t16-pengangkutan-jalan-raya-full-master.html'],['T17','t17-sukan-rekreasi-full-master.html'],['T18','t18-teknologi-komunikasi-full-master.html'],['T19','t19-pekerjaan-full-master.html'],['T20','t20-ekonomi-kewangan-full-master.html'],['T21','t21-kebudayaan-warisan-full-master.html'],['T22','t22-patriotisme-full-master.html'],['T23','t23-nilai-murni-full-master.html'],['T24','t24-masalah-penyelesaian-full-master.html'],['T25','t25-sebab-akibat-full-master.html'],['T26','t26-kata-hubung-penanda-wacana-full-master.html'],['T27','t27-kata-arah-tempat-masa-full-master.html'],['T28','t28-imbuhan-full-master.html'],['T29','t29-sinonim-antonim-full-master.html'],['T30','t30-ungkapan-peribahasa-full-master.html']];

const style=document.createElement('style');
style.textContent=`
.word-search-panel{margin:22px 0;background:#fff;border:1px solid var(--line,#eadfd7);border-radius:25px;padding:22px;box-shadow:0 11px 30px rgba(60,40,30,.07)}
.word-search-panel h2{margin:0 0 6px;font-size:26px}.word-search-help{color:var(--muted,#6c6670);margin:0 0 12px}.word-search-box{display:flex;gap:10px}.word-search-input{width:100%;border:1px solid #e7d5ca;border-radius:17px;background:#fffaf7;padding:15px 17px;outline:none;font-size:19px}.word-search-input:focus{border-color:#d69d78;box-shadow:0 0 0 4px rgba(184,71,47,.08)}
.word-search-status{margin-top:10px;color:#746861;font-size:14px}.word-results{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px;margin-top:15px}.word-result{border:1px solid #eadfd7;border-radius:18px;padding:16px;background:#fffaf7}.word-result h3{margin:0;color:#9b3d28;font-size:24px}.word-meaning{font-size:18px;font-weight:800;margin:3px 0 10px}.word-meta{font-size:13px;color:#786d66;margin-bottom:8px}.word-context{background:#fff3e8;border-radius:12px;padding:10px 12px;font-size:14px}.word-context b{color:#8f3f2b}.word-related{margin-top:8px;font-size:13px;color:#655b55}.word-open{display:inline-block;margin-top:11px;background:#9b3d28;color:#fff;border-radius:999px;padding:7px 11px;font-size:13px;font-weight:850}.word-empty{margin-top:14px;padding:15px;border:1px dashed #d8c4b7;border-radius:15px;color:#756b65;display:none}.word-mark{background:#ffe5a8;padding:0 2px;border-radius:3px}
@media(max-width:760px){.word-results{grid-template-columns:1fr}.word-search-panel{padding:18px}.word-result h3{font-size:22px}}
`;
document.head.appendChild(style);

const dashboard=document.querySelector('.dashboard');
if(!dashboard)return;
const panel=document.createElement('section');
panel.className='word-search-panel';
panel.innerHTML=`<h2>Cari perkataan｜搜索词汇</h2><p class="word-search-help">输入一个马来文或华语词，例如 <b>gembira</b>。系统会直接显示词义、学习等级、使用语境和相关词汇。</p><div class="word-search-box"><input id="wordSearch" class="word-search-input" type="search" autocomplete="off" placeholder="Cari perkataan / 搜索词汇，例如 gembira、prihatin、关心"></div><div id="wordSearchStatus" class="word-search-status">Memuatkan kosa kata…｜正在载入词库…</div><div id="wordResults" class="word-results"></div><div id="wordEmpty" class="word-empty">Perkataan tidak ditemui｜没有找到这个词</div>`;
dashboard.insertAdjacentElement('afterend',panel);

const input=panel.querySelector('#wordSearch'), results=panel.querySelector('#wordResults'), status=panel.querySelector('#wordSearchStatus'), empty=panel.querySelector('#wordEmpty');
let index=[];
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const norm=s=>String(s??'').toLowerCase().normalize('NFKC').trim();
const clean=s=>String(s??'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
const add=o=>{if(!o.word||!o.meaning)return; const key=[norm(o.word),norm(o.meaning),o.href,o.level,o.section].join('|'); if(!index.some(x=>x._key===key))index.push({...o,_key:key});};

function parseRaw(text,code,href){
 const m=text.match(/const\s+raw\s*=\s*`([\s\S]*?)`\s*;/); if(!m)return false;
 const lines=m[1].split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
 for(const line of lines){const p=line.split('|'); if(p.length<11)continue; const section=p[0].toUpperCase(); const msTitle=clean(p[1]), zhTitle=clean(p[2]);
  for(let i=3;i<=10;i++){const level='L'+(i-2); const entries=p[i].split(';').map(x=>x.trim()).filter(Boolean); const related=entries.map(e=>clean(e.split('~')[0])).filter(Boolean);
   for(const e of entries){const k=e.indexOf('~'); if(k<1)continue; add({word:clean(e.slice(0,k)),meaning:clean(e.slice(k+1)),code,href,level,section,sectionTitle:msTitle+'｜'+zhTitle,related});}
  }
 }
 return true;
}

function parseDom(text,code,href){
 const doc=new DOMParser().parseFromString(text,'text/html');
 const pageTitle=clean(doc.querySelector('h1')?.textContent||code);
 const containers=[...doc.querySelectorAll('.item,.word')];
 for(const c of containers){
  const wordEl=c.querySelector('.bm,strong'); if(!wordEl)continue; const word=clean(wordEl.textContent); if(!word)continue;
  let meaning=''; const zh=c.querySelector('.zh');
  if(zh)meaning=clean(zh.textContent); else {const ds=[...c.children].filter(x=>x!==wordEl && x.tagName!=='SMALL'); meaning=clean(ds[0]?.textContent||'');}
  if(!meaning)continue;
  const levelEl=c.closest('.level,details'); const cls=(levelEl?.className||'').toString(); const lm=cls.match(/\bl([1-8])\b/i); let level=lm?'L'+lm[1]:'';
  if(!level){const h=clean(levelEl?.querySelector('h3,summary')?.textContent||''); const hm=h.match(/L([1-8])/i); if(hm)level='L'+hm[1];}
  const sec=c.closest('details.section,.section'); const section=(sec?.id||'').toUpperCase(); let sectionTitle=clean(sec?.querySelector('summary,h2,.head')?.textContent||pageTitle); sectionTitle=sectionTitle.replace(/T\d{2}-?[A-J]?\s*[｜·-]?/i,'').trim();
  const peers=[...((c.parentElement?.querySelectorAll('.bm,strong'))||[])].map(x=>clean(x.textContent)).filter(Boolean).slice(0,8);
  add({word,meaning,code,href,level,section,sectionTitle,related:peers});
 }
}

async function build(){
 const loaded=await Promise.all(files.map(async([code,href])=>{try{const r=await fetch(href,{cache:'force-cache'}); if(!r.ok)throw new Error(); const t=await r.text(); if(!parseRaw(t,code,href))parseDom(t,code,href); return true;}catch(e){return false;}}));
 status.textContent=`${index.length} perkataan sedia dicari｜已载入 ${index.length} 个词汇`;
 if(loaded.filter(Boolean).length<files.length)status.textContent+=` · ${loaded.filter(Boolean).length}/30 tema`;
 const q=new URLSearchParams(location.search).get('q'); if(q){input.value=q; search(q);}
}

function mark(text,q){const s=esc(text); const qq=esc(q).replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); if(!qq)return s; return s.replace(new RegExp('('+qq+')','ig'),'<span class="word-mark">$1</span>');}
function search(v){const q=norm(v); results.innerHTML=''; empty.style.display='none'; if(!q){status.textContent=`${index.length} perkataan sedia dicari｜已载入 ${index.length} 个词汇`;return;}
 let found=index.map(x=>{const w=norm(x.word),m=norm(x.meaning); let score=w===q?0:w.startsWith(q)?1:w.includes(q)?2:m===q?3:m.includes(q)?4:99; return [score,x];}).filter(x=>x[0]<99).sort((a,b)=>a[0]-b[0]||a[1].word.localeCompare(b[1].word)).slice(0,30).map(x=>x[1]);
 status.textContent=`${found.length} hasil｜找到 ${found.length} 个结果`;
 if(!found.length){empty.style.display='block';return;}
 for(const x of found){const rel=(x.related||[]).filter(r=>norm(r)!==norm(x.word)).slice(0,4); const card=document.createElement('article'); card.className='word-result';
  card.innerHTML=`<h3>${mark(x.word,v)}</h3><div class="word-meaning">${mark(x.meaning,v)}</div><div class="word-meta">${esc(x.code)}${x.section?' · '+esc(x.section):''}${x.level?' · '+esc(x.level):''}</div><div class="word-context"><b>Konteks penggunaan｜使用语境</b><br>${esc(x.sectionTitle||'Kosa kata Bahasa Melayu｜马来文词汇')}</div>${rel.length?`<div class="word-related"><b>Perkataan berkaitan｜相关词汇：</b> ${rel.map(esc).join(' · ')}</div>`:''}<a class="word-open" href="${esc(x.href)}?q=${encodeURIComponent(x.word)}${x.section?'#'+encodeURIComponent(x.section):''}">Buka tema｜进入主题</a>`;
  results.appendChild(card);
 }
}
let timer; input.addEventListener('input',()=>{clearTimeout(timer); timer=setTimeout(()=>search(input.value),90)});
build();
})();
