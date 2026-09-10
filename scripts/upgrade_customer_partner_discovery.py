from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')

if '/* WENIK PARTNER DISCOVERY V4 — SEARCHABLE MAIN AREAS */' not in html and '/* WENIK PARTNER DISCOVERY V5 — SEARCHABLE MAIN AREAS AR EN */' not in html:
    raise SystemExit('WENIK Partner Discovery V4/V5 marker missing; refusing to modify index.html')

html = html.replace('/* WENIK PARTNER DISCOVERY V4 — SEARCHABLE MAIN AREAS */', '/* WENIK PARTNER DISCOVERY V5 — SEARCHABLE MAIN AREAS AR EN */')

html = re.sub(
    r"const WENIK_AREA_GROUPS=\[.*?\n\];\nconst WENIK_HOME_CATEGORIES=",
    """const WENIK_AREA_GROUPS=[
  ['Beirut',['Beirut','Dahieh']],
  ['Mount Lebanon',['Baabda','Metn','Jounieh','Jbeil','Aley','Chouf']],
  ['South Lebanon',['Saida','Tyre','Jezzine']],
  ['Nabatieh',['Nabatieh','Bint Jbeil','Marjayoun','Hasbaya']],
  ['Bekaa',['Zahle','Baalbek','Hermel']],
  ['North Lebanon',['Tripoli','Zgharta','Batroun','Bsharri','Akkar']]
];
const WENIK_HOME_CATEGORIES=""",
    html,
    count=1,
    flags=re.S,
)

html = re.sub(
    r"const WENIK_AREA_GEO=\[.*?\n\];",
    """const WENIK_AREA_GEO=[
  ['Beirut',33.8938,35.5018],['Beirut',33.8886,35.5216],['Beirut',33.8959,35.4822],['Dahieh',33.8442,35.5104],
  ['Baabda',33.8339,35.5442],['Baabda',33.8515,35.5416],['Metn',33.8844,35.6334],['Metn',33.9337,35.5870],['Jounieh',33.9808,35.6178],['Jbeil',34.1236,35.6511],['Aley',33.8104,35.5970],['Chouf',33.6977,35.5795],
  ['Saida',33.5571,35.3729],['Saida',33.5470,35.3860],['Tyre',33.2705,35.2038],['Jezzine',33.5417,35.5844],
  ['Nabatieh',33.3772,35.4838],['Nabatieh',33.4050,35.4700],['Bint Jbeil',33.1199,35.4334],['Marjayoun',33.3603,35.5911],['Hasbaya',33.3983,35.6854],
  ['Zahle',33.8463,35.9020],['Zahle',33.8154,35.8530],['Baalbek',34.0047,36.2110],['Hermel',34.3942,36.3840],
  ['Tripoli',34.4367,35.8497],['Tripoli',34.4490,35.8178],['Zgharta',34.3970,35.8950],['Batroun',34.2552,35.6581],['Bsharri',34.2508,36.0106],['Akkar',34.5428,36.0790]
];""",
    html,
    count=1,
    flags=re.S,
)

