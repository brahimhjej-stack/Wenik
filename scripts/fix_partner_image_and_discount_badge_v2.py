from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK PARTNER IMAGE + DISCOUNT BADGE V2 */'
if marker in s:
    raise SystemExit('already applied')

# Put the discount badge inside the media container so it is always anchored over the image.
old="""function wenikPartnerCard(x){const d=partnerDiscount(x),cat=displayPartnerCategory(x.category),logo=x.logo_url?'<img src=\"'+esc(x.logo_url)+'\" alt=\"'+esc(x.business_name)+'\" loading=\"lazy\">':'<div class=\"wenikPartnerPlaceholder\">WENIK</div>';return'<article class=\"wenikPartnerCard\" data-wenik-partner-id=\"'+esc(x.partner_id)+'\" tabindex=\"0\" onclick=\"openWenikPartner(\\''+x.partner_id+'\\')\" onkeydown=\"if(event.key===\\'Enter\\'||event.key===\\' \\'){event.preventDefault();openWenikPartner(\\''+x.partner_id+'\\')}>'+(d?'<div class=\"wenikOff\">'+esc(d)+'</div>':'')+'<div class=\"wenikPartnerMedia\">'+logo+'</div><div class=\"wenikPartnerBody\"><div class=\"wenikPartnerName\">'+esc(x.business_name)+'</div><div class=\"wenikPartnerMeta\">'+esc([cat,x.area].filter(Boolean).join(' • '))+'</div><div class=\"wenikPartnerPromo\">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}"""
new="""function wenikPartnerCard(x){const d=partnerDiscount(x),cat=displayPartnerCategory(x.category),logo=x.logo_url?'<img src=\"'+esc(x.logo_url)+'\" alt=\"'+esc(x.business_name)+'\" loading=\"lazy\">':'<div class=\"wenikPartnerPlaceholder\">WENIK</div>';return'<article class=\"wenikPartnerCard\" data-wenik-partner-id=\"'+esc(x.partner_id)+'\" tabindex=\"0\" onclick=\"openWenikPartner(\\''+x.partner_id+'\\')\" onkeydown=\"if(event.key===\\'Enter\\'||event.key===\\' \\'){event.preventDefault();openWenikPartner(\\''+x.partner_id+'\\')}><div class=\"wenikPartnerMedia\">'+logo+(d?'<div class=\"wenikOff\">'+esc(d)+'</div>':'')+'</div><div class=\"wenikPartnerBody\"><div class=\"wenikPartnerName\">'+esc(x.business_name)+'</div><div class=\"wenikPartnerMeta\">'+esc([cat,x.area].filter(Boolean).join(' • '))+'</div><div class=\"wenikPartnerPromo\">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}"""
if old not in s:
    raise SystemExit('Partner card renderer anchor missing')
s=s.replace(old,new,1)

# Never permanently cache an empty approved-image response; retry transient misses.
old_fn="""async function getWenikPartnerApprovedImage(id){
  id=String(id||'');
  if(!id)return'';
  if(WENIK_PARTNER_IMAGE_CACHE.has(id))return WENIK_PARTNER_IMAGE_CACHE.get(id)||'';
  if(WENIK_PARTNER_IMAGE_PENDING.has(id))return WENIK_PARTNER_IMAGE_PENDING.get(id);
  const req=(async()=>{const rows=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]);const url=(rows||[]).find(x=>x?.image_url)?.image_url||'';WENIK_PARTNER_IMAGE_CACHE.set(id,url);WENIK_PARTNER_IMAGE_PENDING.delete(id);return url})();
  WENIK_PARTNER_IMAGE_PENDING.set(id,req);return req;
}"""
new_fn="""async function getWenikPartnerApprovedImage(id){
  id=String(id||'');
  if(!id)return'';
  const cached=WENIK_PARTNER_IMAGE_CACHE.get(id);if(cached)return cached;
  if(WENIK_PARTNER_IMAGE_PENDING.has(id))return WENIK_PARTNER_IMAGE_PENDING.get(id);
  const req=(async()=>{let url='';for(let attempt=0;attempt<3&&!url;attempt++){const rows=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]);url=(rows||[]).find(x=>x?.image_url)?.image_url||'';if(!url&&attempt<2)await new Promise(r=>setTimeout(r,350*(attempt+1)))}if(url)WENIK_PARTNER_IMAGE_CACHE.set(id,url);WENIK_PARTNER_IMAGE_PENDING.delete(id);return url})();
  WENIK_PARTNER_IMAGE_PENDING.set(id,req);return req;
}"""
if old_fn not in s:
    raise SystemExit('Approved image helper anchor missing')
s=s.replace(old_fn,new_fn,1)

old_hyd="""async function hydrateWenikPartnerCard(card){
  if(!card||card.dataset.wenikImageHydrated==='1')return;
  card.dataset.wenikImageHydrated='1';
  const id=card.dataset.wenikPartnerId;if(!id)return;
  const url=await getWenikPartnerApprovedImage(id);if(!url)return;
  const media=card.querySelector('.wenikPartnerMedia');if(!media||!card.isConnected)return;
  const partner=(partnerDirectory||[]).find(x=>String(x.partner_id)===String(id));
  media.innerHTML='<img src=\"'+esc(url)+'\" alt=\"'+esc(partner?.business_name||'WENIK Partner')+'\" loading=\"lazy\" decoding=\"async\">';
}"""
new_hyd="""async function hydrateWenikPartnerCard(card){
  if(!card||card.dataset.wenikImageHydrated==='1')return;
  const id=card.dataset.wenikPartnerId;if(!id)return;
  const url=await getWenikPartnerApprovedImage(id);if(!url)return;
  const media=card.querySelector('.wenikPartnerMedia');if(!media||!card.isConnected)return;
  const partner=(partnerDirectory||[]).find(x=>String(x.partner_id)===String(id));
  const badge=media.querySelector('.wenikOff');
  media.innerHTML='<img src=\"'+esc(url)+'\" alt=\"'+esc(partner?.business_name||'WENIK Partner')+'\" loading=\"lazy\" decoding=\"async\">';
  if(badge)media.appendChild(badge);
  card.dataset.wenikImageHydrated='1';
}"""
if old_hyd not in s:
    raise SystemExit('Hydration function anchor missing')
s=s.replace(old_hyd,new_hyd,1)

style=r'''
<style id="wenikPartnerImageDiscountBadgeV2">
/* WENIK PARTNER IMAGE + DISCOUNT BADGE V2 */
.wenikPartnerMedia{position:relative!important;overflow:hidden!important}
.wenikPartnerMedia .wenikOff{
  position:absolute!important;top:10px!important;left:10px!important;right:auto!important;bottom:auto!important;
  z-index:30!important;width:auto!important;max-width:calc(100% - 20px)!important;margin:0!important;
  padding:7px 10px!important;border-radius:999px!important;white-space:nowrap!important;
  background:rgba(255,255,255,.96)!important;color:#d95b16!important;border:1px solid rgba(255,255,255,.92)!important;
  box-shadow:0 6px 18px rgba(20,12,30,.20)!important;font-size:11px!important;font-weight:950!important;line-height:1!important;
  backdrop-filter:blur(8px)!important;-webkit-backdrop-filter:blur(8px)!important;
}
@media(max-width:390px){.wenikPartnerMedia .wenikOff{top:8px!important;left:8px!important;padding:6px 8px!important;font-size:10px!important}}
</style>
'''
if '</head>' not in s: raise SystemExit('head anchor missing')
s=s.replace('</head>',style+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Robust Partner image + discount badge V2 applied')
