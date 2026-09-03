from pathlib import Path

path = Path('admin.html')
text = path.read_text(encoding='utf-8')

MARK = 'WENIK ADMIN PRODUCTION TOOLS'
if MARK in text:
    print('Admin production tools already applied; no changes.')
    raise SystemExit(0)

# Guard exact current structure before changing anything.
tab_old = '<button class="tab" data-panel="wins">WIN</button><button id="superTab" class="tab hidden" data-panel="super">SUPER ADMIN</button>'
assert text.count(tab_old) == 1, 'Expected WIN/SUPER ADMIN tab anchor not found exactly once.'

tab_new = '<button class="tab" data-panel="wins">WIN</button><button class="tab" data-panel="dashboard">DASHBOARD</button><button class="tab" data-panel="subscriptions">SUBSCRIPTIONS</button><button id="superTab" class="tab hidden" data-panel="super">SUPER ADMIN</button>'
text = text.replace(tab_old, tab_new, 1)

panel_anchor = '<section id="super" class="panel">'
assert text.count(panel_anchor) == 1, 'Super Admin panel anchor not found exactly once.'

panels = r'''
<!-- WENIK ADMIN PRODUCTION TOOLS -->
<section id="dashboard" class="panel">
  <div class="card">
    <div class="row"><div><h2>Home Dashboard</h2><div class="muted">Control customer home banners without touching the website code.</div></div><button id="refreshHomeAds" class="btn secondary" style="width:auto">REFRESH</button></div>
  </div>
  <div class="card">
    <h3>Add / Edit Banner</h3>
    <input id="homeAdId" type="hidden">
    <input id="homeAdImage" class="field" placeholder="Image URL · required">
    <input id="homeAdTitle" class="field" placeholder="Title (optional)">
    <div class="two"><select id="homeAdCtaType" class="field"><option value="partner_page">Partner page</option><option value="url">URL</option><option value="none">No action</option></select><input id="homeAdCtaUrl" class="field" placeholder="CTA URL or /path"></div>
    <div class="two"><input id="homeAdSort" class="field" type="number" value="100" placeholder="Sort order"><input id="homeAdPriority" class="field" type="number" value="0" placeholder="Priority"></div>
    <div class="two"><input id="homeAdStart" class="field" type="datetime-local"><input id="homeAdEnd" class="field" type="datetime-local"></div>
    <select id="homeAdActive" class="field"><option value="false">Inactive</option><option value="true">Active</option></select>
    <div class="actions"><button id="saveHomeAd" class="btn">SAVE BANNER</button><button id="clearHomeAd" class="btn secondary">CLEAR</button></div>
    <div id="homeAdStatus" class="status"></div>
  </div>
  <div id="homeAdsList"></div>
</section>

<section id="subscriptions" class="panel">
  <div class="card"><div class="row"><div><h2>Partner Subscriptions</h2><div class="muted">3 months FREE, then Manual or Whish payment.</div></div><button id="refreshSubscriptions" class="btn secondary" style="width:auto">REFRESH</button></div></div>
  <div id="subscriptionList"></div>
</section>

'''
text = text.replace(panel_anchor, panels + panel_anchor, 1)

# Add panel loaders to the existing tab router only.
tab_router_old = "if(b.dataset.panel==='wins')loadWins();if(b.dataset.panel==='super')loadAdmins()"
assert text.count(tab_router_old) == 1, 'Tab router anchor not found exactly once.'
tab_router_new = "if(b.dataset.panel==='wins')loadWins();if(b.dataset.panel==='dashboard')loadHomeAds();if(b.dataset.panel==='subscriptions')loadSubscriptions();if(b.dataset.panel==='super')loadAdmins()"
text = text.replace(tab_router_old, tab_router_new, 1)

js_anchor = "$('logoutBtn').onclick=async()=>{await sb.auth.signOut();location.reload()};tabs();start();"
assert text.count(js_anchor) == 1, 'Logout/start anchor not found exactly once.'