anchor = "function partnerIcon(v='')"
insert = r"""const WENIK_AREA_ALIASES={
  Beirut:['beirut','بيروت'],Dahieh:['dahieh','dahiyeh','ضاحية','الضاحية'],Baabda:['baabda','بعبدا'],Metn:['metn','maten','المتن','متن'],Jounieh:['jounieh','junieh','جونية'],Jbeil:['jbeil','byblos','جبيل'],Aley:['aley','عاليه'],Chouf:['chouf','shouf','الشوف','شوف'],Saida:['saida','sidon','صيدا'],Tyre:['tyre','sour','صور'],Jezzine:['jezzine','جزين'],Nabatieh:['nabatieh','nabatiyeh','النبطية','نبطية'],BintJbeil:['bint jbeil','bint jbayl','بنت جبيل'],Marjayoun:['marjayoun','marjeyoun','مرجعيون'],Hasbaya:['hasbaya','حاصبيا'],Zahle:['zahle','zahleh','زحلة'],Baalbek:['baalbek','بعلبك'],Hermel:['hermel','الهرمل','هرمل'],Tripoli:['tripoli','طرابلس'],Zgharta:['zgharta','zghorta','زغرتا'],Batroun:['batroun','البترون','بترون'],Bsharri:['bsharri','bcharre','بشري','بشرّي'],Akkar:['akkar','عكار']
};
const WENIK_AREA_FAMILIES={
  Beirut:['Beirut','Downtown Beirut','Achrafieh','Hamra','Verdun','Ras Beirut','Badaro','Mar Mikhael','Gemmayzeh','Mazraa','Tariq El Jdideh'],
  Dahieh:['Dahieh','Dahiyeh','Haret Hreik','Ghobeiry','Chiyah','Bourj El Barajneh','Hadath'],
  Baabda:['Baabda','Hazmieh'],
  Metn:['Metn','Broummana','Beit Mery','Mansourieh','Sin El Fil','Furn El Chebbak','Dekwaneh','Jal El Dib','Antelias','Dbayeh'],
  Jounieh:['Jounieh','Zouk Mosbeh','Zouk Mikael','Kaslik','Ghazir','Adma'],
  Jbeil:['Jbeil','Byblos'],Aley:['Aley','Bhamdoun','Choueifat'],Chouf:['Chouf','Deir El Qamar','Beiteddine','Damour'],
  Saida:['Saida','Sidon','Abra','Haret Saida','Ghazieh','Zahrani'],Tyre:['Tyre','Sour','Abbassieh','Borj El Chemali'],Jezzine:['Jezzine'],
  Nabatieh:['Nabatieh','Kfar Roummane','Habboush','Zefta','Kfar Tebnit'],BintJbeil:['Bint Jbeil','Tebnine'],Marjayoun:['Marjayoun'],Hasbaya:['Hasbaya'],
  Zahle:['Zahle','Chtaura','Jdita','Taalabaya','Rayak','Bar Elias','Qabb Elias','West Bekaa'],Baalbek:['Baalbek'],Hermel:['Hermel'],
  Tripoli:['Tripoli','El Mina'],Zgharta:['Zgharta','Ehden'],Batroun:['Batroun','Chekka'],Bsharri:['Bsharri'],Akkar:['Akkar','Halba']
};
function areaKey(v=''){return String(v).replace(/\s+/g,'')}
function areaAliases(area){const key=areaKey(area);return [area,...(WENIK_AREA_ALIASES[key]||[])].map(normPartner)}
function displayPartnerCategory(v=''){return /^(food|restaurant|restaurants)$/i.test(String(v).trim())?'Restaurants':v}
function ensureWenikPartnerDiscoveryStyles(){if(document.getElementById('wenikPartnerDiscoveryV5Styles'))return;const s=document.createElement('style');s.id='wenikPartnerDiscoveryV5Styles';s.textContent=`
.wenikAreaSearchWrap{position:relative;flex:1;min-width:0}.wenikAreaSearchInput{width:100%;min-height:46px;border:1px solid rgba(255,255,255,.18);border-radius:14px;padding:0 42px 0 14px;background:rgba(255,255,255,.08);color:inherit;font:inherit;box-sizing:border-box}.wenikAreaSearchInput::placeholder{color:rgba(255,255,255,.55)}.wenikAreaSearchChevron{position:absolute;right:14px;top:50%;transform:translateY(-50%);pointer-events:none;opacity:.7}.wenikAreaSearchMenu{position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:50;max-height:260px;overflow:auto;background:#16161d;border:1px solid rgba(255,255,255,.15);border-radius:14px;box-shadow:0 12px 30px rgba(0,0,0,.35);padding:6px}.wenikAreaSearchMenu.hidden{display:none}.wenikAreaOption{display:block;width:100%;border:0;background:transparent;color:#fff;text-align:left;padding:11px 12px;border-radius:10px;font:inherit;cursor:pointer}.wenikAreaOption:hover,.wenikAreaOption:focus{background:rgba(255,255,255,.09);outline:none}.wenikPartnerCard{position:relative;overflow:hidden}.wenikOff{position:absolute!important;top:10px!important;left:10px!important;right:auto!important;z-index:8!important;margin:0!important;max-width:calc(100% - 20px);white-space:nowrap;padding:6px 10px!important;border-radius:999px!important;line-height:1.1!important}
`;document.head.appendChild(s)}
function areaSearchRows(query=''){const q=normPartner(query);const areas=WENIK_AREA_GROUPS.flatMap(g=>g[1]);let rows=areas.map(area=>({area,aliases:areaAliases(area)}));if(q)rows=rows.filter(r=>r.aliases.some(a=>a.startsWith(q)||a.includes(q))).sort((a,b)=>{const ap=a.aliases.some(x=>x.startsWith(q))?0:1,bp=b.aliases.some(x=>x.startsWith(q))?0:1;return ap-bp||a.area.localeCompare(b.area)});return rows}
function mountAreaSearch(selectId,inputId,menuId,onSelect,initial=''){const sel=$(selectId);if(!sel)return;ensureWenikPartnerDiscoveryStyles();sel.style.display='none';let wrap=document.getElementById(inputId+'Wrap'),input=document.getElementById(inputId),menu=document.getElementById(menuId);if(!wrap){wrap=document.createElement('div');wrap.id=inputId+'Wrap';wrap.className='wenikAreaSearchWrap';input=document.createElement('input');input.id=inputId;input.className='wenikAreaSearchInput';input.placeholder='Search area…';input.autocomplete='off';const chev=document.createElement('span');chev.className='wenikAreaSearchChevron';chev.textContent='⌄';menu=document.createElement('div');menu.id=menuId;menu.className='wenikAreaSearchMenu hidden';wrap.append(input,chev,menu);sel.parentNode.insertBefore(wrap,sel)}
const draw=()=>{const rows=areaSearchRows(input.value);menu.innerHTML=(input.value.trim()?'':'<button type="button" class="wenikAreaOption" data-area="">All Areas</button>')+rows.map(r=>'<button type="button" class="wenikAreaOption" data-area="'+esc(r.area)+'">'+esc(r.area)+'</button>').join('');menu.classList.remove('hidden');menu.querySelectorAll('[data-area]').forEach(b=>b.onclick=()=>{const area=b.dataset.area||'';input.value=area;sel.value=area;menu.classList.add('hidden');onSelect(area)})};input.onfocus=draw;input.onclick=draw;input.oninput=draw;input.value=initial||'';document.addEventListener('click',e=>{if(!wrap.contains(e.target))menu.classList.add('hidden')})}

"""
if insert not in html:
    html = html.replace(anchor, insert + anchor, 1)
