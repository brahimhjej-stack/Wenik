from pathlib import Path

# Partner account: submit editable business profile changes for admin approval.
p=Path('partner.html')
s=p.read_text(encoding='utf-8')

old='''  <div class="card" id="profileCard">\n    <div class="eyebrow">BUSINESS PROFILE</div><h2>Complete My Profile</h2>\n    <div class="muted">Keep your business information accurate for WENIK customers.</div>\n    <!-- WENIK PARTNER PROFILE AREA SYNC V1 -->\n    <select id="profileArea" class="field" aria-label="Area / city">'''
new='''  <div class="card" id="profileCard">\n    <div class="eyebrow">BUSINESS PROFILE</div><h2>Edit My Profile</h2>\n    <div class="muted">Submit profile changes for WENIK Admin approval. Your current public profile stays unchanged until approval.</div>\n    <div id="profileApprovalStatus" class="muted" style="margin-top:10px"></div>\n    <input id="profileBusiness" class="field" placeholder="Business name">\n    <!-- WENIK PARTNER PROFILE AREA SYNC V1 -->\n    <select id="profileArea" class="field" aria-label="Area / city">'''
if old not in s: raise SystemExit('partner profile card target missing')
s=s.replace(old,new,1)

old="function fillProfile(x){const map={profileArea:'area',profileAddress:'address',profilePhone:'phone',profileMenu:'menu_url',profileLocation:'location_url',profileInstagram:'instagram_url',profileFacebook:'facebook_url',profileTiktok:'tiktok_url',profileWebsite:'website_url'};for(const [id,k] of Object.entries(map))$(id).value=x?.[k]||''}"
new="function fillProfile(x){const map={profileBusiness:'business_name',profileArea:'area',profileAddress:'address',profilePhone:'phone',profileMenu:'menu_url',profileLocation:'location_url',profileInstagram:'instagram_url',profileFacebook:'facebook_url',profileTiktok:'tiktok_url',profileWebsite:'website_url'};for(const [id,k] of Object.entries(map))$(id).value=x?.[k]||''}"
if old not in s: raise SystemExit('fillProfile target missing')
s=s.replace(old,new,1)

old="$('saveProfileBtn').onclick=async()=>{try{$('saveProfileBtn').disabled=true;$('profileMsg').className='muted';$('profileMsg').textContent='Saving…';await rpc('partner_update_my_profile_v2',{p_area:$('profileArea').value.trim()||null,p_address:$('profileAddress').value.trim()||null,p_phone:$('profilePhone').value.trim()||null,p_menu_url:$('profileMenu').value.trim()||null,p_social_url:null,p_location_url:$('profileLocation').value.trim()||null,p_instagram_url:$('profileInstagram').value.trim()||null,p_facebook_url:$('profileFacebook').value.trim()||null,p_tiktok_url:$('profileTiktok').value.trim()||null,p_website_url:$('profileWebsite').value.trim()||null});$('profileMsg').className='success';$('profileMsg').textContent='Profile saved successfully.'}catch(e){$('profileMsg').className='error';$('profileMsg').textContent=e.message}finally{$('saveProfileBtn').disabled=false}};"
new="async function loadProfileChangeStatus(){try{const rows=await rpc('partner_my_profile_change_status');const r=rows?.[0];$('profileApprovalStatus').textContent=!r?'No pending profile changes.':r.status==='pending'?'Profile changes pending WENIK Admin approval.':r.status==='approved'?'Last profile change approved.':('Last profile change rejected'+(r.review_note?' · '+r.review_note:''));}catch{$('profileApprovalStatus').textContent=''}}\n$('saveProfileBtn').textContent='SUBMIT CHANGES FOR APPROVAL';\n$('saveProfileBtn').onclick=async()=>{try{$('saveProfileBtn').disabled=true;$('profileMsg').className='muted';$('profileMsg').textContent='Submitting…';await rpc('partner_submit_profile_change',{p_business_name:$('profileBusiness').value.trim()||null,p_area:$('profileArea').value.trim()||null,p_address:$('profileAddress').value.trim()||null,p_phone:$('profilePhone').value.trim()||null,p_menu_url:$('profileMenu').value.trim()||null,p_location_url:$('profileLocation').value.trim()||null,p_instagram_url:$('profileInstagram').value.trim()||null,p_facebook_url:$('profileFacebook').value.trim()||null,p_tiktok_url:$('profileTiktok').value.trim()||null,p_website_url:$('profileWebsite').value.trim()||null});$('profileMsg').className='success';$('profileMsg').textContent='Changes submitted. Your current profile stays live until WENIK Admin approves them.';await loadProfileChangeStatus()}catch(e){$('profileMsg').className='error';$('profileMsg').textContent=e.message}finally{$('saveProfileBtn').disabled=false}};"
if old not in s: raise SystemExit('save profile target missing')
s=s.replace(old,new,1)