js = r'''
/* WENIK ADMIN PRODUCTION TOOLS */
function localInput(v){if(!v)return'';const d=new Date(v),z=new Date(d.getTime()-d.getTimezoneOffset()*60000);return z.toISOString().slice(0,16)}
function isoOrNull(id){const v=$(id).value;return v?new Date(v).toISOString():null}
function clearHomeAdForm(){for(const id of ['homeAdId','homeAdImage','homeAdTitle','homeAdCtaUrl','homeAdStart','homeAdEnd'])$(id).value='';$('homeAdCtaType').value='partner_page';$('homeAdSort').value='100';$('homeAdPriority').value='0';$('homeAdActive').value='false';$('homeAdStatus').textContent=''}
async function loadHomeAds(){try{const list=await rpc('admin_home_ads_list');$('homeAdsList').innerHTML=(list||[]).map(a=>'<div class="card"><div class="row"><div><b>'+esc(a.title||'Home banner')+'</b><div class="muted">Order '+a.sort_order+' · Priority '+a.priority+' · '+(a.is_active?'Active':'Inactive')+'</div></div><span class="pill">'+Number(a.impressions||0)+' views · '+Number(a.clicks||0)+' clicks</span></div>'+(a.image_url?'<img class="itemImg" src="'+esc(a.image_url)+'" alt="">':'')+'<div class="muted">'+esc(a.cta_type||'')+(a.cta_url?' · '+esc(a.cta_url):'')+'</div><div class="actions"><button class="btn secondary" onclick="editHomeAd(\''+a.id+'\')">EDIT</button><button class="btn danger" onclick="deleteHomeAd(\''+a.id+'\')">DELETE</button></div></div>').join('')||'<div class="card muted">No dashboard banners.</div>';window._homeAds=list||[]}catch(e){$('homeAdsList').innerHTML='<div class="card error">'+esc(e.message)+'</div>'}}
window.editHomeAd=id=>{const a=(window._homeAds||[]).find(x=>x.id===id);if(!a)return;$('homeAdId').value=a.id;$('homeAdImage').value=a.image_url||'';$('homeAdTitle').value=a.title||'';$('homeAdCtaType').value=a.cta_type||'partner_page';$('homeAdCtaUrl').value=a.cta_url||'';$('homeAdSort').value=a.sort_order??100;$('homeAdPriority').value=a.priority??0;$('homeAdStart').value=localInput(a.starts_at);$('homeAdEnd').value=localInput(a.ends_at);$('homeAdActive').value=String(!!a.is_active);window.scrollTo({top:0,behavior:'smooth'})};
window.deleteHomeAd=async id=>{if(!confirm('Delete this dashboard banner?'))return;try{await rpc('admin_delete_home_ad',{p_id:id});await loadHomeAds()}catch(e){alert(e.message)}};
$('saveHomeAd').onclick=async()=>{try{const image=$('homeAdImage').value.trim();if(!image)throw Error('Image URL is required.');await rpc('admin_upsert_home_ad',{p_id:$('homeAdId').value||null,p_image_url:image,p_title:$('homeAdTitle').value.trim()||null,p_cta_type:$('homeAdCtaType').value,p_cta_url:$('homeAdCtaUrl').value.trim()||null,p_sort_order:Number($('homeAdSort').value||100),p_priority:Number($('homeAdPriority').value||0),p_starts_at:isoOrNull('homeAdStart'),p_ends_at:isoOrNull('homeAdEnd'),p_is_active:$('homeAdActive').value==='true',p_partner_id:null,p_partner_ad_id:null});setStatus('homeAdStatus','Dashboard banner saved.',true);clearHomeAdForm();await loadHomeAds()}catch(e){setStatus('homeAdStatus',e.message)}};
$('clearHomeAd').onclick=clearHomeAdForm;$('refreshHomeAds').onclick=loadHomeAds;

async function loadSubscriptions(){try{const list=await rpc('admin_partner_subscriptions');$('subscriptionList').innerHTML=(list||[]).map(s=>{const access=s.access_until?new Date(s.access_until).toLocaleDateString():'—';return '<div class="card"><div class="row"><div><b>'+esc(s.business_name)+'</b><div class="muted">Access until '+esc(access)+(s.paid_until?' · Paid':' · 3 months FREE')+'</div></div><span class="pill">'+esc(String(s.subscription_status||'').toUpperCase())+'</span></div><div class="two"><input id="payAmount-'+s.partner_id+'" class="field" type="number" min="0.01" step="0.01" placeholder="Amount"><select id="payMethod-'+s.partner_id+'" class="field"><option value="manual">Manual</option><option value="whish">Whish</option></select></div><div class="two"><input id="payMonths-'+s.partner_id+'" class="field" type="number" min="1" max="36" value="1" placeholder="Months"><input id="payRef-'+s.partner_id+'" class="field" placeholder="Payment reference (optional)"></div><button class="btn" onclick="confirmPartnerPayment(\''+s.partner_id+'\',\''+String(s.business_name||'').replace(/'/g,'')+'\')">CONFIRM PAYMENT</button></div>'}).join('')||'<div class="card muted">No partner subscriptions.</div>'}catch(e){$('subscriptionList').innerHTML='<div class="card error">'+esc(e.message)+'</div>'}}
window.confirmPartnerPayment=async(id,name)=>{const amount=Number($('payAmount-'+id).value||0),months=Number($('payMonths-'+id).value||0),method=$('payMethod-'+id).value,ref=$('payRef-'+id).value.trim();if(!(amount>0)){alert('Enter payment amount.');return}if(!Number.isInteger(months)||months<1||months>36){alert('Enter valid subscription months.');return}if(!confirm('Confirm '+method.toUpperCase()+' payment for '+name+'?'))return;try{await rpc('admin_confirm_partner_payment',{p_partner_id:id,p_amount:amount,p_payment_method:method,p_period_months:months,p_provider_reference:ref||null,p_note:null});alert('Payment confirmed and subscription extended.');await loadSubscriptions()}catch(e){alert(e.message)}};
$('refreshSubscriptions').onclick=loadSubscriptions;

'''
text = text.replace(js_anchor, js + js_anchor, 1)

# Final invariants: preserve critical existing features exactly once.
for needle in [
    'admin_draw_campaign_winners_v2',
    'send-push-message',
    'super-admin-create-admin',
    'admin_publish_iza_campaign',
    'admin_review_partner_ad',
    'admin_review_partner_item',
]:
    assert needle in text, f'Critical existing feature missing after patch: {needle}'

path.write_text(text, encoding='utf-8')
print('Applied guarded WENIK Admin production tools patch.')