elif 'WENIK_AREA_ALIASES' not in html:
    raise SystemExit('Could not insert V5 area helpers')

html = re.sub(
    r"function wenikPartnerCard\(x\)\{.*?\}\n\nfunction categoryFamilyMatch",
    "function wenikPartnerCard(x){const d=partnerDiscount(x),cat=displayPartnerCategory(x.category),logo=x.logo_url?'<img src=\"'+esc(x.logo_url)+'\" alt=\"'+esc(x.business_name)+'\" loading=\"lazy\">':'<div class=\"wenikPartnerPlaceholder\">WENIK</div>';return'<article class=\"wenikPartnerCard\" tabindex=\"0\" onclick=\"openWenikPartner(\\''+x.partner_id+'\\')\" onkeydown=\"if(event.key===\\'Enter\\'||event.key===\\' \\'){event.preventDefault();openWenikPartner(\\''+x.partner_id+'\\')}>'+(d?'<div class=\"wenikOff\">'+esc(d)+'</div>':'')+'<div class=\"wenikPartnerMedia\">'+logo+'</div><div class=\"wenikPartnerBody\"><div class=\"wenikPartnerName\">'+esc(x.business_name)+'</div><div class=\"wenikPartnerMeta\">'+esc([cat,x.area].filter(Boolean).join(' • '))+'</div><div class=\"wenikPartnerPromo\">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}\n\nfunction categoryFamilyMatch",
    html,
    count=1,
    flags=re.S,
)

