from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = '<!-- WENIK PARTNER CARDS UNIFORM V1 START -->'
end = '<!-- WENIK PARTNER CARDS UNIFORM V1 END -->'
block = r'''<!-- WENIK PARTNER CARDS UNIFORM V1 START -->
<style id="wenikPartnerCardsUniformV1">
/* Final customer partner-card normalization: same media size + same card proportions. */
.wenikPartnerGrid{
  align-items:stretch!important;
  grid-auto-rows:1fr!important;
}
.wenikPartnerCard{
  display:flex!important;
  flex-direction:column!important;
  height:100%!important;
  min-height:0!important;
  overflow:hidden!important;
}
.wenikPartnerCard .wenikPartnerMedia{
  position:relative!important;
  width:100%!important;
  height:auto!important;
  min-height:0!important;
  max-height:none!important;
  aspect-ratio:16/9!important;
  flex:0 0 auto!important;
  overflow:hidden!important;
}
.wenikPartnerCard .wenikPartnerMedia>img,
.wenikPartnerCard .wenikPartnerMedia img{
  display:block!important;
  width:100%!important;
  height:100%!important;
  min-height:0!important;
  max-height:none!important;
  object-fit:cover!important;
  object-position:center!important;
}
.wenikPartnerCard .wenikPartnerBody{
  flex:1 1 auto!important;
  display:flex!important;
  flex-direction:column!important;
  min-height:96px!important;
  box-sizing:border-box!important;
}
.wenikPartnerCard .wenikPartnerName,
.wenikPartnerCard .wenikPartnerMeta{
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
@media(max-width:390px){
  .wenikPartnerCard .wenikPartnerMedia{aspect-ratio:16/9!important}
  .wenikPartnerCard .wenikPartnerBody{min-height:90px!important}
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
  function norm(v){return String(v||'').trim().toLowerCase()}
  function dataFor(card){
    const id=card?.dataset?.wenikPartnerId;
    const list=window.partnerDirectory||[];
    return list.find(x=>String(x.partner_id||x.id||'')===String(id||''))||null;
  }
  function fix(card){
    if(!card)return;
    const meta=card.querySelector('.wenikPartnerMeta');
    if(!meta)return;
    const partner=dataFor(card);
    let area=cleanArea(partner?.area||'');
    let category=String(partner?.category||'').trim();
    if(!area||!category){
      const raw=(meta.textContent||'').replace(/^📍\s*/,'').trim();
      const parts=raw.split(/\s*[•·]\s*/).map(x=>x.trim()).filter(Boolean);
      if(parts.length>=2){
        if(!area)area=cleanArea(parts[0]);
        if(!category)category=parts[1];
      }
    }
    if(area&&category){
      meta.textContent='📍 '+area+' · '+category;
      meta.dataset.wenikPrettyMeta='1';
    }else if(area){
      meta.textContent='📍 '+area;
      meta.dataset.wenikPrettyMeta='1';
    }
  }
  function all(){document.querySelectorAll('.wenikPartnerCard').forEach(fix)}
  let queued=false;
  function queue(){if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;all()})}
  function boot(){all();new MutationObserver(queue).observe(document.body,{childList:true,subtree:true});[250,700,1500,3000].forEach(ms=>setTimeout(all,ms))}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
<!-- WENIK PARTNER CARDS UNIFORM V1 END -->'''

if start in s and end in s:
    s = re.sub(re.escape(start) + r'.*?' + re.escape(end), block, s, flags=re.S)
else:
    pos = s.lower().rfind('</body>')
    if pos == -1:
        raise SystemExit('index.html has no </body>')
    s = s[:pos] + block + '\n' + s[pos:]

p.write_text(s, encoding='utf-8')
print('Applied WENIK partner-card uniform fix')
