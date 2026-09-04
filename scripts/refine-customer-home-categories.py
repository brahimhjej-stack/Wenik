from pathlib import Path

p=Path('index.html')
h=p.read_text(encoding='utf-8')
marker='/* WENIK HOME CATEGORIES V2 */'
if marker in h:
    print('Already applied')
    raise SystemExit(0)

old='''        <div id="homePartnerCategories" class="wenikCategories"></div>\n        <div id="homePartnerGrid" class="wenikPartnerGrid"><div class="wenikEmpty">Loading partners…</div></div>'''
new='''        <div id="homePartnerGrid" class="wenikPartnerGrid"><div class="wenikEmpty">Loading partners…</div></div>\n        <div id="homePartnerCategories" class="wenikCategories" style="margin-top:14px"></div>'''
if old not in h:
    raise SystemExit('Home partner/category order anchor missing; refusing change')
h=h.replace(old,new,1)

old_icon="function partnerIcon(v=''){const c=normPartner(v);if(/restaurant|food|مطعم|اكل|أكل/.test(c))return'🍽️';if(/cafe|coffee|قهو|كاف/.test(c))return'☕';if(/fashion|cloth|wear|ملابس|البسة|ألبسة/.test(c))return'👕';if(/beauty|salon|spa|صالون|تجميل/.test(c))return'✨';if(/jewel|ذهب|مجوهر/.test(c))return'💎';if(/elect|phone|tech|كهرب|هاتف/.test(c))return'📱';if(/hotel|resort|فندق|منتجع/.test(c))return'🏨';if(/kids|play|entertain|اطفال|أطفال|ترفيه/.test(c))return'🎈';if(/service|خدمات/.test(c))return'🛠️';return'⭐'}"
new_icon="function partnerIcon(v=''){const c=normPartner(v);if(/restaurant|food|مطعم|اكل|أكل/.test(c))return'🍽️';if(/cafe|coffee|قهو|كاف/.test(c))return'☕';if(/sweet|dessert|حلويات/.test(c))return'🍰';if(/shoe|bag|احذية|أحذية|شنط|حقائب/.test(c))return'👟';if(/fashion|cloth|wear|ملابس|البسة|ألبسة/.test(c))return'👕';if(/beauty|تجميل/.test(c))return'💄';if(/hair|salon|barber|صالون|حلاق/.test(c))return'✂️';if(/jewel|ذهب|مجوهر/.test(c))return'💎';if(/elect|phone|tech|كهرب|هاتف/.test(c))return'📱';if(/furniture|اثاث|أثاث/.test(c))return'🛋️';if(/fitness|gym|رياض/.test(c))return'🏋️';if(/hotel|resort|فندق|منتجع/.test(c))return'🏨';if(/pool|swim|مسبح|مسابح/.test(c))return'🏊';if(/entertain|kids|play|اطفال|أطفال|ترفيه/.test(c))return'🎈';if(/auto|car|سيار/.test(c))return'🚗';if(/education|school|institute|تعليم|معهد/.test(c))return'🎓';if(/service|خدمات/.test(c))return'🛠️';return'⭐'}"
if old_icon not in h:
    raise SystemExit('partnerIcon anchor missing; refusing change')
h=h.replace(old_icon,new_icon,1)

