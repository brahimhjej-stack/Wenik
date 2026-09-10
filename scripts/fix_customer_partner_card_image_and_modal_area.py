from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK CUSTOMER PARTNER CARD IMAGE + MODAL AREA FIX V1 */'
if marker in s:
    raise SystemExit('already applied')
if '/* WENIK PARTNER DISCOVERY V5' not in s:
    raise SystemExit('Partner Discovery V5 marker missing')

# 1) Card markup: add partner id so visible cards can be hydrated with the same approved image used in Partner detail.
old="""function wenikPartnerCard(x){const d=partnerDiscount(x),cat=displayPartnerCategory(x.category),logo=x.logo_url?'<img src=\"'+esc(x.logo_url)+'\" alt=\"'+esc(x.business_name)+'\" loading=\"lazy\">':'<div class=\"wenikPartnerPlaceholder\">WENIK</div>';return'<article class=\"wenikPartnerCard\" tabindex=\"0\" onclick=\"openWenikPartner(\\''+x.partner_id+'\\')\" onkeydown=\"if(event.key===\\'Enter\\'||event.key===\\' \\'){event.preventDefault();openWenikPartner(\\''+x.partner_id+'\\')}>'+(d?'<div class=\"wenikOff\">'+esc(d)+'</div>':'')+'<div class=\"wenikPartnerMedia\">'+logo+'</div><div class=\"wenikPartnerBody\"><div class=\"wenikPartnerName\">'+esc(x.business_name)+'</div><div class=\"wenikPartnerMeta\">'+esc([cat,x.area].filter(Boolean).join(' • '))+'</div><div class=\"wenikPartnerPromo\">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}"""
new="""function wenikPartnerCard(x){const d=partnerDiscount(x),cat=displayPartnerCategory(x.category),logo=x.logo_url?'<img src=\"'+esc(x.logo_url)+'\" alt=\"'+esc(x.business_name)+'\" loading=\"lazy\">':'<div class=\"wenikPartnerPlaceholder\">WENIK</div>';return'<article class=\"wenikPartnerCard\" data-wenik-partner-id=\"'+esc(x.partner_id)+'\" tabindex=\"0\" onclick=\"openWenikPartner(\\''+x.partner_id+'\\')\" onkeydown=\"if(event.key===\\'Enter\\'||event.key===\\' \\'){event.preventDefault();openWenikPartner(\\''+x.partner_id+'\\')}>'+(d?'<div class=\"wenikOff\">'+esc(d)+'</div>':'')+'<div class=\"wenikPartnerMedia\">'+logo+'</div><div class=\"wenikPartnerBody\"><div class=\"wenikPartnerName\">'+esc(x.business_name)+'</div><div class=\"wenikPartnerMeta\">'+esc([cat,x.area].filter(Boolean).join(' • '))+'</div><div class=\"wenikPartnerPromo\">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}"""
if old not in s:
    raise SystemExit('wenikPartnerCard anchor missing')
s=s.replace(old,new,1)

