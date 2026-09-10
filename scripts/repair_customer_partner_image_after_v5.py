from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK CUSTOMER PARTNER IMAGE REPAIR AFTER V5 V2 */'

# V5 rewrites the renderer on every workflow run. Replace the renderer itself so:
# 1) the approved image returned as logo_url is painted immediately;
# 2) the discount badge is physically inside the media box, never above the card.
renderer="""function wenikPartnerCard(x){const d=partnerDiscount(x),cat=displayPartnerCategory(x.category),logo=x.logo_url?'<img src=\"'+esc(x.logo_url)+'\" alt=\"'+esc(x.business_name)+'\" loading=\"lazy\" decoding=\"async\">':'<div class=\"wenikPartnerPlaceholder\">WENIK</div>';return'<article class=\"wenikPartnerCard\" data-wenik-partner-id=\"'+esc(x.partner_id)+'\" tabindex=\"0\" onclick=\"openWenikPartner(\\''+x.partner_id+'\\')\" onkeydown=\"if(event.key===\\'Enter\\'||event.key===\\' \\'){event.preventDefault();openWenikPartner(\\''+x.partner_id+'\\')}><div class=\"wenikPartnerMedia\">'+logo+(d?'<div class=\"wenikOff\">'+esc(d)+'</div>':'')+'</div><div class=\"wenikPartnerBody\"><div class=\"wenikPartnerName\">'+esc(x.business_name)+'</div><div class=\"wenikPartnerMeta\">'+esc([cat,x.area].filter(Boolean).join(' • '))+'</div><div class=\"wenikPartnerPromo\">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}"""

pattern=r"function wenikPartnerCard\(x\)\{.*?\}\n\nfunction categoryFamilyMatch"
if not re.search(pattern,s,flags=re.S):
    raise SystemExit('Partner card renderer anchor missing')
s=re.sub(pattern,renderer+'\n\nfunction categoryFamilyMatch',s,count=1,flags=re.S)

if 'async function getWenikPartnerApprovedImage' not in s or 'function observeWenikPartnerCardImages' not in s:
    raise SystemExit('Approved-image hydration helpers missing')

home_old="""$('homePartnerGrid').innerHTML=list.length?list.map(wenikPartnerCard).join(''):(hasFilter?'<div class=\"wenikEmpty\">No partners found for this selection yet.</div>':'<div class=\"wenikEmpty\">WENIK partners will appear here as they are added.</div>')}"""
home_new="""$('homePartnerGrid').innerHTML=list.length?list.map(wenikPartnerCard).join(''):(hasFilter?'<div class=\"wenikEmpty\">No partners found for this selection yet.</div>':'<div class=\"wenikEmpty\">WENIK partners will appear here as they are added.</div>');observeWenikPartnerCardImages()}"""
if home_old in s:s=s.replace(home_old,home_new,1)

list_old="""$('partnerList').innerHTML=list.length?list.map(wenikPartnerCard).join(''):'<div class=\"wenikEmpty\">No partners match your search.</div>'\n}"""
list_new="""$('partnerList').innerHTML=list.length?list.map(wenikPartnerCard).join(''):'<div class=\"wenikEmpty\">No partners match your search.</div>';\n  observeWenikPartnerCardImages()\n}"""
if list_old in s:s=s.replace(list_old,list_new,1)

# Keep modal-area behavior intact if V5 rewrote the open/close functions.
open_old="""window.openWenikPartner=async id=>{const x=(partnerDirectory||[]).find(v=>String(v.partner_id)===String(id));if(!x)return;const a=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]),socials=x.social_links||{},hero=a?.[0]?.image_url||x.logo_url||'',d=partnerDiscount(x),links=[];"""
open_new="""window.openWenikPartner=async id=>{const x=(partnerDirectory||[]).find(v=>String(v.partner_id)===String(id));if(!x)return;hideWenikAreaSearchForDetail(true);const a=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]),socials=x.social_links||{},hero=a?.find(v=>v?.image_url)?.image_url||WENIK_PARTNER_IMAGE_CACHE.get(String(id))||x.logo_url||'',d=partnerDiscount(x),links=[];"""
if open_old in s:s=s.replace(open_old,open_new,1)
close_old="window.closeWenikPartner=()=>{$('wenikPartnerModal').classList.add('hidden');document.body.style.overflow=''};"
close_new="window.closeWenikPartner=()=>{$('wenikPartnerModal').classList.add('hidden');document.body.style.overflow='';hideWenikAreaSearchForDetail(false)};"
if close_old in s:s=s.replace(close_old,close_new,1)

# Strong final CSS wins over older Partner-card rules.
css=r'''\n<style id="wenikPartnerCardDirectFixV2">\n/* WENIK CUSTOMER PARTNER IMAGE REPAIR AFTER V5 V2 */\n.wenikPartnerCard .wenikPartnerMedia{position:relative!important;overflow:hidden!important}\n.wenikPartnerCard .wenikPartnerMedia>.wenikOff{position:absolute!important;top:9px!important;left:9px!important;right:auto!important;bottom:auto!important;z-index:99!important;width:auto!important;max-width:calc(100% - 18px)!important;margin:0!important;padding:6px 9px!important;border-radius:999px!important;background:linear-gradient(135deg,#ff6b00,#ff3d00)!important;color:#fff!important;border:1px solid rgba(255,255,255,.55)!important;box-shadow:0 5px 15px rgba(27,12,12,.28)!important;font-size:11px!important;font-weight:900!important;line-height:1!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}\n.wenikPartnerCard .wenikPartnerMedia>img{width:100%!important;height:100%!important;display:block!important;object-fit:cover!important;object-position:center!important}\n</style>\n'''
if marker not in s:
    if '</head>' not in s:raise SystemExit('head anchor missing')
    s=s.replace('</head>',css+'\n</head>',1)

p.write_text(s,encoding='utf-8')
print('Customer Partner renderer repaired directly after V5')
