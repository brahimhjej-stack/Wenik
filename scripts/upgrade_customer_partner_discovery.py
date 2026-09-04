from pathlib import Path

path=Path('index.html')
html=path.read_text(encoding='utf-8')
marker='/* WENIK PARTNER DISCOVERY V1 */'
if marker in html:
    print('WENIK partner discovery already applied; no change needed.')
    raise SystemExit(0)

required=['id="carousel"','id="campaigns"','id="partners"','id="partnerSearch"','id="partnerArea"','id="partnerCategory"','id="partnerList"','let partnerDirectory=[];','function renderPartners(){','async function loadPartners(){','await Promise.all([loadHome(),loadIza(),refreshUnread()])']
for token in required:
    if token not in html:
        raise SystemExit(f'Required marker missing: {token}; refusing to modify index.html')

css=r'''
/* WENIK PARTNER DISCOVERY V1 */
.wenikDiscovery{padding:14px 12px 16px;overflow:hidden}
.wenikDiscoveryHead{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px}
.wenikDiscoveryTitle{font-size:19px;font-weight:950}.wenikDiscoverySub{font-size:12px;color:#bdb4cb;margin-top:3px}
.wenikLocationRow{display:flex;gap:8px;align-items:center;margin:10px 0 12px}.wenikLocationRow .field{margin:0;flex:1;min-width:0}.wenikLocationRow .btn{width:auto;margin:0;white-space:nowrap;padding:11px 10px;font-size:11px}
.wenikCategories{display:flex;gap:10px;overflow-x:auto;padding:2px 1px 10px;scroll-snap-type:x proximity}.wenikCategories::-webkit-scrollbar{display:none}
.wenikCat{min-width:74px;max-width:74px;border:0;background:transparent;color:#fff;padding:0;display:flex;flex-direction:column;align-items:center;gap:6px;scroll-snap-align:start}.wenikCatCircle{width:64px;height:64px;border-radius:50%;display:grid;place-items:center;font-size:25px;background:linear-gradient(145deg,rgba(143,36,255,.30),rgba(239,21,157,.20),rgba(255,111,33,.18));border:1px solid rgba(255,255,255,.12);box-shadow:0 8px 22px rgba(0,0,0,.26)}.wenikCat.active .wenikCatCircle{outline:2px solid #ffd21c;box-shadow:0 0 0 4px rgba(255,210,28,.10),0 10px 28px rgba(143,36,255,.25)}.wenikCatLabel{font-size:10.5px;line-height:1.15;color:#d9d3e3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:74px;text-align:center}
.wenikPartnerGrid{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:11px!important;margin-top:8px}.wenikPartnerCard{position:relative;overflow:hidden;border-radius:17px;background:linear-gradient(145deg,rgba(24,18,39,.98),rgba(10,9,18,.98));border:1px solid rgba(178,92,255,.22);box-shadow:0 12px 32px rgba(0,0,0,.30);cursor:pointer;min-width:0}.wenikPartnerMedia{aspect-ratio:1.05/1;width:100%;background:linear-gradient(135deg,rgba(143,36,255,.28),rgba(239,21,157,.20),rgba(255,111,33,.20));display:grid;place-items:center;overflow:hidden}.wenikPartnerMedia img{width:100%;height:100%;object-fit:cover;display:block}.wenikPartnerPlaceholder{font-weight:950;font-size:20px;color:#fff;text-align:center;padding:10px}.wenikOff{position:absolute;top:8px;right:8px;z-index:2;padding:6px 8px;border-radius:10px;background:linear-gradient(100deg,#ef159d,#ff6f21,#ffd21c);color:#fff;font-weight:950;font-size:11px;box-shadow:0 8px 20px rgba(0,0,0,.28)}.wenikPartnerBody{padding:10px 10px 12px}.wenikPartnerName{font-size:14px;font-weight:950;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.wenikPartnerMeta{font-size:11px;color:#bcb5c8;margin-top:5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.wenikPartnerPromo{font-size:11px;color:#ffd67a;font-weight:800;margin-top:7px;min-height:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.wenikEmpty{grid-column:1/-1;padding:24px 10px;text-align:center;color:#bcb5c8;border:1px dashed rgba(178,92,255,.25);border-radius:14px}
.wenikPartnerModal{position:fixed;inset:0;z-index:9999;background:rgba(3,2,7,.82);backdrop-filter:blur(8px);display:flex;align-items:flex-end;justify-content:center}.wenikPartnerModal.hidden{display:none!important}.wenikPartnerSheet{width:min(720px,100%);max-height:91vh;overflow:auto;border-radius:24px 24px 0 0;background:linear-gradient(180deg,#171020,#090711);border:1px solid rgba(178,92,255,.28);box-shadow:0 -20px 70px rgba(0,0,0,.60);padding:14px 14px 28px}.wenikModalClose{position:sticky;top:0;margin-left:auto;z-index:5;width:40px;height:40px;border-radius:50%;border:1px solid rgba(255,255,255,.15);background:rgba(9,7,17,.90);color:#fff;font-size:22px;display:grid;place-items:center}.wenikDetailHero{border-radius:18px;overflow:hidden;aspect-ratio:16/9;background:linear-gradient(135deg,rgba(143,36,255,.32),rgba(239,21,157,.22),rgba(255,111,33,.20));display:grid;place-items:center;margin-top:-30px}.wenikDetailHero img{width:100%;height:100%;object-fit:cover}.wenikDetailName{font-size:24px;font-weight:950;margin-top:14px}.wenikDetailMeta{color:#bdb5c9;font-size:13px;margin-top:4px}.wenikDetailPromo{margin-top:12px;border-radius:15px;padding:12px;background:linear-gradient(120deg,rgba(143,36,255,.28),rgba(239,21,157,.20),rgba(255,111,33,.16));border:1px solid rgba(255,210,28,.22)}.wenikDetailPromo strong{display:block;color:#ffd66e;font-size:18px;margin-bottom:3px}.wenikDetailActions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:13px}.wenikDetailActions a{display:block;text-align:center;text-decoration:none;padding:11px 8px;border-radius:12px;background:rgba(143,36,255,.18);border:1px solid rgba(178,92,255,.26);color:#fff;font-weight:850;font-size:12px}.wenikDetailGallery{display:flex;gap:9px;overflow-x:auto;margin-top:12px}.wenikDetailGallery img{width:78%;aspect-ratio:16/10;object-fit:cover;border-radius:14px;border:1px solid rgba(255,255,255,.10)}
@media(max-width:390px){.wenikPartnerGrid{gap:9px!important}.wenikPartnerName{font-size:13px}.wenikCat{min-width:69px;max-width:69px}.wenikCatCircle{width:59px;height:59px}.wenikCatLabel{width:69px}}
'''
idx=html.find('</style>')
if idx<0: raise SystemExit('No </style>; refusing to modify')
html=html[:idx]+'\n'+css+'\n'+html[idx:]

