from pathlib import Path

p = Path('admin.html')
s = p.read_text(encoding='utf-8')

marker = '<!-- WENIK MISSING PARTNER ACCESS BULK V1 -->'
if marker in s:
    print('Already patched; no changes needed.')
    raise SystemExit(0)

subscription_anchor = '<div class="card"><div class="row"><div><h2>Partner Subscriptions</h2><div class="muted">3 months FREE, then Manual or Whish payment.</div></div><button id="refreshSubscriptions" class="btn secondary" style="width:auto">REFRESH</button></div></div>'
html_block = '''<!-- WENIK MISSING PARTNER ACCESS BULK V1 -->\n  <div class="card" id="missingPartnerAccessCard"><h2>Missing Partner Access</h2><div class="muted">Create Login access for the 9 Partners that were added as directory data only. Existing Partner data stays unchanged.</div><button id="createMissingPartnerAccessBtn" class="btn">CREATE ACCESS FOR 9 PARTNERS</button><div id="missingPartnerAccessStatus" class="status"></div><div id="missingPartnerAccessResults"></div></div>\n  '''
if s.count(subscription_anchor) != 1:
    raise SystemExit(f'Expected exactly one Partner Subscriptions anchor, found {s.count(subscription_anchor)}')
s = s.replace(subscription_anchor, html_block + subscription_anchor, 1)

js_anchor = "$('logoutBtn').onclick=async()=>{await sb.auth.signOut();location.reload()};tabs();start();"
js_block = r'''// WENIK MISSING PARTNER ACCESS BULK V1
const WENIK_MISSING_PARTNERS=[
  {id:'3887feb9-e923-404b-9eb5-db6ad9982df6',name:'Farouj Chahine',username:'faroujchahine'},
  {id:'0bc2dc1d-db00-423e-af85-c101d359cdcb',name:'Kashmir Wears',username:'kashmirwears'},
  {id:'6cf8a835-f88e-498c-ac7e-dc502e149013',name:"L'Atelier de Vera",username:'atelierdevera'},
  {id:'c9db34bf-9369-4b8f-8275-dfdaf94b2822',name:'Labneh w Jebneh',username:'labnehwjebneh'},
  {id:'a7ac3e4f-d565-4b1c-85f7-a8f33ad92a44',name:'Ghazi Issa Electrical',username:'ghaziissaelectrical'},
  {id:'017bb4e2-0378-426e-813d-7bd3edf351a1',name:'Jaber Jewelry',username:'jaberjewelry'},
  {id:'87def644-2dff-4e07-9839-64accaee68dd',name:'Lilandi Coffee',username:'lilandicoffee'},
  {id:'6514c793-e80d-44d4-a15e-01ea7438268e',name:'Eat Vite',username:'eatvite'},
  {id:'12ab422f-f1e1-4e0f-b416-9eb57f9fad1c',name:'Salon Mohammad Sabah',username:'salonmohammadsabah'}
];
function wenikTempPassword(){
  const u='ABCDEFGHJKLMNPQRSTUVWXYZ',l='abcdefghijkmnopqrstuvwxyz',d='23456789',x='@#%!?',a=u+l+d+x;
  const pick=s=>s[Math.floor(Math.random()*s.length)];
  let out=pick(u)+pick(l)+pick(d)+pick(x);
  while(out.length<14)out+=pick(a);
  return out.split('').sort(()=>Math.random()-.5).join('');
}
$('createMissingPartnerAccessBtn').onclick=async()=>{
  if(!confirm('Create Partner Login access for the 9 missing accounts? Existing Partner profiles will not be changed.'))return;
  const btn=$('createMissingPartnerAccessBtn'),status=$('missingPartnerAccessStatus'),box=$('missingPartnerAccessResults');
  btn.disabled=true;status.textContent='Creating Partner access…';box.innerHTML='';
  const rows=[];
  for(const p of WENIK_MISSING_PARTNERS){
    const password=wenikTempPassword();
    try{
      const {data,error}=await sb.functions.invoke('admin-create-partner-user',{body:{partner_id:p.id,username:p.username,password,display_name:p.name,role:'partner_manager'}});
      if(error)throw error;if(data?.error)throw Error(data.error);
      rows.push({name:p.name,username:p.username,password,ok:true});
    }catch(e){
      rows.push({name:p.name,username:p.username,password:'',ok:false,error:e?.message||'Could not create access'});
    }
    box.innerHTML=rows.map(r=>'<div class="card" style="padding:14px"><b>'+esc(r.name)+'</b><div class="muted">Username: '+esc(r.username)+'</div>'+(r.ok?'<div class="good">Temporary password: <b>'+esc(r.password)+'</b></div>':'<div class="error">'+esc(r.error)+'</div>')+'</div>').join('');
  }
  const ok=rows.filter(r=>r.ok).length;
  status.textContent=ok+' of '+rows.length+' Partner access accounts created. Save the temporary passwords now; Partners must change them after login.';
  btn.disabled=false;
};
'''
if s.count(js_anchor) != 1:
    raise SystemExit(f'Expected exactly one logout/start JS anchor, found {s.count(js_anchor)}')
s = s.replace(js_anchor, js_block + js_anchor, 1)

if s.count(marker) != 2:
    raise SystemExit(f'Expected 2 feature markers after patch, found {s.count(marker)}')
p.write_text(s, encoding='utf-8')
print('Patched admin.html with Missing Partner Access only.')
