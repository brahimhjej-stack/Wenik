from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')

start = '/* WENIK PARTNER DISCOVERY V1 — QR/WIN/IZA behavior unchanged */'
end = 'let partnerDirectory=[];'
if start not in html or end not in html:
    raise SystemExit('Partner discovery markers missing; refusing to modify index.html')

new_block = r'''/* WENIK PARTNER DISCOVERY V3 — FIXED AREAS + LIVE LOCATION */
let homePartnerCategory='',homePartnerAreaSaved=localStorage.getItem('wenik_partner_area')||'';
const normPartner=v=>String(v??'').trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9\u0600-\u06ff]+/g,' ');

const WENIK_AREA_GROUPS=[
  ['Beirut',['Beirut','Downtown Beirut','Achrafieh','Hamra','Verdun','Ras Beirut','Badaro','Mar Mikhael','Gemmayzeh','Mazraa','Tariq El Jdideh']],
  ['Mount Lebanon',['Baabda','Hazmieh','Hadath','Choueifat','Aley','Bhamdoun','Broummana','Beit Mery','Mansourieh','Sin El Fil','Furn El Chebbak','Dekwaneh','Jal El Dib','Antelias','Dbayeh','Zouk Mosbeh','Zouk Mikael','Kaslik','Jounieh','Ghazir','Adma']],
  ['South Lebanon',['Saida','Abra','Haret Saida','Ghazieh','Zahrani','Jezzine','Tyre','Abbassieh','Borj El Chemali']],
  ['Nabatieh',['Nabatieh','Kfar Roummane','Habboush','Zefta','Kfar Tebnit','Bint Jbeil','Tebnine','Marjayoun','Hasbaya']],
  ['Bekaa',['Zahle','Chtaura','Jdita','Taalabaya','Rayak','Bar Elias','Qabb Elias','West Bekaa','Baalbek','Hermel']],
  ['North Lebanon',['Tripoli','El Mina','Zgharta','Ehden','Koura','Amioun','Chekka','Batroun','Bsharri','Akkar','Halba']]
];
const WENIK_HOME_CATEGORIES=['Restaurants','Cafés','Sweets','Fashion','Shoes & Bags','Beauty','Hair Salons','Fitness','Perfumes','Optics','Jewelry','Electronics','Furniture','Hotels','Entertainment','Automotive','Education','Services','Swimming Pools'];
const WENIK_AREA_GEO=[
  ['Beirut',33.8938,35.5018],['Achrafieh',33.8886,35.5216],['Hamra',33.8959,35.4822],['Verdun',33.8869,35.4855],
  ['Baabda',33.8339,35.5442],['Hazmieh',33.8515,35.5416],['Aley',33.8104,35.5970],['Broummana',33.8844,35.6334],['Dbayeh',33.9337,35.5870],['Jounieh',33.9808,35.6178],
  ['Saida',33.5571,35.3729],['Jezzine',33.5417,35.5844],['Tyre',33.2705,35.2038],
  ['Nabatieh',33.3772,35.4838],['Bint Jbeil',33.1199,35.4334],['Marjayoun',33.3603,35.5911],['Hasbaya',33.3983,35.6854],
  ['Zahle',33.8463,35.9020],['Chtaura',33.8154,35.8530],['Baalbek',34.0047,36.2110],['Hermel',34.3942,36.3840],
  ['Tripoli',34.4367,35.8497],['Zgharta',34.3970,35.8950],['Batroun',34.2552,35.6581],['Bsharri',34.2508,36.0106],['Halba',34.5428,36.0790]
];

function partnerIcon(v=''){const c=normPartner(v);if(/restaurant|food|مطعم|اكل|أكل/.test(c))return'🍽️';if(/cafe|coffee|قهو|كاف/.test(c))return'☕';if(/sweet|dessert|حلويات/.test(c))return'🍰';if(/shoe|bag|احذية|أحذية|شنط|حقائب/.test(c))return'👟';if(/fashion|cloth|wear|ملابس|البسة|ألبسة/.test(c))return'👕';if(/beauty|تجميل|cosmetic/.test(c))return'💄';if(/hair|salon|barber|صالون|حلاق/.test(c))return'✂️';if(/fitness|gym|رياض/.test(c))return'🏋️';if(/perfume|عطر/.test(c))return'🌸';if(/optic|eyewear|نظارات/.test(c))return'👓';if(/jewel|ذهب|مجوهر/.test(c))return'💎';if(/elect|phone|tech|كهرب|هاتف/.test(c))return'📱';if(/furniture|اثاث|أثاث/.test(c))return'🛋️';if(/hotel|resort|فندق|منتجع/.test(c))return'🏨';if(/pool|swim|مسبح|مسابح/.test(c))return'🏊';if(/entertain|kids|play|اطفال|أطفال|ترفيه/.test(c))return'🎈';if(/auto|car|سيار/.test(c))return'🚗';if(/education|school|institute|تعليم|معهد/.test(c))return'🎓';if(/service|خدمات/.test(c))return'🛠️';return'⭐'}
function partnerDiscount(x){const t=normPartner(x.benefit_type),v=Number(x.benefit_value);if(Number.isFinite(v)&&v>0){if(/percent|percentage|discount|خصم/.test(t))return Math.round(v)+'% OFF';if(/cash|amount|fixed/.test(t))return'$'+(v%1?v.toFixed(2):Math.round(v))+' OFF'}return x.benefit_title?'WENIK OFFER':''}
function wenikPartnerCard(x){const d=partnerDiscount(x),logo=x.logo_url?'<img src="'+esc(x.logo_url)+'" alt="'+esc(x.business_name)+'" loading="lazy">':'<div class="wenikPartnerPlaceholder">WENIK</div>';return'<article class="wenikPartnerCard" tabindex="0" onclick="openWenikPartner(\''+x.partner_id+'\')" onkeydown="if(event.key===\'Enter\'||event.key===\' \'){event.preventDefault();openWenikPartner(\''+x.partner_id+'\')}>'+(d?'<div class="wenikOff">'+esc(d)+'</div>':'')+'<div class="wenikPartnerMedia">'+logo+'</div><div class="wenikPartnerBody"><div class="wenikPartnerName">'+esc(x.business_name)+'</div><div class="wenikPartnerMeta">'+esc([x.category,x.area].filter(Boolean).join(' • '))+'</div><div class="wenikPartnerPromo">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}

function categoryFamilyMatch(actual,wanted){const a=normPartner(actual),w=normPartner(wanted);if(!wanted)return true;if(a===w||a.includes(w)||w.includes(a))return true;const groups={restaurants:/restaurant|food|مطعم|اكل|أكل/,cafes:/cafe|coffee|قهو|كاف/,sweets:/sweet|dessert|حلويات/,fashion:/fashion|cloth|wear|ملابس|البسة|ألبسة/,shoesbags:/shoe|bag|احذية|أحذية|شنط|حقائب/,beauty:/beauty|cosmetic|تجميل/,hair:/hair|salon|barber|صالون|حلاق/,fitness:/fitness|gym|رياض/,perfumes:/perfume|عطر/,optics:/optic|eyewear|نظارات/,jewelry:/jewel|ذهب|مجوهر/,electronics:/elect|phone|tech|كهرب|هاتف/,furniture:/furniture|اثاث|أثاث/,hotels:/hotel|resort|فندق|منتجع/,entertainment:/entertain|kids|play|اطفال|أطفال|ترفيه/,automotive:/auto|car|سيار/,education:/education|school|institute|تعليم|معهد/,services:/service|خدمات/,pools:/pool|swim|مسبح|مسابح/};const key=w.includes('restaurant')?'restaurants':w.includes('cafe')?'cafes':w.includes('sweet')?'sweets':w==='fashion'?'fashion':w.includes('shoe')||w.includes('bag')?'shoesbags':w==='beauty'?'beauty':w.includes('hair')||w.includes('salon')?'hair':w.includes('fitness')?'fitness':w.includes('perfume')?'perfumes':w.includes('optic')?'optics':w.includes('jewel')?'jewelry':w.includes('elect')?'electronics':w.includes('furniture')?'furniture':w.includes('hotel')?'hotels':w.includes('entertain')?'entertainment':w.includes('auto')?'automotive':w.includes('education')?'education':w.includes('service')?'services':w.includes('pool')?'pools':'';return key?groups[key].test(a):false}
function areaFamilyMatch(actual,wanted){if(!wanted)return true;const a=normPartner(actual),w=normPartner(wanted);return a===w||a.includes(w)||w.includes(a)}
function partnerMatches(x,q='',area='',category=''){const text=normPartner([x.business_name,x.category,x.area,x.address,x.benefit_title,x.benefit_conditions].filter(Boolean).join(' '));return(!q||text.includes(normPartner(q)))&&areaFamilyMatch(x.area,area)&&(!category||categoryFamilyMatch(x.category,category))}

function buildAreaOptions(selected=''){let out='<option value="">All Areas</option>';for(const [group,areas] of WENIK_AREA_GROUPS){out+='<optgroup label="'+esc(group)+'">'+areas.map(a=>'<option value="'+esc(a)+'" '+(normPartner(a)===normPartner(selected)?'selected':'')+'>'+esc(a)+'</option>').join('')+'</optgroup>'}return out}
function renderHomePartners(){if(!$('homePartnerGrid'))return;const filtered=(partnerDirectory||[]).filter(x=>partnerMatches(x,'',homePartnerAreaSaved,homePartnerCategory)),list=filtered.slice(0,6),hasFilter=!!(homePartnerAreaSaved||homePartnerCategory);$('homePartnerGrid').innerHTML=list.length?list.map(wenikPartnerCard).join(''):(hasFilter?'<div class="wenikEmpty">No partners found for this selection yet.</div>':'<div class="wenikEmpty">WENIK partners will appear here as they are added.</div>')}
function renderHomePartnerCategories(){if(!$('homePartnerCategories'))return;$('homePartnerCategories').innerHTML='<button class="wenikCat '+(homePartnerCategory?'':'active')+'" data-hcat=""><span class="wenikCatCircle">✨</span><span class="wenikCatLabel">ALL</span></button>'+WENIK_HOME_CATEGORIES.map(c=>'<button class="wenikCat '+(normPartner(c)===normPartner(homePartnerCategory)?'active':'')+'" data-hcat="'+esc(c)+'"><span class="wenikCatCircle">'+partnerIcon(c)+'</span><span class="wenikCatLabel">'+esc(c)+'</span></button>').join('');document.querySelectorAll('[data-hcat]').forEach(b=>b.onclick=()=>{homePartnerCategory=b.dataset.hcat||'';renderHomePartnerCategories();renderHomePartners()})}
function fillHomePartnerAreas(){if(!$('homePartnerArea'))return;$('homePartnerArea').innerHTML=buildAreaOptions(homePartnerAreaSaved);$('homePartnerArea').value=homePartnerAreaSaved||'';$('homePartnerLocationStatus').textContent=homePartnerAreaSaved?'Showing '+homePartnerAreaSaved:'Choose any area or use your location'}
function distKm(a,b,c,d){const R=6371,p=x=>x*Math.PI/180,d1=p(c-a),d2=p(d-b),z=Math.sin(d1/2)**2+Math.cos(p(a))*Math.cos(p(c))*Math.sin(d2/2)**2;return 2*R*Math.asin(Math.sqrt(z))}
function detectPartnerArea(lat,lng){return WENIK_AREA_GEO.map(([area,a,b])=>({area,d:distKm(lat,lng,a,b)})).sort((x,y)=>x.d-y.d)[0]?.area||''}
function useWenikLocation(silent=false){if(!navigator.geolocation){$('homePartnerLocationStatus').textContent='Location is not supported on this device';return}$('homePartnerLocationStatus').textContent='Getting your location…';navigator.geolocation.getCurrentPosition(p=>{const area=detectPartnerArea(p.coords.latitude,p.coords.longitude);if(area){homePartnerAreaSaved=area;localStorage.setItem('wenik_partner_area',area);$('homePartnerArea').value=area;$('homePartnerLocationStatus').textContent='Near you: '+area;renderHomePartners();if($('partnerArea')){$('partnerArea').value=area;renderPartners()}}else $('homePartnerLocationStatus').textContent='Location enabled — choose your area'},()=>{if(!silent)$('homePartnerLocationStatus').textContent='Please allow location access or choose an area'},{enableHighAccuracy:true,timeout:10000,maximumAge:300000})}
async function loadPartnerDiscovery(){await loadPartners();fillHomePartnerAreas();renderHomePartnerCategories();renderHomePartners();$('homePartnerArea').onchange=()=>{homePartnerAreaSaved=$('homePartnerArea').value||'';if(homePartnerAreaSaved)localStorage.setItem('wenik_partner_area',homePartnerAreaSaved);else localStorage.removeItem('wenik_partner_area');$('homePartnerLocationStatus').textContent=homePartnerAreaSaved?'Showing '+homePartnerAreaSaved:'Showing all areas';renderHomePartners()};$('homeUseLocation').onclick=()=>useWenikLocation(false);$('homeViewAllPartners').onclick=()=>{const b=[...document.querySelectorAll('#nav button')].find(x=>x.textContent.trim().startsWith('PARTNERS'));tab('partners',b)}}
window.openWenikPartner=async id=>{const x=(partnerDirectory||[]).find(v=>String(v.partner_id)===String(id));if(!x)return;const a=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]),socials=x.social_links||{},hero=a?.[0]?.image_url||x.logo_url||'',d=partnerDiscount(x),links=[];if(x.phone)links.push('<a href="tel:'+esc(String(x.phone).replace(/[^+\d]/g,''))+'">📞 CALL</a>');if(safeUrl(x.location_url))links.push('<a href="'+esc(x.location_url)+'" target="_blank">📍 LOCATION</a>');if(safeUrl(x.menu_url))links.push('<a href="'+esc(x.menu_url)+'" target="_blank">🍽️ MENU</a>');for(const [k,label] of [['instagram','INSTAGRAM'],['facebook','FACEBOOK'],['website','WEBSITE']])if(safeUrl(socials[k]))links.push('<a href="'+esc(socials[k])+'" target="_blank">'+label+'</a>');$('wenikPartnerDetail').innerHTML='<div class="wenikDetailHero">'+(hero?'<img src="'+esc(hero)+'">':'<div class="wenikPartnerPlaceholder">WENIK</div>')+'</div><div class="wenikDetailName">'+esc(x.business_name)+'</div><div class="wenikDetailMeta">'+esc([x.category,x.area,x.address].filter(Boolean).join(' • '))+'</div>'+((x.benefit_title||d)?'<div class="wenikDetailPromo"><strong>'+esc(d||'WENIK OFFER')+'</strong><div>'+esc(x.benefit_title||'')+'</div>'+(x.benefit_conditions?'<div class="wenikDetailMeta">'+esc(x.benefit_conditions)+'</div>':'')+'</div>':'')+(a?.length?'<div class="wenikDetailGallery">'+a.map(v=>'<img src="'+esc(v.image_url)+'" loading="lazy">').join('')+'</div>':'')+(links.length?'<div class="wenikDetailActions">'+links.join('')+'</div>':'');$('wenikPartnerModal').classList.remove('hidden');document.body.style.overflow='hidden';for(const v of a||[])rpc('track_partner_ad_impression',{p_ad_id:v.id}).catch(()=>{})};
window.closeWenikPartner=()=>{$('wenikPartnerModal').classList.add('hidden');document.body.style.overflow=''};

'''

before, rest = html.split(start,1)
_, after = rest.split(end,1)
html = before + new_block + end + after

# Keep the full Partners tab on the same fixed area/category system.
load_pat = re.compile(r"async function loadPartners\(\)\{.*?\n\}\n\n\$\('partnerSearch'\)", re.S)
replacement = r'''async function loadPartners(){
  partnerDirectory=await rpc('public_partner_directory_v2').catch(()=>[]);
  $('partnerArea').innerHTML=buildAreaOptions($('partnerArea').value||'');
  $('partnerCategory').innerHTML='<option value="">All Categories</option>'+WENIK_HOME_CATEGORIES.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join('');
  renderPartners();
}

$('partnerSearch')'''
html, n = load_pat.subn(replacement, html, count=1)
if n != 1:
    raise SystemExit('Could not safely patch loadPartners(); refusing to write')

# Update the static helper text shown before JS loads.
html = html.replace('Location enabled — choose your area','Location enabled — choose your area')
html = html.replace('Use your location or choose an area','Choose any area or use your location')

path.write_text(html, encoding='utf-8')
print('WENIK Partner Discovery V3 applied successfully.')