home_block=r'''
      <div class="sectionTitle"><h3>PARTNERS</h3><span class="muted">Near you</span></div>
      <div class="card wenikDiscovery" id="homePartnerDiscovery">
        <div class="wenikDiscoveryHead"><div><div class="wenikDiscoveryTitle">DISCOVER WENIK PARTNERS</div><div id="homePartnerLocationStatus" class="wenikDiscoverySub">Use your location or choose an area</div></div></div>
        <div class="wenikLocationRow"><select id="homePartnerArea" class="field"><option value="">All Areas</option></select><button id="homeUseLocation" class="btn secondary" type="button">📍 LOCATION</button></div>
        <div id="homePartnerCategories" class="wenikCategories"></div>
        <div id="homePartnerGrid" class="wenikPartnerGrid"><div class="wenikEmpty">Loading partners…</div></div>
        <button id="homeViewAllPartners" class="btn secondary" type="button" style="margin-top:12px">VIEW ALL PARTNERS</button>
      </div>
'''
anchor='      <div class="sectionTitle"><h3>WIN</h3></div><div id="campaigns"></div>'
if anchor not in html: raise SystemExit('WIN home anchor missing; refusing to modify')
html=html.replace(anchor,home_block+anchor,1)
html=html.replace('<div id="partnerList"></div>','<div id="partnerList" class="wenikPartnerGrid"></div>',1)