html = re.sub(
    r"function areaFamilyMatch\(actual,wanted\)\{.*?\}\nfunction partnerMatches",
    "function areaFamilyMatch(actual,wanted){if(!wanted)return true;const a=normPartner(actual),w=normPartner(wanted);if(a===w||a.includes(w)||w.includes(a))return true;const fam=WENIK_AREA_FAMILIES[areaKey(wanted)]||[];return fam.some(v=>{const n=normPartner(v);return a===n||a.includes(n)||n.includes(a)})}\nfunction partnerMatches",
    html,
    count=1,
    flags=re.S,
)

html = re.sub(
    r"function fillHomePartnerAreas\(\)\{.*?\}\nfunction distKm",
    "function fillHomePartnerAreas(){if(!$('homePartnerArea'))return;const sel=$('homePartnerArea');sel.innerHTML=buildAreaOptions(homePartnerAreaSaved);sel.value=homePartnerAreaSaved||'';mountAreaSearch('homePartnerArea','homePartnerAreaSearch','homePartnerAreaMenu',area=>{homePartnerAreaSaved=area;if(area)localStorage.setItem('wenik_partner_area',area);else localStorage.removeItem('wenik_partner_area');$('homePartnerLocationStatus').textContent=area?'Showing '+area:'Showing all areas';renderHomePartners()},homePartnerAreaSaved);$('homePartnerLocationStatus').textContent=homePartnerAreaSaved?'Showing '+homePartnerAreaSaved:'Search an area or use your location'}\nfunction distKm",
    html,
    count=1,
    flags=re.S,
)

html = html.replace("if($('homePartnerAreaSearch'))$('homePartnerAreaSearch').value=area;", "if($('homePartnerAreaSearch'))$('homePartnerAreaSearch').value=area;")

old_load = "async function loadPartners(){\n  partnerDirectory=await rpc('public_partner_directory_v2').catch(()=>[]);\n  $('partnerArea').innerHTML=buildAreaOptions($('partnerArea').value||'');\n  $('partnerCategory').innerHTML='<option value=\"\">All Categories</option>'+WENIK_HOME_CATEGORIES.map(x=>'<option value=\"'+esc(x)+'\">'+esc(x)+'</option>').join('');\n  renderPartners();\n}"
new_load = "async function loadPartners(){\n  partnerDirectory=await rpc('public_partner_directory_v2').catch(()=>[]);\n  $('partnerArea').innerHTML=buildAreaOptions($('partnerArea').value||'');\n  $('partnerCategory').innerHTML='<option value=\"\">All Categories</option>'+WENIK_HOME_CATEGORIES.map(x=>'<option value=\"'+esc(x)+'\">'+esc(x)+'</option>').join('');\n  mountAreaSearch('partnerArea','partnerAreaSearch','partnerAreaMenu',area=>{ $('partnerArea').value=area; renderPartners(); },$('partnerArea').value||'');\n  renderPartners();\n}"
if old_load in html:
    html = html.replace(old_load,new_load,1)
elif "mountAreaSearch('partnerArea'" not in html:
    raise SystemExit('Could not patch loadPartners searchable area')

html = html.replace("esc([x.category,x.area,x.address].filter(Boolean).join(' • '))", "esc([displayPartnerCategory(x.category),x.area,x.address].filter(Boolean).join(' • '))")

path.write_text(html, encoding='utf-8')
print('WENIK Partner Discovery V5 applied successfully.')
