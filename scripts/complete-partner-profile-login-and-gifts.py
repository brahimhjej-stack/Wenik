from pathlib import Path
p=Path('partner.html')
s=p.read_text()
if 'WENIK PARTNER PROFILE COMPLETION V2' in s:
    raise SystemExit('already applied')
# login field: phone -> username
s=s.replace('<input id="phone" class="field" placeholder="Mobile" inputmode="tel" autocomplete="tel">','<input id="username" class="field" placeholder="Username" autocomplete="username">',1)
# insert profile/password/media cards before gifts
anchor='  <!-- WENIK PARTNER GIFTS UI -->\n'
if anchor not in s: raise SystemExit('gift anchor missing')
block='''  <!-- WENIK PARTNER PROFILE COMPLETION V2 -->
  <div id="passwordCard" class="card hidden">
    <div class="eyebrow">SECURITY</div><h2>Change Temporary Password</h2>
    <div class="muted">For security, choose your own password before continuing.</div>
    <input id="newPassword" class="field" type="password" minlength="8" placeholder="New password · minimum 8 characters">
    <button id="changePasswordBtn" class="btn">CHANGE PASSWORD</button><div id="passwordMsg" class="muted"></div>
  </div>
  <div class="card" id="profileCard">
    <div class="eyebrow">BUSINESS PROFILE</div><h2>Complete My Profile</h2>
    <div class="muted">Keep your business information accurate for WENIK customers.</div>
    <input id="profileArea" class="field" placeholder="Area / city">
    <input id="profileAddress" class="field" placeholder="Address">
    <input id="profilePhone" class="field" placeholder="Business phone" inputmode="tel">
    <input id="profileMenu" class="field" placeholder="Menu URL (optional)">
    <input id="profileLocation" class="field" placeholder="Google Maps / location URL (optional)">
    <input id="profileInstagram" class="field" placeholder="Instagram URL (optional)">
    <input id="profileFacebook" class="field" placeholder="Facebook URL (optional)">
    <input id="profileTiktok" class="field" placeholder="TikTok URL (optional)">
    <input id="profileWebsite" class="field" placeholder="Website URL (optional)">
    <button id="saveProfileBtn" class="btn">SAVE PROFILE</button><div id="profileMsg" class="muted"></div>
  </div>
  <div class="card" id="mediaCard">
    <div class="eyebrow">BUSINESS IMAGES</div><h2>My Images</h2>
    <div class="muted">Upload up to 5 images. New or changed images remain Pending until WENIK Admin approves them.</div>
    <div id="mediaSlots"></div>
    <div id="mediaMsg" class="muted"></div>
  </div>
'''
s=s.replace(anchor,block+anchor,1)
# remove old phone helper if present; harmless otherwise
s=s.replace("function ph(v){let d=v.replace(/\\D/g,'');if(d.startsWith('961'))return'+'+d;if(d.startsWith('0'))d=d.slice(1);return'+961'+d}\n",'',1)
# replace start function and login handler
old="""async function start(){
  const{data:{session}}=await sb.auth.getSession();if(!session)return showLogin();
  try{const p=await rpc('partner_my_profile');if(!p?.length)throw Error('This account is not a partner.');$('business').textContent=p[0].business_name;$('login').classList.add('hidden');$('app').classList.remove('hidden');await loadGifts()}
  catch(e){await sb.auth.signOut();showLogin(e.message)}
}
function showLogin(m=''){$('app').classList.add('hidden');$('login').classList.remove('hidden');$('loginMsg').textContent=m}
$('loginBtn').onclick=async()=>{try{$('loginMsg').textContent='Signing in…';const{error}=await sb.auth.signInWithPassword({phone:ph($('phone').value),password:$('password').value});if(error)throw error;await start()}catch(e){$('loginMsg').textContent=e.message}};
"""
new="""let partnerProfile=null;
async function start(){
  const{data:{session}}=await sb.auth.getSession();if(!session)return showLogin();
  try{const p=await rpc('partner_my_profile_v2');if(!p?.length)throw Error('This account is not a partner.');partnerProfile=p[0];$('business').textContent=partnerProfile.business_name;$('login').classList.add('hidden');$('app').classList.remove('hidden');fillProfile(partnerProfile);const st=await rpc('partner_login_state');if(st?.[0]?.must_change_password)$('passwordCard').classList.remove('hidden');else $('passwordCard').classList.add('hidden');await Promise.all([loadGifts(),loadMedia()])}
  catch(e){await sb.auth.signOut();showLogin(e.message)}
}
function showLogin(m=''){$('app').classList.add('hidden');$('login').classList.remove('hidden');$('loginMsg').textContent=m}
$('loginBtn').onclick=async()=>{try{$('loginMsg').textContent='Signing in…';const username=$('username').value.trim().toLowerCase(),password=$('password').value;if(!username||!password)throw Error('Enter username and password.');const{data,error}=await sb.functions.invoke('partner-login',{body:{username,password}});if(error)throw error;if(data?.error)throw Error(data.error==='account_locked'?'Account temporarily locked. Try again later.':'Invalid username or password.');const r=await sb.auth.setSession({access_token:data.access_token,refresh_token:data.refresh_token});if(r.error)throw r.error;await start()}catch(e){$('loginMsg').textContent=e.message||'Login failed.'}};
"""
if old not in s: raise SystemExit('start/login anchor missing')
s=s.replace(old,new,1)
# insert profile/media JS before giftEsc
js_anchor="function giftEsc(v){"
if js_anchor not in s: raise SystemExit('giftEsc anchor missing')
js="""function fillProfile(x){const map={profileArea:'area',profileAddress:'address',profilePhone:'phone',profileMenu:'menu_url',profileLocation:'location_url',profileInstagram:'instagram_url',profileFacebook:'facebook_url',profileTiktok:'tiktok_url',profileWebsite:'website_url'};for(const [id,k] of Object.entries(map))$(id).value=x?.[k]||''}
$('saveProfileBtn').onclick=async()=>{try{$('saveProfileBtn').disabled=true;$('profileMsg').className='muted';$('profileMsg').textContent='Saving…';await rpc('partner_update_my_profile_v2',{p_area:$('profileArea').value.trim()||null,p_address:$('profileAddress').value.trim()||null,p_phone:$('profilePhone').value.trim()||null,p_menu_url:$('profileMenu').value.trim()||null,p_social_url:null,p_location_url:$('profileLocation').value.trim()||null,p_instagram_url:$('profileInstagram').value.trim()||null,p_facebook_url:$('profileFacebook').value.trim()||null,p_tiktok_url:$('profileTiktok').value.trim()||null,p_website_url:$('profileWebsite').value.trim()||null});$('profileMsg').className='success';$('profileMsg').textContent='Profile saved successfully.'}catch(e){$('profileMsg').className='error';$('profileMsg').textContent=e.message}finally{$('saveProfileBtn').disabled=false}};
$('changePasswordBtn').onclick=async()=>{try{const pw=$('newPassword').value;if(pw.length<8)throw Error('Password must be at least 8 characters.');$('changePasswordBtn').disabled=true;$('passwordMsg').textContent='Updating…';const{error}=await sb.auth.updateUser({password:pw});if(error)throw error;await rpc('partner_mark_password_changed');$('newPassword').value='';$('passwordMsg').className='success';$('passwordMsg').textContent='Password changed successfully.';setTimeout(()=>$('passwordCard').classList.add('hidden'),700)}catch(e){$('passwordMsg').className='error';$('passwordMsg').textContent=e.message}finally{$('changePasswordBtn').disabled=false}};
async function loadMedia(){try{const list=await rpc('partner_my_ads');const by=new Map((list||[]).map(x=>[Number(x.slot_no),x]));$('mediaSlots').innerHTML=[1,2,3,4,5].map(i=>{const a=by.get(i);return '<div class="card"><div class="eyebrow">IMAGE '+i+'</div>'+(a?.image_url?'<img src="'+giftEsc(a.image_url)+'" style="width:100%;max-height:220px;object-fit:cover;border-radius:18px;margin-top:12px">':'<div class="muted" style="margin-top:12px">No image yet.</div>')+'<div class="muted">'+(a?'Status: '+giftEsc(String(a.approval_status||'pending').toUpperCase()):'')+'</div><input id="mediaFile-'+i+'" class="field" type="file" accept="image/*"><button class="btn secondary" data-upload-slot="'+i+'">UPLOAD / REPLACE IMAGE '+i+'</button></div>'}).join('');document.querySelectorAll('[data-upload-slot]').forEach(b=>b.onclick=()=>uploadMedia(Number(b.dataset.uploadSlot)))}catch(e){$('mediaMsg').className='error';$('mediaMsg').textContent=e.message}}
async function uploadMedia(slot){try{if(!partnerProfile?.partner_id)throw Error('Partner profile not loaded.');const f=$('mediaFile-'+slot).files?.[0];if(!f)throw Error('Choose an image first.');if(f.size>8*1024*1024)throw Error('Image is too large. Maximum 8 MB.');$('mediaMsg').className='muted';$('mediaMsg').textContent='Uploading image '+slot+'…';const ext=(f.name.split('.').pop()||'jpg').replace(/[^a-z0-9]/gi,'').toLowerCase()||'jpg',path=partnerProfile.partner_id+'/slot-'+slot+'-'+Date.now()+'.'+ext;const up=await sb.storage.from('partner-media').upload(path,f,{upsert:false,contentType:f.type||undefined});if(up.error)throw up.error;const pub=sb.storage.from('partner-media').getPublicUrl(path).data.publicUrl;await rpc('partner_submit_ad',{p_slot_no:slot,p_image_url:pub,p_title:partnerProfile.business_name,p_description:null,p_cta_label:null,p_cta_url:null});$('mediaMsg').className='success';$('mediaMsg').textContent='Image submitted. Waiting for Admin approval.';await loadMedia()}catch(e){$('mediaMsg').className='error';$('mediaMsg').textContent=e.message}}

"""
s=s.replace(js_anchor,js+js_anchor,1)
# Replace gift render to show quantity and edit quantity
oldfrag="<div class=\"muted\">Status: '+giftEsc(String(g.approval_status||'pending').toUpperCase())+'</div>"
newfrag="<div class=\"muted\">Quantity: '+Number(g.quantity||1)+' · Status: '+giftEsc(String(g.approval_status||'pending').toUpperCase())+'</div>"
if oldfrag in s: s=s.replace(oldfrag,newfrag,1)
s=s.replace("data-description=\"'+giftEsc(g.description||'')+'\">EDIT", "data-description=\"'+giftEsc(g.description||'')+'\" data-quantity=\"'+Number(g.quantity||1)+'\">EDIT",1)
oldcall="""const description=prompt('Short description (optional):',b.dataset.description||'');if(description===null)return;try{await rpc('partner_update_gift',{p_gift_id:b.dataset.editGift,p_name:name.trim(),p_description:description.trim()||null});"""
newcall="""const description=prompt('Short description (optional):',b.dataset.description||'');if(description===null)return;const qRaw=prompt('Quantity:',b.dataset.quantity||'1');if(qRaw===null)return;const quantity=Number(qRaw);if(!Number.isInteger(quantity)||quantity<1){alert('Quantity must be 1 or more.');return}try{await rpc('partner_update_gift',{p_gift_id:b.dataset.editGift,p_name:name.trim(),p_description:description.trim()||null,p_quantity:quantity});"""
if oldcall not in s: raise SystemExit('gift edit call anchor missing')
s=s.replace(oldcall,newcall,1)
p.write_text(s)
print('patched partner.html')
