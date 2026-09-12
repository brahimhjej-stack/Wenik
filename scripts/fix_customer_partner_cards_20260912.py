from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = '<!-- WENIK PARTNER CARDS UNIFORM V1 START -->'
end = '<!-- WENIK PARTNER CARDS UNIFORM V1 END -->'

block = r'''<!-- WENIK PARTNER CARDS UNIFORM V1 START -->
<style id="wenikPartnerCardsUniformV1">
/* FINAL V2: only cards that really have an image get one identical square media box. */
.wenikPartnerGrid{align-items:start!important;grid-auto-rows:auto!important}
.wenikPartnerCard{min-width:0!important;overflow:hidden!important;border-radius:22px!important;background:#fff!important}
.wenikPartnerCard.wenikHasRealImage>.wenikPartnerMedia{
  position:relative!important;display:block!important;width:100%!important;
  height:var(--wenik-card-media-px)!important;min-height:var(--wenik-card-media-px)!important;
  max-height:var(--wenik-card-media-px)!important;flex:0 0 var(--wenik-card-media-px)!important;
  aspect-ratio:auto!important;overflow:hidden!important;
}
.wenikPartnerCard.wenikHasRealImage>.wenikPartnerMedia>img{
  position:absolute!important;inset:0!important;width:100%!important;height:100%!important;
  min-width:100%!important;min-height:100%!important;max-width:none!important;max-height:none!important;
  object-fit:cover!important;object-position:center center!important;margin:0!important;padding:0!important;
}
@media(max-width:390px){.wenikPartnerCard{border-radius:19px!important}}
</style>
<script id="wenikPartnerCardsUniformRuntimeV1">
(function(){
  const SEL='.wenikPartnerCard';
  let queued=false;

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

  function lockRealImage(card){
    if(!card||!card.isConnected)return;
    const media=card.querySelector(':scope > .wenikPartnerMedia')||card.querySelector('.wenikPartnerMedia');
    if(!media)return;
    const img=media.querySelector('img');

    /* No real image: keep the compact no-photo card behavior already used by WENIK. */
    if(!img){
      card.classList.remove('wenikHasRealImage');
      card.style.removeProperty('--wenik-card-media-px');
      return;
    }

    card.classList.add('wenikHasRealImage');
    card.dataset.wenikApprovedImage='1';

    const rect=card.getBoundingClientRect();
    const mediaRect=media.getBoundingClientRect();
    const w=Math.max(1,Math.round(rect.width||mediaRect.width||card.offsetWidth||media.offsetWidth||0));
    if(w<=1)return;
    const px=w+'px';
    card.style.setProperty('--wenik-card-media-px',px);

    const mediaStyle=[
      'position:relative!important','display:block!important','width:100%!important',
      'height:'+px+'!important','min-height:'+px+'!important','max-height:'+px+'!important',
      'flex:0 0 '+px+'!important','aspect-ratio:auto!important','overflow:hidden!important'
    ].join(';');
    if(media.getAttribute('style')!==mediaStyle)media.setAttribute('style',mediaStyle);

    const imgStyle=[
      'position:absolute!important','inset:0!important','display:block!important',
      'width:100%!important','height:100%!important','min-width:100%!important','min-height:100%!important',
      'max-width:none!important','max-height:none!important','object-fit:cover!important',
      'object-position:center center!important','margin:0!important','padding:0!important'
    ].join(';');
    if(img.getAttribute('style')!==imgStyle)img.setAttribute('style',imgStyle);
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

  function fixAll(){document.querySelectorAll(SEL).forEach(card=>{lockRealImage(card);fixMeta(card)})}
  function queue(){if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;fixAll()})}

  function boot(){
    fixAll();
    const mo=new MutationObserver(queue);
    mo.observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['style','src','class']});
    window.__wenikPartnerMediaMO=mo;
    if('ResizeObserver'in window){
      const ro=new ResizeObserver(queue);
      document.querySelectorAll('.wenikPartnerGrid').forEach(el=>ro.observe(el));
      ro.observe(document.documentElement);
      window.__wenikPartnerMediaRO=ro;
    }
    addEventListener('resize',queue,{passive:true});
    addEventListener('orientationchange',queue,{passive:true});
    [0,50,120,250,500,900,1500,2500,4000,7000].forEach(ms=>setTimeout(fixAll,ms));
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
<!-- WENIK PARTNER CARDS UNIFORM V1 END -->'''

# Replace our previous block with the single final implementation.
if start in s and end in s:
    s = re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda _m: block, s, flags=re.S)
else:
    pos = s.lower().rfind('</body>')
    if pos == -1:
        raise SystemExit('index.html has no </body>')
    s = s[:pos] + block + '\n' + s[pos:]

# Old accumulated 4:3 declarations are not allowed to fight the final customer-card rule.
s = s.replace('aspect-ratio:4/3!important;', 'aspect-ratio:1/1!important;')
s = s.replace('aspect-ratio: 4/3!important;', 'aspect-ratio:1/1!important;')
s = s.replace('aspect-ratio:4 / 3!important;', 'aspect-ratio:1/1!important;')

p.write_text(s, encoding='utf-8')
print('Applied final WENIK equal square real-image card lock')
