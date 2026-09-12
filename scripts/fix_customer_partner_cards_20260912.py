from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = '<!-- WENIK PARTNER CARDS UNIFORM V1 START -->'
end = '<!-- WENIK PARTNER CARDS UNIFORM V1 END -->'
block = r'''<!-- WENIK PARTNER CARDS UNIFORM V1 START -->
<style id="wenikPartnerCardsUniformV1">
/* FINAL: every customer partner card uses the same large square photo, regardless of source image ratio. */
.wenikPartnerGrid{align-items:stretch!important;grid-auto-rows:auto!important}
.wenikPartnerCard{
  display:flex!important;flex-direction:column!important;min-width:0!important;height:auto!important;
  overflow:hidden!important;border-radius:22px!important;background:#fff!important;
}
.wenikPartnerCard .wenikPartnerMedia{
  position:relative!important;display:block!important;width:100%!important;
  height:var(--wenik-media-size,220px)!important;min-height:var(--wenik-media-size,220px)!important;
  max-height:var(--wenik-media-size,220px)!important;aspect-ratio:auto!important;flex:0 0 auto!important;
  overflow:hidden!important;background:linear-gradient(135deg,#f4ebff,#fff1e8,#fff8d9)!important;
}
.wenikPartnerCard .wenikPartnerMedia>img,
.wenikPartnerCard .wenikPartnerMedia img{
  position:absolute!important;inset:0!important;display:block!important;width:100%!important;height:100%!important;
  min-width:100%!important;min-height:100%!important;max-width:none!important;max-height:none!important;
  object-fit:cover!important;object-position:center center!important;margin:0!important;padding:0!important;
}
.wenikPartnerCard .wenikPartnerPlaceholder{
  position:absolute!important;inset:0!important;width:100%!important;height:100%!important;
  display:grid!important;place-items:center!important;font-size:27px!important;
}
.wenikPartnerCard .wenikPartnerBody{
  flex:1 1 auto!important;display:flex!important;flex-direction:column!important;min-height:98px!important;
  padding:10px 12px 10px!important;box-sizing:border-box!important;background:#fff!important;
}
.wenikPartnerCard .wenikPartnerName{margin:0!important;font-size:15px!important;line-height:1.15!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
.wenikPartnerCard .wenikPartnerMeta{margin-top:4px!important;font-size:11px!important;line-height:1.2!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
.wenikPartnerCard .wenikPartnerFooter{margin-top:auto!important;padding-top:8px!important}
@media(max-width:390px){
  .wenikPartnerCard{border-radius:19px!important}
  .wenikPartnerCard .wenikPartnerBody{min-height:92px!important;padding:9px 9px 8px!important}
  .wenikPartnerCard .wenikPartnerName{font-size:13.5px!important}
  .wenikPartnerCard .wenikPartnerMeta{font-size:10px!important}
}
</style>
<script id="wenikPartnerCardsUniformRuntimeV1">
(function(){
  function cleanArea(value){
    const raw=String(value||'').replace(/^📍\s*/,'').trim();
    if(!raw)return '';
    const parts=raw.split(/\s*[–—-]\s*/).map(x=>x.trim()).filter(Boolean);
    if(parts.length===2 && parts[0].localeCompare(parts[1],undefined,{sensitivity:'base'})===0)return parts[0];
    return raw;
  }
  function dataFor(card){
    const id=card?.dataset?.wenikPartnerId;
    const list=window.partnerDirectory||[];
    return list.find(x=>String(x.partner_id||x.id||'')===String(id||''))||null;
  }
  function forceMedia(card){
    const media=card&&card.querySelector('.wenikPartnerMedia');
    if(!media)return;
    const w=Math.round(card.getBoundingClientRect().width||media.getBoundingClientRect().width||0);
    if(w>0){
      card.style.setProperty('--wenik-media-size',w+'px');
      media.style.setProperty('height',w+'px','important');
      media.style.setProperty('min-height',w+'px','important');
      media.style.setProperty('max-height',w+'px','important');
      media.style.setProperty('aspect-ratio','auto','important');
    }
    media.querySelectorAll('img').forEach(img=>{
      img.style.setProperty('position','absolute','important');
      img.style.setProperty('inset','0','important');
      img.style.setProperty('width','100%','important');
      img.style.setProperty('height','100%','important');
      img.style.setProperty('min-width','100%','important');
      img.style.setProperty('min-height','100%','important');
      img.style.setProperty('max-width','none','important');
      img.style.setProperty('max-height','none','important');
      img.style.setProperty('object-fit','cover','important');
      img.style.setProperty('object-position','center center','important');
      img.style.setProperty('margin','0','important');
      img.style.setProperty('padding','0','important');
    });
  }
  function fixMeta(card){
    const meta=card&&card.querySelector('.wenikPartnerMeta');
    if(!meta)return;
    const partner=dataFor(card);
    let area=cleanArea(partner?.area||'');
    let category=String(partner?.category||'').trim();
    if(!area||!category){
      const raw=(meta.textContent||'').replace(/^📍\s*/,'').trim();
      const parts=raw.split(/\s*[•·]\s*/).map(x=>x.trim()).filter(Boolean);
      if(parts.length>=2){if(!area)area=cleanArea(parts[0]);if(!category)category=parts[1]}
    }
    if(area&&category)meta.textContent='📍 '+area+' · '+category;
    else if(area)meta.textContent='📍 '+area;
    meta.dataset.wenikPrettyMeta='1';
  }
  function fix(card){if(!card)return;forceMedia(card);fixMeta(card)}
  function all(){document.querySelectorAll('.wenikPartnerCard').forEach(fix)}
  let queued=false;
  function queue(){if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;all()})}
  function boot(){
    all();
    new MutationObserver(queue).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['style','src','class']});
    if('ResizeObserver'in window){const ro=new ResizeObserver(queue);document.querySelectorAll('.wenikPartnerGrid,.wenikPartnerCard').forEach(el=>ro.observe(el));window.__wenikPartnerCardRO=ro}
    addEventListener('resize',queue,{passive:true});
    [50,150,300,600,1000,1800,3000,5000].forEach(ms=>setTimeout(all,ms));
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
<!-- WENIK PARTNER CARDS UNIFORM V1 END -->'''

if start in s and end in s:
    s = re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda _m: block, s, flags=re.S)
else:
    pos = s.lower().rfind('</body>')
    if pos == -1:
        raise SystemExit('index.html has no </body>')
    s = s[:pos] + block + '\n' + s[pos:]

p.write_text(s, encoding='utf-8')
print('Applied WENIK forced equal square partner-card photos')