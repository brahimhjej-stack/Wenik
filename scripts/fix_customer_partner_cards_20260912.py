from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = '<!-- WENIK PARTNER CARDS UNIFORM V1 START -->'
end = '<!-- WENIK PARTNER CARDS UNIFORM V1 END -->'

block = r'''<!-- WENIK PARTNER CARDS UNIFORM V1 START -->
<style id="wenikPartnerCardsUniformV1">
/* FINAL V5: one self-contained card = square image + body. */
.wenikPartnerGrid{align-items:start!important;grid-auto-rows:auto!important}
.wenikPartnerCard{display:flex!important;flex-direction:column!important;align-self:start!important;height:auto!important;min-height:0!important;max-height:none!important;overflow:hidden!important;border-radius:22px!important;background:#fff!important}
.wenikPartnerCard .wenikPartnerMedia{position:relative!important;display:block!important;width:100%!important;height:auto!important;min-height:0!important;max-height:none!important;aspect-ratio:1/1!important;flex:0 0 auto!important;overflow:hidden!important;box-sizing:border-box!important}
.wenikPartnerCard .wenikPartnerMedia>img{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;min-width:100%!important;min-height:100%!important;max-width:none!important;max-height:none!important;object-fit:cover!important;object-position:center!important;margin:0!important;padding:0!important}
.wenikPartnerCard .wenikPartnerPlaceholder{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;display:grid!important;place-items:center!important}
.wenikPartnerCard .wenikPartnerBody{position:relative!important;display:block!important;flex:0 0 auto!important;width:100%!important;height:auto!important;min-height:118px!important;max-height:none!important;box-sizing:border-box!important;padding:10px 10px 12px!important;background:#fff!important;overflow:visible!important}
.wenikPartnerCard .wenikPartnerName{display:block!important;position:relative!important;visibility:visible!important;opacity:1!important;height:auto!important;min-height:17px!important}
.wenikPartnerCard .wenikPartnerMeta{display:block!important;position:relative!important;visibility:visible!important;opacity:1!important;height:auto!important;min-height:14px!important}
@media(max-width:390px){.wenikPartnerCard{border-radius:19px!important}.wenikPartnerCard .wenikPartnerBody{min-height:112px!important}}
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
  function hardLock(card){
    if(!card)return;
    for(const [k,v] of [['display','flex'],['flex-direction','column'],['height','auto'],['min-height','0'],['max-height','none'],['overflow','hidden']])card.style.setProperty(k,v,'important');
    const media=card.querySelector('.wenikPartnerMedia');
    const body=card.querySelector('.wenikPartnerBody');
    if(media){
      for(const [k,v] of [['position','relative'],['display','block'],['width','100%'],['height','auto'],['min-height','0'],['max-height','none'],['aspect-ratio','1 / 1'],['flex','0 0 auto'],['overflow','hidden']])media.style.setProperty(k,v,'important');
      const img=media.querySelector('img');
      if(img)for(const [k,v] of [['position','absolute'],['inset','0'],['width','100%'],['height','100%'],['object-fit','cover'],['object-position','center']])img.style.setProperty(k,v,'important');
    }
    if(body){
      for(const [k,v] of [['position','relative'],['display','block'],['width','100%'],['height','auto'],['min-height','118px'],['max-height','none'],['flex','0 0 auto'],['visibility','visible'],['opacity','1'],['overflow','visible'],['background','#fff']])body.style.setProperty(k,v,'important');
      body.querySelectorAll('.wenikPartnerName,.wenikPartnerMeta,.wenikPartnerPromo,.wenikPartnerFooter').forEach(el=>{el.style.setProperty('visibility','visible','important');el.style.setProperty('opacity','1','important')});
    }
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
    const wanted=area&&category?'📍 '+area+' · '+category:area?'📍 '+area:category?category:'';
    if(wanted&&meta.textContent!==wanted)meta.textContent=wanted;
  }
  function fixAll(){document.querySelectorAll('.wenikPartnerCard').forEach(card=>{hardLock(card);fixMeta(card)})}
  let queued=false;
  function queue(){if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;fixAll()})}
  function boot(){fixAll();new MutationObserver(queue).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['style','class','src']});addEventListener('resize',queue,{passive:true});[0,50,150,300,700,1500,3000].forEach(ms=>setTimeout(fixAll,ms))}
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

for old in ('aspect-ratio:4/3!important;','aspect-ratio: 4/3!important;','aspect-ratio:4 / 3!important;','aspect-ratio:16/10!important;','aspect-ratio: 16/10!important;','aspect-ratio:16 / 10!important;'):
    s = s.replace(old, 'aspect-ratio:1/1!important;')

# Replace the card renderer itself. Inline !important keeps the image and its text body together.
new_renderer = r'''function wenikPartnerCard(x){const d=partnerDiscount(x),cat=displayPartnerCategory(x.category),img=x.logo_url?'<img style="position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:cover!important;object-position:center!important" src="'+esc(x.logo_url)+'" alt="'+esc(x.business_name)+'" loading="lazy" decoding="async">':'<div class="wenikPartnerPlaceholder">WENIK</div>';return'<article class="wenikPartnerCard" data-wenik-partner-id="'+esc(x.partner_id)+'" style="display:flex!important;flex-direction:column!important;height:auto!important;min-height:0!important;overflow:hidden!important" tabindex="0" onclick="openWenikPartner(\\''+x.partner_id+'\\')" onkeydown="if(event.key===\\'Enter\\'||event.key===\\' \\'){event.preventDefault();openWenikPartner(\\''+x.partner_id+'\\')}"><div class="wenikPartnerMedia" style="position:relative!important;display:block!important;width:100%!important;height:auto!important;aspect-ratio:1/1!important;overflow:hidden!important;flex:0 0 auto!important">'+img+(d?'<div class="wenikOff">'+esc(d)+'</div>':'')+'</div><div class="wenikPartnerBody" style="position:relative!important;display:block!important;width:100%!important;height:auto!important;min-height:118px!important;flex:0 0 auto!important;visibility:visible!important;opacity:1!important;background:#fff!important"><div class="wenikPartnerName" style="display:block!important;visibility:visible!important;opacity:1!important">'+esc(x.business_name)+'</div><div class="wenikPartnerMeta" style="display:block!important;visibility:visible!important;opacity:1!important">'+esc([x.area,cat].filter(Boolean).join(' · '))+'</div><div class="wenikPartnerPromo">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}'''
s = re.sub(r'function wenikPartnerCard\(x\)\{.*?\}\n\nfunction categoryFamilyMatch', lambda m: new_renderer + '\n\nfunction categoryFamilyMatch', s, count=1, flags=re.S)

# Home list: partners with complete approved image/profile appear first; this restores Beit El Kel Bites and Dimassi in Nabatieh.
new_home = r'''function renderHomePartners(){if(!$('homePartnerGrid'))return;const filtered=(partnerDirectory||[]).filter(x=>partnerMatches(x,'',homePartnerAreaSaved,homePartnerCategory)).sort((a,b)=>{const ai=a.logo_url?1:0,bi=b.logo_url?1:0;if(ai!==bi)return bi-ai;const ab=a.benefit_title?1:0,bb=b.benefit_title?1:0;if(ab!==bb)return bb-ab;return String(a.business_name||'').localeCompare(String(b.business_name||''))}),list=filtered.slice(0,6),hasFilter=!!(homePartnerAreaSaved||homePartnerCategory);$('homePartnerGrid').innerHTML=list.length?list.map(wenikPartnerCard).join(''):(hasFilter?'<div class="wenikEmpty">No partners found for this selection yet.</div>':'<div class="wenikEmpty">WENIK partners will appear here as they are added.</div>');observeWenikPartnerCardImages()}'''
s = re.sub(r'function renderHomePartners\(\)\{.*?\}\nfunction renderHomePartnerCategories', lambda m: new_home + '\nfunction renderHomePartnerCategories', s, count=1, flags=re.S)

p.write_text(s, encoding='utf-8')
print('Applied WENIK partner-card V5: image and text stay together; complete Nabatieh partners prioritized')