modal=r'''
<div id="wenikPartnerModal" class="wenikPartnerModal hidden" role="dialog" aria-modal="true" aria-label="Partner details"><div class="wenikPartnerSheet"><button id="wenikPartnerClose" class="wenikModalClose" type="button">×</button><div id="wenikPartnerDetail"></div></div></div>
'''
nav_anchor='<nav id="nav" class="nav hidden">'
if nav_anchor not in html: raise SystemExit('Nav anchor missing; refusing to modify')
html=html.replace(nav_anchor,modal+'\n'+nav_anchor,1)

helpers=r'''
/* WENIK PARTNER DISCOVERY V1 — QR/WIN/IZA behavior unchanged */
let homePartnerCategory='',homePartnerAreaSaved=localStorage.getItem('wenik_partner_area')||'';
const normPartner=v=>String(v??'').trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9\u0600-\u06ff]+/g,' ');
function partnerIcon(v=''){const c=normPartner(v);if(/restaurant|food|مطعم|اكل|أكل/.test(c))return'🍽️';if(/cafe|coffee|قهو|كاف/.test(c))return'☕';if(/fashion|cloth|wear|ملابس|البسة|ألبسة/.test(c))return'👕';if(/beauty|salon|spa|صالون|تجميل/.test(c))return'✨';if(/jewel|ذهب|مجوهر/.test(c))return'💎';if(/elect|phone|tech|كهرب|هاتف/.test(c))return'📱';if(/hotel|resort|فندق|منتجع/.test(c))return'🏨';if(/kids|play|entertain|اطفال|أطفال|ترفيه/.test(c))return'🎈';if(/service|خدمات/.test(c))return'🛠️';return'⭐'}
function partnerDiscount(x){const t=normPartner(x.benefit_type),v=Number(x.benefit_value);if(Number.isFinite(v)&&v>0){if(/percent|percentage|discount|خصم/.test(t))return Math.round(v)+'% OFF';if(/cash|amount|fixed/.test(t))return'$'+(v%1?v.toFixed(2):Math.round(v))+' OFF'}return x.benefit_title?'WENIK OFFER':''}
function wenikPartnerCard(x){const d=partnerDiscount(x),logo=x.logo_url?'<img src="'+esc(x.logo_url)+'" alt="'+esc(x.business_name)+'" loading="lazy">':'<div class="wenikPartnerPlaceholder">WENIK</div>';return'<article class="wenikPartnerCard" tabindex="0" onclick="openWenikPartner(\''+x.partner_id+'\')" onkeydown="if(event.key===\'Enter\'||event.key===\' \'){event.preventDefault();openWenikPartner(\''+x.partner_id+'\')}>'+(d?'<div class="wenikOff">'+esc(d)+'</div>':'')+'<div class="wenikPartnerMedia">'+logo+'</div><div class="wenikPartnerBody"><div class="wenikPartnerName">'+esc(x.business_name)+'</div><div class="wenikPartnerMeta">'+esc([x.category,x.area].filter(Boolean).join(' • '))+'</div><div class="wenikPartnerPromo">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}
function partnerMatches(x,q='',area='',category=''){const text=normPartner([x.business_name,x.category,x.area,x.benefit_title,x.benefit_conditions].filter(Boolean).join(' '));return(!q||text.includes(normPartner(q)))&&(!area||normPartner(x.area)===normPartner(area))&&(!category||normPartner(x.category)===normPartner(category))}
function renderHomePartners(){if(!$('homePartnerGrid'))return;const list=(partnerDirectory||[]).filter(x=>partnerMatches(x,'',homePartnerAreaSaved,homePartnerCategory)).slice(0,6);$('homePartnerGrid').innerHTML=list.length?list.map(wenikPartnerCard).join(''):'<div class="wenikEmpty">No partners found in this area yet.</div>'}
function renderHomePartnerCategories(){if(!$('homePartnerCategories'))return;const cats=[...new Set((partnerDirectory||[]).map(x=>x.category).filter(Boolean))].sort((a,b)=>String(a).localeCompare(String(b)));$('homePartnerCategories').innerHTML='<button class="wenikCat '+(homePartnerCategory?'':'active')+'" data-hcat=""><span class="wenikCatCircle">✨</span><span class="wenikCatLabel">ALL</span></button>'+cats.map(c=>'<button class="wenikCat '+(normPartner(c)===normPartner(homePartnerCategory)?'active':'')+'" data-hcat="'+esc(c)+'"><span class="wenikCatCircle">'+partnerIcon(c)+'</span><span class="wenikCatLabel">'+esc(c)+'</span></button>').join('');document.querySelectorAll('[data-hcat]').forEach(b=>b.onclick=()=>{homePartnerCategory=b.dataset.hcat||'';renderHomePartnerCategories();renderHomePartners()})}
function fillHomePartnerAreas(){const areas=[...new Set((partnerDirectory||[]).map(x=>x.area).filter(Boolean))].sort((a,b)=>String(a).localeCompare(String(b)));$('homePartnerArea').innerHTML='<option value="">All Areas</option>'+areas.map(a=>'<option value="'+esc(a)+'">'+esc(a)+'</option>').join('');const saved=areas.find(a=>normPartner(a)===normPartner(homePartnerAreaSaved));if(saved){homePartnerAreaSaved=saved;$('homePartnerArea').value=saved;$('homePartnerLocationStatus').textContent='Showing '+saved}else homePartnerAreaSaved=''}
const WENIK_CITIES=[{a:['nabatieh','nabatiyeh','النبطية'],lat:33.3772,lng:35.4838},{a:['sour','tyre','صور'],lat:33.2705,lng:35.2038},{a:['saida','sidon','صيدا'],lat:33.5571,lng:35.3729},{a:['beirut','بيروت'],lat:33.8938,lng:35.5018},{a:['baalbek','بعلبك'],lat:34.0047,lng:36.2110},{a:['zahle','زحلة'],lat:33.8463,lng:35.9020},{a:['tripoli','طرابلس'],lat:34.4367,lng:35.8497},{a:['jounieh','جونية'],lat:33.9808,lng:35.6178},{a:['aley','عاليه'],lat:33.8104,lng:35.5970}];
function distKm(a,b,c,d){const R=6371,p=(x=>x*Math.PI/180),d1=p(c-a),d2=p(d-b),z=Math.sin(d1/2)**2+Math.cos(p(a))*Math.cos(p(c))*Math.sin(d2/2)**2;return 2*R*Math.asin(Math.sqrt(z))}
function detectPartnerArea(lat,lng){const areas=[...new Set((partnerDirectory||[]).map(x=>x.area).filter(Boolean))],m=WENIK_CITIES.map(c=>{const area=areas.find(v=>c.a.some(a=>normPartner(v).includes(normPartner(a))||normPartner(a).includes(normPartner(v))));return area?{area,d:distKm(lat,lng,c.lat,c.lng)}:null}).filter(Boolean).sort((a,b)=>a.d-b.d);return m[0]&&m[0].d<=35?m[0].area:''}
function useWenikLocation(silent=false){if(!navigator.geolocation){$('homePartnerLocationStatus').textContent='Choose your area';return}$('homePartnerLocationStatus').textContent='Getting your location…';navigator.geolocation.getCurrentPosition(p=>{const area=detectPartnerArea(p.coords.latitude,p.coords.longitude);if(area){homePartnerAreaSaved=area;localStorage.setItem('wenik_partner_area',area);$('homePartnerArea').value=area;$('homePartnerLocationStatus').textContent='Near you: '+area;renderHomePartners()}else $('homePartnerLocationStatus').textContent='Location enabled — choose your area'},()=>{if(!silent)$('homePartnerLocationStatus').textContent='Location unavailable — choose your area'},{timeout:7000,maximumAge:600000})}
async function loadPartnerDiscovery(){await loadPartners();fillHomePartnerAreas();renderHomePartnerCategories();renderHomePartners();$('homePartnerArea').onchange=()=>{homePartnerAreaSaved=$('homePartnerArea').value||'';if(homePartnerAreaSaved)localStorage.setItem('wenik_partner_area',homePartnerAreaSaved);else localStorage.removeItem('wenik_partner_area');$('homePartnerLocationStatus').textContent=homePartnerAreaSaved?'Showing '+homePartnerAreaSaved:'Showing all areas';renderHomePartners()};$('homeUseLocation').onclick=()=>useWenikLocation(false);$('homeViewAllPartners').onclick=()=>{const b=[...document.querySelectorAll('#nav button')].find(x=>x.textContent.trim().startsWith('PARTNERS'));tab('partners',b)};if(!homePartnerAreaSaved)setTimeout(()=>useWenikLocation(true),700)}
window.openWenikPartner=async id=>{const x=(partnerDirectory||[]).find(v=>String(v.partner_id)===String(id));if(!x)return;const a=await rpc('public_partner_ads',{p_partner_id:id}).catch(()=>[]),socials=x.social_links||{},hero=a?.[0]?.image_url||x.logo_url||'',d=partnerDiscount(x),links=[];if(x.phone)links.push('<a href="tel:'+esc(String(x.phone).replace(/[^+\d]/g,''))+'">📞 CALL</a>');if(safeUrl(x.location_url))links.push('<a href="'+esc(x.location_url)+'" target="_blank">📍 LOCATION</a>');if(safeUrl(x.menu_url))links.push('<a href="'+esc(x.menu_url)+'" target="_blank">🍽️ MENU</a>');for(const [k,label] of [['instagram','INSTAGRAM'],['facebook','FACEBOOK'],['website','WEBSITE']])if(safeUrl(socials[k]))links.push('<a href="'+esc(socials[k])+'" target="_blank">'+label+'</a>');$('wenikPartnerDetail').innerHTML='<div class="wenikDetailHero">'+(hero?'<img src="'+esc(hero)+'">':'<div class="wenikPartnerPlaceholder">WENIK</div>')+'</div><div class="wenikDetailName">'+esc(x.business_name)+'</div><div class="wenikDetailMeta">'+esc([x.category,x.area,x.address].filter(Boolean).join(' • '))+'</div>'+((x.benefit_title||d)?'<div class="wenikDetailPromo"><strong>'+esc(d||'WENIK OFFER')+'</strong><div>'+esc(x.benefit_title||'')+'</div>'+(x.benefit_conditions?'<div class="wenikDetailMeta">'+esc(x.benefit_conditions)+'</div>':'')+'</div>':'')+(a?.length?'<div class="wenikDetailGallery">'+a.map(v=>'<img src="'+esc(v.image_url)+'" loading="lazy">').join('')+'</div>':'')+(links.length?'<div class="wenikDetailActions">'+links.join('')+'</div>':'');$('wenikPartnerModal').classList.remove('hidden');document.body.style.overflow='hidden';for(const v of a||[])rpc('track_partner_ad_impression',{p_ad_id:v.id}).catch(()=>{})};
window.closeWenikPartner=()=>{$('wenikPartnerModal').classList.add('hidden');document.body.style.overflow=''};
'''
partner_anchor='let partnerDirectory=[];'
html=html.replace(partner_anchor,helpers+'\n'+partner_anchor,1)