old="await Promise.all([loadGifts(),loadMedia()])}"
new="await Promise.all([loadGifts(),loadMedia(),loadProfileChangeStatus()])}"
if old not in s: raise SystemExit('partner start target missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# Admin: show pending partner profile changes in Approvals and approve/reject them.
p=Path('admin.html')
s=p.read_text(encoding='utf-8')
old='''<section id="approvals" class="panel"><div class="card"><div class="row"><div><h2>Pending Partner Content</h2><div class="muted">Approve or reject partner ads and items.</div></div><button id="refreshApprovals" class="btn secondary" style="width:auto">REFRESH</button></div></div><div class="cols"><div><h3>Ads</h3><div id="pendingAds"></div></div><div><h3>Items</h3><div id="pendingItems"></div></div></div></section>'''
new='''<section id="approvals" class="panel"><div class="card"><div class="row"><div><h2>Pending Partner Content</h2><div class="muted">Approve or reject partner ads, items and profile edits.</div></div><button id="refreshApprovals" class="btn secondary" style="width:auto">REFRESH</button></div></div><div class="cols"><div><h3>Ads</h3><div id="pendingAds"></div></div><div><h3>Items</h3><div id="pendingItems"></div></div></div><h3>Profile Changes</h3><div id="pendingProfileChanges"></div></section>'''
if old not in s: raise SystemExit('admin approvals html target missing')
s=s.replace(old,new,1)

old="$('refreshApprovals').onclick=loadApprovals;"
new="""async function loadProfileApprovals(){try{const list=await rpc('admin_pending_partner_profile_changes');$('pendingProfileChanges').innerHTML=(list||[]).map(r=>{const o=r.old_values||{},n=r.new_values||{};const keys=['business_name','area','address','phone','menu_url','location_url','instagram_url','facebook_url','tiktok_url','website_url'];const changes=keys.filter(k=>String(o[k]??'')!==String(n[k]??'')).map(k=>'<div class=\"muted\" style=\"margin-top:6px\"><b>'+esc(k.replaceAll('_',' '))+'</b><br>Old: '+esc(o[k]??'—')+'<br>New: '+esc(n[k]??'—')+'</div>').join('');return '<div class=\"card\"><div class=\"row\"><b>'+esc(r.business_name||'Partner')+'</b><span class=\"pill\">PROFILE EDIT</span></div>'+changes+'<div class=\"actions\"><button class=\"btn ok\" onclick=\"reviewProfileChange(\\\''+r.request_id+'\\\',true)\">APPROVE</button><button class=\"btn danger\" onclick=\"reviewProfileChange(\\\''+r.request_id+'\\\',false)\">REJECT</button></div></div>'}).join('')||'<div class=\"card muted\">No pending profile changes.</div>'}catch(e){$('pendingProfileChanges').innerHTML='<div class=\"card error\">'+esc(e.message)+'</div>'}}\nwindow.reviewProfileChange=async(id,approve)=>{let note=null;if(!approve)note=prompt('Reason for rejection (optional):')||null;try{await rpc('admin_review_partner_profile_change',{p_request_id:id,p_approve:approve,p_note:note});await loadProfileApprovals()}catch(e){alert(e.message)}};\nconst originalLoadApprovals=loadApprovals;loadApprovals=async()=>{await Promise.all([originalLoadApprovals(),loadProfileApprovals()])};\n$('refreshApprovals').onclick=loadApprovals;"""
if old not in s: raise SystemExit('admin refresh approvals target missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Patched partner/admin staging profile edit approval flow only.')