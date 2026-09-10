from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')

if 'WENIK PARTNER DISCOVERY V5' not in html:
    raise SystemExit('WENIK Partner Discovery V5 marker missing; refusing to modify index.html')

style = r'''<style id="wenikAreaOverlayV6">
/* WENIK AREA OVERLAY V6 — list floats above the whole page */
.wenikAreaSearchWrap{position:relative!important;z-index:20000!important;overflow:visible!important}
.wenikAreaSearchMenu{position:fixed!important;z-index:2147483000!important;background:#fff!important;color:#17131f!important;border:1px solid #e6e6ec!important;border-radius:16px!important;box-shadow:0 18px 45px rgba(20,12,40,.28)!important;padding:0!important;max-height:min(58vh,430px)!important;overflow-y:auto!important;overflow-x:hidden!important;-webkit-overflow-scrolling:touch!important}
.wenikAreaSearchMenu.hidden{display:none!important}
.wenikAreaOption{display:block!important;width:100%!important;background:#fff!important;color:#17131f!important;text-align:left!important;padding:14px 16px!important;border:0!important;border-bottom:1px solid #ececf2!important;border-radius:0!important;font:inherit!important;font-size:16px!important;font-weight:650!important;line-height:1.25!important;cursor:pointer!important}
.wenikAreaOption:last-child{border-bottom:0!important}
.wenikAreaOption:hover,.wenikAreaOption:focus{background:#f3edff!important;color:#2b125f!important;outline:none!important}
.wenikAreaOption:first-child{background:#f5efff!important;color:#2b125f!important}
</style>'''

if 'id="wenikAreaOverlayV6"' not in html:
    html = html.replace('</head>', style + '\n</head>', 1)

new_mount = r'''function mountAreaSearch(selectId,inputId,menuId,onSelect,initial=''){const sel=$(selectId);if(!sel)return;ensureWenikPartnerDiscoveryStyles();sel.style.display='none';let wrap=document.getElementById(inputId+'Wrap'),input=document.getElementById(inputId),menu=document.getElementById(menuId);if(!wrap){wrap=document.createElement('div');wrap.id=inputId+'Wrap';wrap.className='wenikAreaSearchWrap';input=document.createElement('input');input.id=inputId;input.className='wenikAreaSearchInput';input.placeholder='All Areas';input.autocomplete='off';const chev=document.createElement('span');chev.className='wenikAreaSearchChevron';chev.textContent='⌄';menu=document.createElement('div');menu.id=menuId;menu.className='wenikAreaSearchMenu hidden';wrap.append(input,chev);document.body.appendChild(menu);sel.parentNode.insertBefore(wrap,sel)}
const positionMenu=()=>{const r=input.getBoundingClientRect();const gap=7;const margin=12;const maxW=Math.max(260,Math.min(r.width,window.innerWidth-margin*2));menu.style.left=Math.max(margin,Math.min(r.left,window.innerWidth-maxW-margin))+'px';menu.style.width=maxW+'px';menu.style.right='auto';const below=window.innerHeight-r.bottom-gap;const above=r.top-gap;if(below>=220||below>=above){menu.style.top=(r.bottom+gap)+'px';menu.style.bottom='auto';menu.style.maxHeight=Math.max(180,Math.min(430,below-margin))+'px'}else{menu.style.top='auto';menu.style.bottom=(window.innerHeight-r.top+gap)+'px';menu.style.maxHeight=Math.max(180,Math.min(430,above-margin))+'px'}};
const queryValue=()=>input.value.trim()==='All Areas'?'':input.value;
const draw=()=>{const q=queryValue();const rows=areaSearchRows(q);menu.innerHTML=(q.trim()?'':'<button type="button" class="wenikAreaOption" data-area="">All Areas</button>')+rows.map(r=>'<button type="button" class="wenikAreaOption" data-area="'+esc(r.area)+'">'+esc(r.area)+'</button>').join('');positionMenu();menu.classList.remove('hidden');menu.querySelectorAll('[data-area]').forEach(b=>b.onclick=()=>{const area=b.dataset.area||'';input.value=area||'All Areas';sel.value=area;menu.classList.add('hidden');onSelect(area)})};input.onfocus=()=>{if(input.value==='All Areas')input.select();draw()};input.onclick=draw;input.oninput=draw;input.value=initial||'All Areas';const reposition=()=>{if(!menu.classList.contains('hidden'))positionMenu()};window.addEventListener('resize',reposition,{passive:true});window.addEventListener('scroll',reposition,true);document.addEventListener('click',e=>{if(!wrap.contains(e.target)&&!menu.contains(e.target))menu.classList.add('hidden')})}'''

pattern = r"function mountAreaSearch\(selectId,inputId,menuId,onSelect,initial=''\)\{.*?\}\n\nfunction partnerIcon"
html2, n = re.subn(pattern, new_mount + '\n\nfunction partnerIcon', html, count=1, flags=re.S)
if n != 1:
    raise SystemExit('Could not replace mountAreaSearch for overlay behavior')
html = html2

path.write_text(html, encoding='utf-8')
print('WENIK area overlay V6 applied successfully.')
