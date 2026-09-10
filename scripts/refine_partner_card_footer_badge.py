from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK PARTNER CARD FOOTER BADGE V1 */'
if marker in s:
    raise SystemExit('already applied')
style=r'''
<style id="wenikPartnerCardFooterBadgeV1">
/* WENIK PARTNER CARD FOOTER BADGE V1 */
.wenikPartnerCard{
  position:relative!important;
  display:flex!important;
  flex-direction:column!important;
  height:100%!important;
  min-height:0!important;
  overflow:hidden!important;
  background:#fff!important;
  border-radius:22px!important;
  border:1px solid rgba(61,31,82,.08)!important;
  box-shadow:0 12px 28px rgba(48,25,67,.10)!important;
}
.wenikPartnerMedia{
  position:relative!important;
  width:100%!important;
  aspect-ratio:16/9!important;
  min-height:0!important;
  overflow:hidden!important;
  border-radius:0!important;
  background:linear-gradient(135deg,#f3eaff,#fff0e7,#fff7da)!important;
}
.wenikPartnerMedia:after{display:none!important;content:none!important}
.wenikPartnerMedia>img,.wenikPartnerMedia img{
  width:100%!important;
  height:100%!important;
  max-width:none!important;
  display:block!important;
  object-fit:cover!important;
  object-position:center!important;
}
.wenikPartnerBody{
  position:relative!important;
  left:auto!important;right:auto!important;bottom:auto!important;
  z-index:auto!important;
  flex:1 1 auto!important;
  display:flex!important;
  flex-direction:column!important;
  min-height:132px!important;
  padding:12px 13px 11px!important;
  background:#fff!important;
  color:#21172d!important;
  pointer-events:auto!important;
  box-sizing:border-box!important;
}
.wenikPartnerName{
  color:#21172d!important;
  font-size:16px!important;
  font-weight:950!important;
  line-height:1.15!important;
  text-shadow:none!important;
  letter-spacing:-.2px!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
.wenikPartnerMeta{
  margin-top:6px!important;
  color:#797280!important;
  font-size:12px!important;
  font-weight:700!important;
  line-height:1.25!important;
  text-shadow:none!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
.wenikPartnerPromo{
  display:none!important;
}
.wenikPartnerFooter{
  margin-top:auto!important;
  display:flex!important;
  align-items:center!important;
  justify-content:space-between!important;
  gap:8px!important;
  padding-top:10px!important;
}
.wenikPartnerFooter .wenikOff,
.wenikPartnerFooter .wenikPartnerBadge{
  position:static!important;
  display:inline-flex!important;
  align-items:center!important;
  gap:5px!important;
  width:auto!important;
  max-width:calc(100% - 60px)!important;
  margin:0!important;
  padding:7px 10px!important;
  border-radius:999px!important;
  background:linear-gradient(90deg,#fff0e7,#fff4ec)!important;
  color:#f05a16!important;
  border:0!important;
  box-shadow:none!important;
  font-size:11px!important;
  font-weight:950!important;
  line-height:1!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
  backdrop-filter:none!important;
  -webkit-backdrop-filter:none!important;
}
.wenikPartnerFooter .wenikPartnerBadge:before,
.wenikPartnerFooter .wenikOff:before{content:'🎁';font-size:12px;line-height:1}
.wenikPartnerView{
  flex:0 0 auto!important;
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  min-width:52px!important;
  height:30px!important;
  padding:0 11px!important;
  border-radius:999px!important;
  background:linear-gradient(135deg,#f3d9ff,#eadcff)!important;
  color:#7b2cff!important;
  font-size:11px!important;
  font-weight:950!important;
  line-height:1!important;
}
@media(max-width:390px){
  .wenikPartnerCard{border-radius:19px!important}
  .wenikPartnerBody{min-height:124px!important;padding:10px 10px 10px!important}
  .wenikPartnerName{font-size:14px!important}
  .wenikPartnerMeta{font-size:10.5px!important}
  .wenikPartnerFooter{gap:6px!important;padding-top:8px!important}
  .wenikPartnerFooter .wenikOff,.wenikPartnerFooter .wenikPartnerBadge{font-size:9.5px!important;padding:6px 8px!important;max-width:calc(100% - 48px)!important}
  .wenikPartnerView{min-width:43px!important;height:27px!important;padding:0 8px!important;font-size:9.5px!important}
}
</style>
<script id="wenikPartnerCardFooterBadgeRuntimeV1">
(function(){
  function cleanDiscount(text){
    const t=String(text||'').trim();
    const m=t.match(/(\d+(?:\.\d+)?)\s*%\s*OFF/i);
    return m?(m[1]+'% OFF'):t;
  }
  function polish(card){
    if(!card)return;
    const body=card.querySelector('.wenikPartnerBody');
    if(!body)return;
    let footer=body.querySelector('.wenikPartnerFooter');
    if(!footer){footer=document.createElement('div');footer.className='wenikPartnerFooter';body.appendChild(footer)}
    let badge=card.querySelector('.wenikOff');
    if(badge){
      badge.textContent=cleanDiscount(badge.textContent);
      if(badge.parentElement!==footer)footer.appendChild(badge);
    } else if(!footer.querySelector('.wenikPartnerBadge')) {
      const promo=card.querySelector('.wenikPartnerPromo');
      const b=document.createElement('span');b.className='wenikPartnerBadge';b.textContent=(promo&&promo.textContent.trim())||'WENIK PARTNER';footer.appendChild(b);
    }
    if(!footer.querySelector('.wenikPartnerView')){
      const v=document.createElement('span');v.className='wenikPartnerView';v.textContent='View';footer.appendChild(v);
    }
    const meta=card.querySelector('.wenikPartnerMeta');
    if(meta && !meta.dataset.wenikPrettyMeta){
      const parts=(meta.textContent||'').split('•').map(x=>x.trim()).filter(Boolean);
      if(parts.length>=2){meta.textContent='📍 '+parts[1]+'   •   '+parts[0]}
      meta.dataset.wenikPrettyMeta='1';
    }
  }
  function all(){document.querySelectorAll('.wenikPartnerCard').forEach(polish)}
  let q=false;
  function queue(){if(q)return;q=true;requestAnimationFrame(()=>{q=false;all()})}
  function boot(){all();new MutationObserver(queue).observe(document.body,{childList:true,subtree:true});[250,800,1800].forEach(ms=>setTimeout(all,ms))}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
'''
if '</head>' not in s:
    raise SystemExit('head anchor missing')
s=s.replace('</head>',style+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Refined Partner card footer badge layout applied')
