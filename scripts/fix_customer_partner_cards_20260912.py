from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = '<!-- WENIK PARTNER CARDS UNIFORM V1 START -->'
end = '<!-- WENIK PARTNER CARDS UNIFORM V1 END -->'

block = r'''<!-- WENIK PARTNER CARDS UNIFORM V1 START -->
<style id="wenikPartnerCardsUniformV1">
/* FINAL V3: layout-only fix. Every partner media box is square and card height follows its content. */
.wenikPartnerGrid{
  align-items:start!important;
  grid-auto-rows:auto!important;
}
.wenikPartnerCard{
  display:flex!important;
  flex-direction:column!important;
  align-self:start!important;
  min-width:0!important;
  height:auto!important;
  min-height:0!important;
  max-height:none!important;
  overflow:hidden!important;
  border-radius:22px!important;
  background:#fff!important;
}
.wenikPartnerCard>.wenikPartnerMedia,
.wenikPartnerCard .wenikPartnerMedia{
  position:relative!important;
  display:block!important;
  width:100%!important;
  height:auto!important;
  min-height:0!important;
  max-height:none!important;
  aspect-ratio:1/1!important;
  flex:0 0 auto!important;
  overflow:hidden!important;
  box-sizing:border-box!important;
  background:linear-gradient(135deg,#f4ebff,#fff1e8,#fff8d9)!important;
}
.wenikPartnerCard>.wenikPartnerMedia>img,
.wenikPartnerCard .wenikPartnerMedia img{
  position:absolute!important;
  inset:0!important;
  display:block!important;
  width:100%!important;
  height:100%!important;
  min-width:100%!important;
  min-height:100%!important;
  max-width:none!important;
  max-height:none!important;
  object-fit:cover!important;
  object-position:center center!important;
  margin:0!important;
  padding:0!important;
}
.wenikPartnerCard .wenikPartnerPlaceholder{
  position:absolute!important;
  inset:0!important;
  width:100%!important;
  height:100%!important;
  display:grid!important;
  place-items:center!important;
  box-sizing:border-box!important;
}
.wenikPartnerCard>.wenikPartnerBody,
.wenikPartnerCard .wenikPartnerBody{
  flex:0 0 auto!important;
  height:auto!important;
  min-height:0!important;
  max-height:none!important;
  box-sizing:border-box!important;
}
@media(max-width:390px){.wenikPartnerCard{border-radius:19px!important}}
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
  function partnerFor(card){
    const id=card?.dataset?.wenikPartnerId;
    const list=window.partnerDirectory||[];
    return list.find(x=>String(x.partner_id||x.id||'')===String(id||''))||null;
  }
  function fixMeta(card){
    const meta=card&&card.querySelector('.wenikPartnerMeta');
    if(!meta)return;
    const partner=partnerFor(card);
    let area=cleanArea(partner?.area||'');
    let category=String(partner?.category||'').trim();
    if(!area||!category){
      const raw=(meta.textContent||'').replace(/^📍\s*/,'').trim();
      const parts=raw.split(/\s*[•·]\s*/).map(x=>x.trim()).filter(Boolean);
      if(parts.length>=2){if(!area)area=cleanArea(parts[0]);if(!category)category=parts[1]}
    }
    const wanted=area&&category?'📍 '+area+' · '+category:area?'📍 '+area:'';
    if(wanted&&meta.textContent!==wanted)meta.textContent=wanted;
  }
  function fixAll(){document.querySelectorAll('.wenikPartnerCard').forEach(fixMeta)}
  function boot(){
    fixAll();
    new MutationObserver(()=>requestAnimationFrame(fixAll)).observe(document.body,{childList:true,subtree:true});
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

# Remove old competing 4:3 geometry anywhere in the accumulated stylesheet.
s = s.replace('aspect-ratio:4/3!important;', 'aspect-ratio:1/1!important;')
s = s.replace('aspect-ratio: 4/3!important;', 'aspect-ratio:1/1!important;')
s = s.replace('aspect-ratio:4 / 3!important;', 'aspect-ratio:1/1!important;')

p.write_text(s, encoding='utf-8')
print('Applied WENIK partner-card V3: square media and natural card heights')
