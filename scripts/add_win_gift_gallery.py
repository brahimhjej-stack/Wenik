from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- WENIK WIN GIFT GALLERY V1 -->'

# Remove the broken V1 gallery if it is already present. The original injector
# appended literal \\n tokens into a classic script, which stops that script from parsing.
if marker in s:
    s=re.sub(r'\n?<!-- WENIK WIN GIFT GALLERY V1 -->\n<div class="winGiftGalleryBlock">[\s\S]*?</div>\n</section>', '\n</section>', s, count=1)
    s=re.sub(r'\n?/\* WENIK WIN GIFT GALLERY V1 \*/\n\.winGiftGalleryBlock\{[\s\S]*?@media\(min-width:700px\)\{\.winGiftGallery\{grid-template-columns:repeat\(4,minmax\(0,1fr\)\)\}\}\n?', '\n', s, count=1)
    # Remove the old broken literal-backslash JS block through the classic script close.
    s=re.sub(r'\\n// WENIK WIN GIFT GALLERY V1\\n[\s\S]*?(?=</script>)', '', s, count=1)

# Find WIN section.
pat=re.compile(r'(<section\b[^>]*\bid=["\'](?:win|wins)["\'][^>]*>[\s\S]*?)(</section>)',re.I)
m=pat.search(s)
if not m:
    raise SystemExit('WIN section not found')

html='''\n<!-- WENIK WIN GIFT GALLERY V1 -->\n<div class="winGiftGalleryBlock">\n  <div class="winGiftGalleryHead"><div><div class="winGiftEyebrow">ALL GIFTS</div><h2>Gifts you can WIN</h2></div><span id="winGiftCount" class="winGiftCount">0</span></div>\n  <input id="winGiftSearch" class="winGiftSearch" type="search" placeholder="Search gifts or partner" autocomplete="off">\n  <div id="winGiftGallery" class="winGiftGallery"><div class="winGiftEmpty">Loading gifts…</div></div>\n  <button id="winGiftMore" class="winGiftMore hidden" type="button">SHOW MORE GIFTS</button>\n</div>\n'''
s=s[:m.start(2)]+html+s[m.start(2):]

css='''\n/* WENIK WIN GIFT GALLERY V1 */\n.winGiftGalleryBlock{margin:18px 0 8px}.winGiftGalleryHead{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;margin-bottom:10px}.winGiftGalleryHead h2{margin:2px 0 0}.winGiftEyebrow{font-size:11px;font-weight:900;letter-spacing:2px;color:#ffb6df}.winGiftCount{min-width:38px;text-align:center;border-radius:999px;padding:7px 10px;background:rgba(255,255,255,.09);font-weight:900}.winGiftSearch{width:100%;border-radius:16px;border:1px solid rgba(255,255,255,.13);background:rgba(10,8,20,.78);color:#fff;padding:14px 15px;margin:4px 0 14px;font-size:15px}.winGiftGallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.winGiftCard{overflow:hidden;border-radius:20px;background:linear-gradient(145deg,rgba(30,18,52,.98),rgba(12,10,24,.98));border:1px solid rgba(177,92,255,.22);box-shadow:0 12px 28px rgba(0,0,0,.22)}.winGiftImgWrap{position:relative;aspect-ratio:1/1;background:linear-gradient(135deg,#24163a,#11101c);overflow:hidden}.winGiftImg{width:100%;height:100%;display:block;object-fit:cover}.winGiftImgFallback{width:100%;height:100%;display:grid;place-items:center;font-size:42px}.winGiftRemain{position:absolute;top:9px;right:9px;padding:6px 8px;border-radius:999px;background:rgba(7,6,14,.82);backdrop-filter:blur(8px);font-size:11px;font-weight:900}.winGiftBody{padding:11px 12px 13px}.winGiftTitle{font-weight:900;line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.winGiftPartner{font-size:12px;color:#bbb4ca;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.winGiftMore{width:100%;margin-top:14px;border:0;border-radius:16px;padding:13px 14px;background:linear-gradient(100deg,#8f24ff,#ef159d 45%,#ff7625);color:#fff;font-weight:900}.winGiftEmpty{grid-column:1/-1;text-align:center;padding:24px 12px;color:#bbb4ca}.hidden{display:none!important}@media(min-width:700px){.winGiftGallery{grid-template-columns:repeat(4,minmax(0,1fr))}}\n'''
if '</style>' not in s: raise SystemExit('style end not found')
s=s.replace('</style>',css+'</style>',1)