# 2) Add lazy approved-image hydration + area hide helper before area options.
anchor="function buildAreaOptions(selected='')"
insert=r'''/* WENIK CUSTOMER PARTNER CARD IMAGE + MODAL AREA FIX V1 */
const WENIK_PARTNER_IMAGE_CACHE=new Map();
const WENIK_PARTNER_IMAGE_PENDING=new Map();
async function getWenikPartnerApprovedImage(id){
  id=String(id||'');
  if(!id)return'';
  if(WENIK_PARTNER_IMAGE_CACHE.has(id))return WENIK_PARTNER_IMAGE_CACHE.get(id)||'';
  if(WENIK_PARTNER_IMAGE_PENDING.has(id))return WENIK_PARTNER_IMAGE_PENDING.get(id);
  const req=(async()=>{const rows=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]);const url=(rows||[]).find(x=>x?.image_url)?.image_url||'';WENIK_PARTNER_IMAGE_CACHE.set(id,url);WENIK_PARTNER_IMAGE_PENDING.delete(id);return url})();
  WENIK_PARTNER_IMAGE_PENDING.set(id,req);return req;
}
async function hydrateWenikPartnerCard(card){
  if(!card||card.dataset.wenikImageHydrated==='1')return;
  card.dataset.wenikImageHydrated='1';
  const id=card.dataset.wenikPartnerId;if(!id)return;
  const url=await getWenikPartnerApprovedImage(id);if(!url)return;
  const media=card.querySelector('.wenikPartnerMedia');if(!media||!card.isConnected)return;
  const partner=(partnerDirectory||[]).find(x=>String(x.partner_id)===String(id));
  media.innerHTML='<img src="'+esc(url)+'" alt="'+esc(partner?.business_name||'WENIK Partner')+'" loading="lazy" decoding="async">';
}
let WENIK_PARTNER_IMAGE_OBSERVER=null;
function observeWenikPartnerCardImages(){
  const cards=[...document.querySelectorAll('.wenikPartnerCard[data-wenik-partner-id]')].filter(c=>c.dataset.wenikObserved!=='1');
  if(!cards.length)return;
  if(!('IntersectionObserver'in window)){cards.slice(0,24).forEach(hydrateWenikPartnerCard);return}
  if(!WENIK_PARTNER_IMAGE_OBSERVER)WENIK_PARTNER_IMAGE_OBSERVER=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){WENIK_PARTNER_IMAGE_OBSERVER.unobserve(e.target);hydrateWenikPartnerCard(e.target)}},{rootMargin:'220px 0px'});
  cards.forEach(c=>{c.dataset.wenikObserved='1';WENIK_PARTNER_IMAGE_OBSERVER.observe(c)});
}
function hideWenikAreaSearchForDetail(hide){
  for(const id of ['partnerAreaSearchWrap','homePartnerAreaSearchWrap']){const el=document.getElementById(id);if(el)el.style.visibility=hide?'hidden':''}
  for(const id of ['partnerAreaMenu','homePartnerAreaMenu']){const el=document.getElementById(id);if(el)el.classList.add('hidden')}
}

'''
if anchor not in s: raise SystemExit('buildAreaOptions anchor missing')
s=s.replace(anchor,insert+anchor,1)

# 3) Trigger lazy hydration after every card render.
s=s.replace("$('homePartnerGrid').innerHTML=list.length?list.map(wenikPartnerCard).join(''):(hasFilter?'<div class=\"wenikEmpty\">No partners found for this selection yet.</div>':'<div class=\"wenikEmpty\">WENIK partners will appear here as they are added.</div>')}","$('homePartnerGrid').innerHTML=list.length?list.map(wenikPartnerCard).join(''):(hasFilter?'<div class=\"wenikEmpty\">No partners found for this selection yet.</div>':'<div class=\"wenikEmpty\">WENIK partners will appear here as they are added.</div>');observeWenikPartnerCardImages()}",1)
s=s.replace("$('partnerList').innerHTML=list.length?list.map(wenikPartnerCard).join(''):'<div class=\"wenikEmpty\">No partners match your search.</div>'\n}","$('partnerList').innerHTML=list.length?list.map(wenikPartnerCard).join(''):'<div class=\"wenikEmpty\">No partners match your search.</div>';\n  observeWenikPartnerCardImages()\n}",1)

# 4) Use cached approved image in detail when available, and hide area selectors while modal is open.
old_open="""window.openWenikPartner=async id=>{const x=(partnerDirectory||[]).find(v=>String(v.partner_id)===String(id));if(!x)return;const a=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]),socials=x.social_links||{},hero=a?.[0]?.image_url||x.logo_url||'',d=partnerDiscount(x),links=[];"""
new_open="""window.openWenikPartner=async id=>{const x=(partnerDirectory||[]).find(v=>String(v.partner_id)===String(id));if(!x)return;hideWenikAreaSearchForDetail(true);const a=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]),socials=x.social_links||{},hero=a?.find(v=>v?.image_url)?.image_url||WENIK_PARTNER_IMAGE_CACHE.get(String(id))||x.logo_url||'',d=partnerDiscount(x),links=[];"""
if old_open not in s: raise SystemExit('open partner anchor missing')
s=s.replace(old_open,new_open,1)
old_close="window.closeWenikPartner=()=>{$('wenikPartnerModal').classList.add('hidden');document.body.style.overflow=''};"
new_close="window.closeWenikPartner=()=>{$('wenikPartnerModal').classList.add('hidden');document.body.style.overflow='';hideWenikAreaSearchForDetail(false)};"
if old_close not in s: raise SystemExit('close partner anchor missing')
s=s.replace(old_close,new_close,1)

p.write_text(s,encoding='utf-8')
print('Customer partner card image + modal area fix applied')
