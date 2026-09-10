from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK PARTNER IMAGE + DISCOUNT BADGE V3 */'
if marker in s:
    raise SystemExit('already applied')

style=r'''
<style id="wenikPartnerImageDiscountBadgeV3">
/* WENIK PARTNER IMAGE + DISCOUNT BADGE V3 */
.wenikPartnerMedia{position:relative!important;overflow:hidden!important}
.wenikPartnerMedia>img{width:100%!important;height:100%!important;display:block!important;object-fit:cover!important;object-position:center!important}
.wenikPartnerMedia .wenikOff{
  position:absolute!important;
  top:8px!important;left:8px!important;right:auto!important;bottom:auto!important;
  z-index:60!important;
  width:auto!important;max-width:calc(100% - 16px)!important;
  margin:0!important;padding:7px 11px!important;
  border-radius:999px!important;
  white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;
  background:linear-gradient(135deg,#ff6b00,#ff3d00)!important;
  color:#fff!important;
  border:1px solid rgba(255,255,255,.55)!important;
  box-shadow:0 5px 15px rgba(27,12,12,.28)!important;
  font-size:11px!important;font-weight:950!important;line-height:1!important;
  letter-spacing:.15px!important;
}
@media(max-width:390px){.wenikPartnerMedia .wenikOff{top:7px!important;left:7px!important;padding:6px 9px!important;font-size:10px!important;max-width:calc(100% - 14px)!important}}
</style>
<script id="wenikPartnerImageDiscountBadgeRuntimeV3">
(function(){
  const busy=new WeakSet();

  function moveBadge(card,media){
    let badge=card.querySelector('.wenikOff');
    if(badge){
      const text=(badge.textContent||'').trim();
      if(text)card.dataset.wenikDiscountText=text;
      if(badge.parentElement!==media)media.appendChild(badge);
      return badge;
    }
    const saved=(card.dataset.wenikDiscountText||'').trim();
    if(saved){
      badge=document.createElement('div');
      badge.className='wenikOff';
      badge.textContent=saved;
      media.appendChild(badge);
      return badge;
    }
    return null;
  }

  async function normalizeCard(card){
    if(!card)return;
    const media=card.querySelector('.wenikPartnerMedia');
    if(!media)return;
    const badge=moveBadge(card,media);
    const id=(card.dataset.wenikPartnerId||'').trim();
    if(!id||busy.has(card))return;

    const img=media.querySelector('img');
    if(img && img.src && !media.querySelector('.wenikPartnerPlaceholder')){
      card.dataset.wenikImageHydrated='1';
      return;
    }

    if(typeof window.getWenikPartnerApprovedImage!=='function' && typeof getWenikPartnerApprovedImage!=='function')return;
    busy.add(card);
    try{
      const fn=window.getWenikPartnerApprovedImage||getWenikPartnerApprovedImage;
      const url=await fn(id);
      if(!url||!card.isConnected)return;
      const currentMedia=card.querySelector('.wenikPartnerMedia');
      if(!currentMedia)return;
      const keepBadge=currentMedia.querySelector('.wenikOff')||badge;
      const partner=(window.partnerDirectory||[]).find(x=>String(x.partner_id)===String(id));
      const name=(partner&&partner.business_name)||'WENIK Partner';
      const escFn=typeof window.esc==='function'?window.esc:(v=>String(v||'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c])));
      currentMedia.innerHTML='<img src="'+escFn(url)+'" alt="'+escFn(name)+'" loading="lazy" decoding="async">';
      if(keepBadge)currentMedia.appendChild(keepBadge);
      card.dataset.wenikImageHydrated='1';
      card.dataset.wenikApprovedImage='1';
    }catch(e){
      console.warn('WENIK partner card image hydration retry',e);
    }finally{busy.delete(card)}
  }

  function normalizeAll(){document.querySelectorAll('.wenikPartnerCard[data-wenik-partner-id]').forEach(normalizeCard)}
  let queued=false;
  function queue(){if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;normalizeAll()})}
  function boot(){
    normalizeAll();
    new MutationObserver(queue).observe(document.body,{childList:true,subtree:true});
    [450,1200,2500,5000].forEach(ms=>setTimeout(normalizeAll,ms));
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
'''
if '</head>' not in s:
    raise SystemExit('head anchor missing')
s=s.replace('</head>',style+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Partner approved image + discount badge V3 applied')
