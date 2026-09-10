from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK CUSTOMER PARTNER IMAGE REPAIR AFTER V5 V1 */'

# V5 can rewrite the card renderer on every workflow run. Restore the data attribute
# required by the approved-image hydration logic, even when the older fix marker exists.
base="""function wenikPartnerCard(x){const d=partnerDiscount(x),cat=displayPartnerCategory(x.category),logo=x.logo_url?'<img src=\"'+esc(x.logo_url)+'\" alt=\"'+esc(x.business_name)+'\" loading=\"lazy\">':'<div class=\"wenikPartnerPlaceholder\">WENIK</div>';return'<article class=\"wenikPartnerCard\" tabindex=\"0\" onclick=\"openWenikPartner(\\''+x.partner_id+'\\')\" onkeydown=\"if(event.key===\\'Enter\\'||event.key===\\' \\'){event.preventDefault();openWenikPartner(\\''+x.partner_id+'\\')}>'+(d?'<div class=\"wenikOff\">'+esc(d)+'</div>':'')+'<div class=\"wenikPartnerMedia\">'+logo+'</div><div class=\"wenikPartnerBody\"><div class=\"wenikPartnerName\">'+esc(x.business_name)+'</div><div class=\"wenikPartnerMeta\">'+esc([cat,x.area].filter(Boolean).join(' • '))+'</div><div class=\"wenikPartnerPromo\">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}"""
fixed="""function wenikPartnerCard(x){const d=partnerDiscount(x),cat=displayPartnerCategory(x.category),logo=x.logo_url?'<img src=\"'+esc(x.logo_url)+'\" alt=\"'+esc(x.business_name)+'\" loading=\"lazy\">':'<div class=\"wenikPartnerPlaceholder\">WENIK</div>';return'<article class=\"wenikPartnerCard\" data-wenik-partner-id=\"'+esc(x.partner_id)+'\" tabindex=\"0\" onclick=\"openWenikPartner(\\''+x.partner_id+'\\')\" onkeydown=\"if(event.key===\\'Enter\\'||event.key===\\' \\'){event.preventDefault();openWenikPartner(\\''+x.partner_id+'\\')}>'+(d?'<div class=\"wenikOff\">'+esc(d)+'</div>':'')+'<div class=\"wenikPartnerMedia\">'+logo+'</div><div class=\"wenikPartnerBody\"><div class=\"wenikPartnerName\">'+esc(x.business_name)+'</div><div class=\"wenikPartnerMeta\">'+esc([cat,x.area].filter(Boolean).join(' • '))+'</div><div class=\"wenikPartnerPromo\">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}"""
if 'data-wenik-partner-id' not in s:
    if base not in s: raise SystemExit('Partner card renderer anchor missing')
    s=s.replace(base,fixed,1)

if 'async function getWenikPartnerApprovedImage' not in s or 'function observeWenikPartnerCardImages' not in s:
    raise SystemExit('Approved-image hydration helpers missing')

home_old="""$('homePartnerGrid').innerHTML=list.length?list.map(wenikPartnerCard).join(''):(hasFilter?'<div class=\"wenikEmpty\">No partners found for this selection yet.</div>':'<div class=\"wenikEmpty\">WENIK partners will appear here as they are added.</div>')}"""
home_new="""$('homePartnerGrid').innerHTML=list.length?list.map(wenikPartnerCard).join(''):(hasFilter?'<div class=\"wenikEmpty\">No partners found for this selection yet.</div>':'<div class=\"wenikEmpty\">WENIK partners will appear here as they are added.</div>');observeWenikPartnerCardImages()}"""
if home_old in s: s=s.replace(home_old,home_new,1)

list_old="""$('partnerList').innerHTML=list.length?list.map(wenikPartnerCard).join(''):'<div class=\"wenikEmpty\">No partners match your search.</div>'\n}"""
list_new="""$('partnerList').innerHTML=list.length?list.map(wenikPartnerCard).join(''):'<div class=\"wenikEmpty\">No partners match your search.</div>';\n  observeWenikPartnerCardImages()\n}"""
if list_old in s: s=s.replace(list_old,list_new,1)

# Keep modal-area behavior intact if V5 rewrote the open/close functions.
open_old="""window.openWenikPartner=async id=>{const x=(partnerDirectory||[]).find(v=>String(v.partner_id)===String(id));if(!x)return;const a=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]),socials=x.social_links||{},hero=a?.[0]?.image_url||x.logo_url||'',d=partnerDiscount(x),links=[];"""
open_new="""window.openWenikPartner=async id=>{const x=(partnerDirectory||[]).find(v=>String(v.partner_id)===String(id));if(!x)return;hideWenikAreaSearchForDetail(true);const a=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]),socials=x.social_links||{},hero=a?.find(v=>v?.image_url)?.image_url||WENIK_PARTNER_IMAGE_CACHE.get(String(id))||x.logo_url||'',d=partnerDiscount(x),links=[];"""
if open_old in s: s=s.replace(open_old,open_new,1)
close_old="window.closeWenikPartner=()=>{$('wenikPartnerModal').classList.add('hidden');document.body.style.overflow=''};"
close_new="window.closeWenikPartner=()=>{$('wenikPartnerModal').classList.add('hidden');document.body.style.overflow='';hideWenikAreaSearchForDetail(false)};"
if close_old in s: s=s.replace(close_old,close_new,1)

if marker not in s:
    s=s.replace('/* WENIK CUSTOMER PARTNER CARD IMAGE + MODAL AREA FIX V1 */',marker+'\n/* WENIK CUSTOMER PARTNER CARD IMAGE + MODAL AREA FIX V1 */',1)

p.write_text(s,encoding='utf-8')
print('Customer Partner image hydration repaired after V5')
