(()=>{
const packs=['curriculum-dict-kata-nama-core-14.json','curriculum-dict-kata-nama-complete-15.json','curriculum-dict-kata-nama-complete-16.json','curriculum-dict-kata-nama-complete-17.json'];
const m=(document.title+' '+location.pathname).match(/T(\d{2})/i)||location.pathname.match(/t(\d{2})/i);if(!m)return;const theme='T'+m[1];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const norm=s=>String(s??'').toLowerCase().trim();
async function load(){let all=[];for(const f of packs){try{const r=await fetch(f,{cache:'no-cache'});if(r.ok)all.push(...await r.json())}catch(e){}}
const seen=new Set();const words=all.filter(x=>x.theme===theme&&x.type==='nama').filter(x=>{const k=norm(x.word);if(!k||seen.has(k))return false;seen.add(k);return true});if(!words.length)return;
const style=document.createElement('style');style.textContent=`.kn-theme{margin:24px 0;background:#fff;border:1px solid var(--line,#e5ddd7);border-radius:22px;padding:22px;box-shadow:0 10px 28px rgba(30,30,30,.07)}.kn-theme h2{font-size:28px;margin:0 0 5px}.kn-sub{color:var(--muted,#68707c);margin:0 0 16px}.kn-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.kn-card{border:1px solid var(--line,#e5ddd7);border-radius:15px;padding:14px;background:#fff}.kn-word{font-size:21px;font-weight:900}.kn-zh{font-size:17px;font-weight:750;margin:2px 0 8px}.kn-use,.kn-ex{font-size:15px;line-height:1.55;margin-top:7px}.kn-use{color:#514b47}.kn-ex{color:var(--muted,#68707c)}@media(max-width:720px){.kn-grid{grid-template-columns:1fr}}`;document.head.appendChild(style);
const sec=document.createElement('section');sec.className='kn-theme';sec.id='kata-nama';sec.innerHTML=`<h2>Kata Nama｜高频名词</h2><p class="kn-sub">Kosa kata utama mengikut tema ini｜本主题高频核心名词</p><div class="kn-grid">${words.sort((a,b)=>a.word.localeCompare(b.word,'ms')).map(x=>`<article class="kn-card"><div class="kn-word">${esc(x.word)}</div><div class="kn-zh">${esc(x.meaning)}</div>${x.usage?`<div class="kn-use"><b>Penggunaan｜用法：</b>${esc(x.usage)}</div>`:''}${x.example?`<div class="kn-ex"><b>Contoh ayat｜例句：</b>${esc(x.example)}</div>`:''}</article>`).join('')}</div>`;
const main=document.querySelector('main');if(main)main.appendChild(sec);
}
load();
})();