old_render="function renderHomePartnerCategories(){if(!$('homePartnerCategories'))return;const cats=[...new Set((partnerDirectory||[]).map(x=>x.category).filter(Boolean))].sort((a,b)=>String(a).localeCompare(String(b)));$('homePartnerCategories').innerHTML='<button class=\"wenikCat '+(homePartnerCategory?'':'active')+'\" data-hcat=\"\"><span class=\"wenikCatCircle\">✨</span><span class=\"wenikCatLabel\">ALL</span></button>'+cats.map(c=>'<button class=\"wenikCat '+(normPartner(c)===normPartner(homePartnerCategory)?'active':'')+'\" data-hcat=\"'+esc(c)+'\"><span class=\"wenikCatCircle\">'+partnerIcon(c)+'</span><span class=\"wenikCatLabel\">'+esc(c)+'</span></button>').join('');document.querySelectorAll('[data-hcat]').forEach(b=>b.onclick=()=>{homePartnerCategory=b.dataset.hcat||'';renderHomePartnerCategories();renderHomePartners()})}"
new_render="""/* WENIK HOME CATEGORIES V2 */
const WENIK_HOME_CATEGORIES=['Restaurants','Cafés','Sweets','Fashion','Shoes & Bags','Beauty','Hair Salons','Jewelry','Electronics','Furniture','Fitness','Hotels','Entertainment','Automotive','Education','Services','Swimming Pools'];
function categoryFamilyMatch(actual,wanted){const a=normPartner(actual),w=normPartner(wanted);if(!wanted)return true;if(a===w||a.includes(w)||w.includes(a))return true;const groups={restaurants:/restaurant|food|مطعم|اكل|أكل/,cafes:/cafe|coffee|قهو|كاف/,sweets:/sweet|dessert|حلويات/,fashion:/fashion|cloth|wear|ملابس|البسة|ألبسة/,shoesbags:/shoe|bag|احذية|أحذية|شنط|حقائب/,beauty:/beauty|تجميل/,hair:/hair|salon|barber|صالون|حلاق/,jewelry:/jewel|ذهب|مجوهر/,electronics:/elect|phone|tech|كهرب|هاتف/,furniture:/furniture|اثاث|أثاث/,fitness:/fitness|gym|رياض/,hotels:/hotel|resort|فندق|منتجع/,entertainment:/entertain|kids|play|اطفال|أطفال|ترفيه/,automotive:/auto|car|سيار/,education:/education|school|institute|تعليم|معهد/,services:/service|خدمات/,pools:/pool|swim|مسبح|مسابح/};const key=w.includes('restaurant')?'restaurants':w.includes('cafe')?'cafes':w.includes('sweet')?'sweets':w==='fashion'?'fashion':w.includes('shoe')||w.includes('bag')?'shoesbags':w==='beauty'?'beauty':w.includes('hair')||w.includes('salon')?'hair':w.includes('jewel')?'jewelry':w.includes('elect')?'electronics':w.includes('furniture')?'furniture':w.includes('fitness')?'fitness':w.includes('hotel')?'hotels':w.includes('entertain')?'entertainment':w.includes('auto')?'automotive':w.includes('education')?'education':w.includes('service')?'services':w.includes('pool')?'pools':'';return key?groups[key].test(a):false}
function renderHomePartnerCategories(){if(!$('homePartnerCategories'))return;const cats=WENIK_HOME_CATEGORIES;$('homePartnerCategories').innerHTML='<button class=\"wenikCat '+(homePartnerCategory?'':'active')+'\" data-hcat=\"\"><span class=\"wenikCatCircle\">✨</span><span class=\"wenikCatLabel\">ALL</span></button>'+cats.map(c=>'<button class=\"wenikCat '+(normPartner(c)===normPartner(homePartnerCategory)?'active':'')+'\" data-hcat=\"'+esc(c)+'\"><span class=\"wenikCatCircle\">'+partnerIcon(c)+'</span><span class=\"wenikCatLabel\">'+esc(c)+'</span></button>').join('');document.querySelectorAll('[data-hcat]').forEach(b=>b.onclick=()=>{homePartnerCategory=b.dataset.hcat||'';renderHomePartnerCategories();renderHomePartners()})}"""
if old_render not in h:
    raise SystemExit('Category renderer anchor missing; refusing change')
h=h.replace(old_render,new_render,1)

old_match="function partnerMatches(x,q='',area='',category=''){const text=normPartner([x.business_name,x.category,x.area,x.benefit_title,x.benefit_conditions].filter(Boolean).join(' '));return(!q||text.includes(normPartner(q)))&&(!area||normPartner(x.area)===normPartner(area))&&(!category||normPartner(x.category)===normPartner(category))}"
new_match="function partnerMatches(x,q='',area='',category=''){const text=normPartner([x.business_name,x.category,x.area,x.benefit_title,x.benefit_conditions].filter(Boolean).join(' '));return(!q||text.includes(normPartner(q)))&&(!area||normPartner(x.area)===normPartner(area))&&(!category||categoryFamilyMatch(x.category,category))}"
if old_match not in h:
    raise SystemExit('partnerMatches anchor missing; refusing change')
h=h.replace(old_match,new_match,1)

p.write_text(h,encoding='utf-8')
print('Applied partner-first Home order and 17-category horizontal rail.')