# Inject into the existing module script so rpc/esc are in scope. The RPC requires p_limit.
js='''\n// WENIK WIN GIFT GALLERY V1\nlet __winGiftRows=[],__winGiftFiltered=[],__winGiftShown=0;\nconst __winGiftBatch=24;\nfunction __wgNum(v){const n=Number(v);return Number.isFinite(n)?n:null}\nfunction __winGiftNormalize(x){\n  const remain=__wgNum(x.remaining_quantity??x.remaining??x.remaining_gifts??x.stock_remaining);\n  return {id:x.gift_id||x.id||'',title:x.gift_title||x.title||x.name||x.gift_name||'WENIK Gift',partner:x.partner_name||x.business_name||x.partner||'',image:x.image_url||x.gift_image_url||x.photo_url||x.partner_logo_url||x.image||'',remain};\n}\nfunction __winGiftRender(reset=false){\n  const box=$('winGiftGallery'),more=$('winGiftMore'),count=$('winGiftCount');if(!box||!more||!count)return;\n  if(reset){__winGiftShown=0;box.innerHTML=''}count.textContent=String(__winGiftFiltered.length);\n  const end=Math.min(__winGiftShown+__winGiftBatch,__winGiftFiltered.length),rows=__winGiftFiltered.slice(__winGiftShown,end);\n  if(reset&&!rows.length)box.innerHTML='<div class="winGiftEmpty">No gifts available right now.</div>';\n  for(const g of rows){const card=document.createElement('article');card.className='winGiftCard';const img=g.image?'<img class="winGiftImg" loading="lazy" decoding="async" src="'+esc(g.image)+'" alt="'+esc(g.title)+'">':'<div class="winGiftImgFallback">🎁</div>';const rem=g.remain===null?'':'<span class="winGiftRemain">'+esc(g.remain)+' left</span>';card.innerHTML='<div class="winGiftImgWrap">'+img+rem+'</div><div class="winGiftBody"><div class="winGiftTitle">'+esc(g.title)+'</div><div class="winGiftPartner">'+esc(g.partner||'WENIK')+'</div></div>';const im=card.querySelector('img');if(im)im.addEventListener('error',()=>{im.parentElement.innerHTML='<div class="winGiftImgFallback">🎁</div>'},{once:true});box.appendChild(card)}\n  __winGiftShown=end;more.classList.toggle('hidden',__winGiftShown>=__winGiftFiltered.length);\n}\nasync function loadWinGiftGallery(){\n  const box=$('winGiftGallery');if(!box)return;try{if(!__winGiftRows.length){box.innerHTML='<div class="winGiftEmpty">Loading gifts…</div>';const rows=await rpc('public_active_win_gifts',{p_limit:500});__winGiftRows=(rows||[]).map(__winGiftNormalize).filter(g=>g.remain===null||g.remain>0)}const q=($('winGiftSearch')?.value||'').trim().toLowerCase();__winGiftFiltered=!q?__winGiftRows:__winGiftRows.filter(g=>(g.title+' '+g.partner).toLowerCase().includes(q));__winGiftRender(true)}catch(e){box.innerHTML='<div class="winGiftEmpty">Gifts are temporarily unavailable.</div>';console.error('WIN gifts gallery',e)}\n}\n$('winGiftSearch')?.addEventListener('input',loadWinGiftGallery);$('winGiftMore')?.addEventListener('click',()=>__winGiftRender(false));\n'''
module_end=s.find('</script>', s.find('<script type="module">'))
if module_end<0: raise SystemExit('module script end not found')
s=s[:module_end]+js+s[module_end:]
# Ensure the existing WIN navigation loads both wins and gallery.
s=s.replace("if(id==='win')loadWins();", "if(id==='win'){loadWins();loadWinGiftGallery();}", 1)

p.write_text(s,encoding='utf-8')
print('WIN gift gallery V1 fixed and applied')