start=html.find('function renderPartners(){')
end=html.find('\nasync function loadPartners(){',start)
if start<0 or end<0: raise SystemExit('Could not isolate renderPartners; refusing to modify')
new_render=r'''function renderPartners(){
  const q=($('partnerSearch').value||'').trim(),area=$('partnerArea').value,category=$('partnerCategory').value;
  const list=(partnerDirectory||[]).filter(x=>partnerMatches(x,q,area,category));
  $('partnerList').classList.add('wenikPartnerGrid');
  $('partnerList').innerHTML=list.length?list.map(wenikPartnerCard).join(''):'<div class="wenikEmpty">No partners match your search.</div>'
}
'''
html=html[:start]+new_render+html[end:]

html=html.replace('await Promise.all([loadHome(),loadIza(),refreshUnread()])','await Promise.all([loadHome(),loadIza(),refreshUnread(),loadPartnerDiscovery()])',1)

close_anchor='</script>\n</body>'
extra=r'''
$('wenikPartnerClose').onclick=closeWenikPartner;
$('wenikPartnerModal').onclick=e=>{if(e.target===$('wenikPartnerModal'))closeWenikPartner()};
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('wenikPartnerModal').classList.contains('hidden'))closeWenikPartner()});
'''
if close_anchor not in html: raise SystemExit('Script close anchor missing; refusing to modify')
html=html.replace(close_anchor,extra+'\n</script>\n</body>',1)

path.write_text(html,encoding='utf-8')
print('Applied WENIK Customer Home + Partner discovery upgrade')
