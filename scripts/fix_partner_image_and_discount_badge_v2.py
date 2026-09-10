from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK PARTNER IMAGE + DISCOUNT BADGE V2 */'
if marker in s:
    raise SystemExit('already applied')

# This version avoids brittle exact matching of the generated partner-card renderer.
# It normalizes the discount badge at runtime, so V5 rewrites cannot break placement.
style=r'''
<style id="wenikPartnerImageDiscountBadgeV2">
/* WENIK PARTNER IMAGE + DISCOUNT BADGE V2 */
.wenikPartnerMedia{position:relative!important;overflow:hidden!important}
.wenikPartnerMedia .wenikOff{
  position:absolute!important;
  top:9px!important;left:9px!important;right:auto!important;bottom:auto!important;
  z-index:40!important;
  width:auto!important;max-width:calc(100% - 18px)!important;
  margin:0!important;padding:7px 10px!important;
  border-radius:999px!important;
  white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;
  background:rgba(255,255,255,.96)!important;
  color:#d95b16!important;
  border:1px solid rgba(255,255,255,.92)!important;
  box-shadow:0 6px 18px rgba(20,12,30,.20)!important;
  font-size:11px!important;font-weight:950!important;line-height:1!important;
  backdrop-filter:blur(8px)!important;-webkit-backdrop-filter:blur(8px)!important;
}
@media(max-width:390px){
  .wenikPartnerMedia .wenikOff{top:8px!important;left:8px!important;padding:6px 8px!important;font-size:10px!important;max-width:calc(100% - 16px)!important}
}
</style>
<script id="wenikPartnerImageDiscountBadgeRuntimeV2">
(function(){
  function normalizeCard(card){
    if(!card)return;
    const media=card.querySelector('.wenikPartnerMedia');
    if(!media)return;
    let badge=card.querySelector('.wenikOff');
    if(badge){
      const text=(badge.textContent||'').trim();
      if(text)card.dataset.wenikDiscountText=text;
      if(badge.parentElement!==media)media.appendChild(badge);
      return;
    }
    const saved=(card.dataset.wenikDiscountText||'').trim();
    if(saved){
      badge=document.createElement('div');
      badge.className='wenikOff';
      badge.textContent=saved;
      media.appendChild(badge);
    }
  }
  function normalizeAll(){document.querySelectorAll('.wenikPartnerCard').forEach(normalizeCard)}
  let queued=false;
  function queue(){if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;normalizeAll()})}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>{normalizeAll();new MutationObserver(queue).observe(document.body,{childList:true,subtree:true})});
  else{normalizeAll();new MutationObserver(queue).observe(document.body,{childList:true,subtree:true})}
})();
</script>
'''
if '</head>' not in s:
    raise SystemExit('head anchor missing')
s=s.replace('</head>',style+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Resilient Partner image + discount badge V2 applied')
