from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')

if '/* WENIK PARTNER DISCOVERY V3 — FIXED AREAS + LIVE LOCATION */' not in html and '/* WENIK PARTNER DISCOVERY V4 — SEARCHABLE MAIN AREAS */' not in html:
    raise SystemExit('WENIK Partner Discovery V3/V4 marker missing; refusing to modify index.html')

html = html.replace('/* WENIK PARTNER DISCOVERY V3 — FIXED AREAS + LIVE LOCATION */', '/* WENIK PARTNER DISCOVERY V4 — SEARCHABLE MAIN AREAS */')

html = re.sub(
    r"const WENIK_AREA_GROUPS=\[.*?\n\];\nconst WENIK_HOME_CATEGORIES=",
    """const WENIK_AREA_GROUPS=[
  ['Beirut',['Beirut']],
  ['Mount Lebanon',['Baabda','Aley','Jounieh']],
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

old_discount = "function partnerDiscount(x){const t=normPartner(x.benefit_type),v=Number(x.benefit_value);if(Number.isFinite(v)&&v>0){if(/percent|percentage|discount|خصم/.test(t))return Math.round(v)+'% OFF';if(/cash|amount|fixed/.test(t))return'$'+(v%1?v.toFixed(2):Math.round(v))+' OFF'}return x.benefit_title?'WENIK OFFER':''}"
new_discount = "function partnerDiscount(x){const t=normPartner(x.benefit_type),v=Number(x.benefit_value),txt=String([x.benefit_title,x.benefit_conditions].filter(Boolean).join(' '));if(Number.isFinite(v)&&v>0){if(/percent|percentage|discount|خصم/.test(t)||v<=100)return Math.round(v)+'% OFF';if(/cash|amount|fixed/.test(t))return'$'+(v%1?v.toFixed(2):Math.round(v))+' OFF'}const m=txt.match(/(\\d{1,2}(?:\\.\\d+)?)\\s*%/);if(m)return Number(m[1])+'% OFF';return x.benefit_title?'WENIK OFFER':''}"
if old_discount in html:
    html = html.replace(old_discount, new_discount, 1)
elif new_discount not in html:
    raise SystemExit('partnerDiscount target not found')

old_fill = "function fillHomePartnerAreas(){if(!$('homePartnerArea'))return;$('homePartnerArea').innerHTML=buildAreaOptions(homePartnerAreaSaved);$('homePartnerArea').value=homePartnerAreaSaved||'';$('homePartnerLocationStatus').textContent=homePartnerAreaSaved?'Showing '+homePartnerAreaSaved:'Choose any area or use your location'}"
new_fill = "function fillHomePartnerAreas(){if(!$('homePartnerArea'))return;const sel=$('homePartnerArea');sel.innerHTML=buildAreaOptions(homePartnerAreaSaved);sel.value=homePartnerAreaSaved||'';let input=$('homePartnerAreaSearch');if(!input){input=document.createElement('input');input.id='homePartnerAreaSearch';input.setAttribute('list','wenikAreaList');input.setAttribute('placeholder','Search area…');input.setAttribute('autocomplete','off');input.style.cssText='width:100%;min-height:46px;border:1px solid rgba(255,255,255,.18);border-radius:14px;padding:0 14px;background:rgba(255,255,255,.08);color:inherit;font:inherit;box-sizing:border-box';const dl=document.createElement('datalist');dl.id='wenikAreaList';dl.innerHTML=WENIK_AREA_GROUPS.flatMap(g=>g[1]).map(a=>'<option value=\\\"'+esc(a)+'\\\"></option>').join('');sel.parentNode.insertBefore(input,sel);sel.parentNode.insertBefore(dl,sel);sel.style.display='none';input.oninput=()=>{const v=input.value.trim(),areas=WENIK_AREA_GROUPS.flatMap(g=>g[1]),match=areas.find(a=>normPartner(a)===normPartner(v));if(match){homePartnerAreaSaved=match;sel.value=match;localStorage.setItem('wenik_partner_area',match);$('homePartnerLocationStatus').textContent='Showing '+match;renderHomePartners()}};input.onchange=input.oninput}input.value=homePartnerAreaSaved||'';$('homePartnerLocationStatus').textContent=homePartnerAreaSaved?'Showing '+homePartnerAreaSaved:'Type the first letter to search an area or use your location'}"
if old_fill in html:
    html = html.replace(old_fill, new_fill, 1)
elif new_fill not in html:
    raise SystemExit('fillHomePartnerAreas target not found')

# Keep the visible home category wording consistently as Restaurants rather than Food.
html = html.replace("['Food','Cafés'", "['Restaurants','Cafés'")
html = html.replace('>Food</span>', '>Restaurants</span>')

# GPS should also update the searchable field when present.
html = html.replace("$('homePartnerArea').value=area;$('homePartnerLocationStatus').textContent='Near you: '+area;", "$('homePartnerArea').value=area;if($('homePartnerAreaSearch'))$('homePartnerAreaSearch').value=area;$('homePartnerLocationStatus').textContent='Near you: '+area;")

path.write_text(html, encoding='utf-8')
print('WENIK Partner Discovery V4 applied successfully.')
