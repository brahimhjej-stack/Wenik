from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = '<!-- WENIK PARTNER CARDS UNIFORM V1 START -->'
end = '<!-- WENIK PARTNER CARDS UNIFORM V1 END -->'

block = r'''<!-- WENIK PARTNER CARDS UNIFORM V1 START -->
<style id="wenikPartnerCardsUniformV1">
/* FINAL V4: every visible partner image uses the exact card width as its image height. */
.wenikPartnerGrid{align-items:start!important;grid-auto-rows:auto!important}
.wenikPartnerCard{display:flex!important;flex-direction:column!important;align-self:start!important;height:auto!important;min-height:0!important;max-height:none!important;overflow:hidden!important;border-radius:22px!important;background:#fff!important}
.wenikPartnerCard .wenikPartnerMedia{position:relative!important;display:block!important;width:100%!important;aspect-ratio:1/1!important;flex:none!important;overflow:hidden!important;box-sizing:border-box!important;background:linear-gradient(135deg,#f4ebff,#fff1e8,#fff8d9)!important}
.wenikPartnerCard .wenikPartnerMedia>img{position:absolute!important;inset:0!important;display:block!important;width:100%!important;height:100%!important;min-width:100%!important;min-height:100%!important;max-width:none!important;max-height:none!important;object-fit:cover!important;object-position:center center!important;margin:0!important;padding:0!important}
.wenikPartnerCard .wenikPartnerPlaceholder{position:absolute!important;inset:0!important;display:grid!important;place-items:center!important;width:100%!important;height:100%!important}
.wenikPartnerCard .wenikPartnerBody{flex:none!important;height:auto!important;min-height:0!important;max-height:none!important}
@media(max-width:390px){.wenikPartnerCard{border-radius:19px!important}}
</style>
<script id="wenikPartnerCardsUniformRuntimeV1">
(function(){
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
  function lockSquare(card){
    if(!card||!card.isConnected)return;
    const media=card.querySelector('.wenikPartnerMedia');
    if(!media)return;
    const width=Math.round(card.getBoundingClientRect().width||media.getBoundingClientRect().width||card.offsetWidth||0);
    if(width<2)return;
    const px=width+'px';
    media.style.setProperty('width','100%','important');
    media.style.setProperty('height',px,'important');
    media.style.setProperty('min-height',px,'important');
    media.style.setProperty('max-height',px,'important');
    media.style.setProperty('aspect-ratio','1 / 1','important');
    media.style.setProperty('flex','0 0 '+px,'important');
    media.style.setProperty('position','relative','important');
    media.style.setProperty('overflow','hidden','important');
    const img=media.querySelector('img');
    if(img){
      img.style.setProperty('position','absolute','important');
      img.style.setProperty('inset','0','important');
      img.style.setProperty('width','100%','important');
      img.style.setProperty('height','100%','important');
      img.style.setProperty('object-fit','cover','important');
      img.style.setProperty('object-position','center center','important');
    }
    card.style.setProperty('height','auto','important');
    card.style.setProperty('min-height','0','important');
    card.style.setProperty('align-self','start','important');
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
  function fixAll(){document.querySelectorAll('.wenikPartnerCard').forEach(card=>{lockSquare(card);fixMeta(card)})}
  function queue(){if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;fixAll()})}
  function boot(){
    fixAll();
    const mo=new MutationObserver(queue);
    mo.observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['style','class','src']});
    if('ResizeObserver' in window){const ro=new ResizeObserver(queue);ro.observe(document.documentElement);document.querySelectorAll('.wenikPartnerGrid').forEach(x=>ro.observe(x));window.__wenikPartnerSquareRO=ro}
    addEventListener('resize',queue,{passive:true});
    addEventListener('orientationchange',queue,{passive:true});
    [0,50,120,250,500,900,1500,2500,4000].forEach(ms=>setTimeout(fixAll,ms));
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

# Neutralize accumulated competing aspect-ratios on partner media.
s = re.sub(r'(\.wenikPartnerMedia[^{}]*\{[^{}]*?)aspect-ratio\s*:\s*[^;}]+' , lambda m: m.group(1)+'aspect-ratio:1/1!important', s)

p.write_text(s, encoding='utf-8')
print('Applied WENIK partner-card V4: exact square media lock on every card')
