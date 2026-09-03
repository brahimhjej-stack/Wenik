from pathlib import Path

partner = Path('partner.html')
admin = Path('admin.html')

p = partner.read_text(encoding='utf-8')
a = admin.read_text(encoding='utf-8')

PMARK = '<!-- WENIK PARTNER GIFTS UI -->'
AMARK = '<!-- WENIK ADMIN GIFTS APPROVAL UI -->'

if PMARK not in p:
    anchor = '  <button id="logoutBtn" class="btn secondary">LOG OUT</button>'
    assert anchor in p, 'partner logout anchor missing'
    html = '''  <!-- WENIK PARTNER GIFTS UI -->
  <div class="card" id="giftsCard">
    <div class="eyebrow">WENIK GIFTS</div><h2>My Gifts</h2>
    <div class="muted">Optional. Add as many gifts as you want. Every new or edited gift needs WENIK Admin approval.</div>
    <input id="giftName" class="field" placeholder="Gift name">
    <input id="giftDescription" class="field" placeholder="Short description (optional)">
    <button id="addGiftBtn" class="btn">+ ADD GIFT</button>
    <div id="giftMsg" class="muted"></div>
    <div id="giftList"></div>
  </div>
'''
    p = p.replace(anchor, html + anchor, 1)

    js_anchor = "$('logoutBtn').onclick=async()=>{stopCamera();await sb.auth.signOut();showLogin()};"
    assert js_anchor in p, 'partner JS logout anchor missing'
    js = r'''
function giftEsc(v){return String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
async function loadGifts(){
  try{const list=await rpc('partner_my_gifts');$('giftList').innerHTML=(list||[]).map(g=>'<div class="card"><div><b>'+giftEsc(g.name)+'</b><div class="muted">'+giftEsc(g.description||'')+'</div><div class="muted">Status: '+giftEsc(String(g.approval_status||'pending').toUpperCase())+'</div></div><div class="actions"><button class="btn secondary" data-edit-gift="'+g.id+'" data-name="'+giftEsc(g.name)+'" data-description="'+giftEsc(g.description||'')+'">EDIT</button>'+(g.approval_status==='approved'?'':'<button class="btn secondary" data-delete-gift="'+g.id+'">DELETE</button>')+'</div></div>').join('')||'<div class="muted" style="margin-top:16px">No gifts added yet.</div>';document.querySelectorAll('[data-delete-gift]').forEach(b=>b.onclick=async()=>{if(!confirm('Delete this gift?'))return;try{await rpc('partner_delete_gift',{p_gift_id:b.dataset.deleteGift});await loadGifts()}catch(e){$('giftMsg').className='error';$('giftMsg').textContent=e.message}});document.querySelectorAll('[data-edit-gift]').forEach(b=>b.onclick=async()=>{const name=prompt('Gift name:',b.dataset.name||'');if(name===null)return;const description=prompt('Short description (optional):',b.dataset.description||'');if(description===null)return;try{await rpc('partner_update_gift',{p_gift_id:b.dataset.editGift,p_name:name.trim(),p_description:description.trim()||null});$('giftMsg').className='success';$('giftMsg').textContent='Gift updated and sent back for Admin approval.';await loadGifts()}catch(e){$('giftMsg').className='error';$('giftMsg').textContent=e.message}})}catch(e){$('giftMsg').className='error';$('giftMsg').textContent=e.message}}
$('addGiftBtn').onclick=async()=>{try{const name=$('giftName').value.trim(),description=$('giftDescription').value.trim();if(!name)throw Error('Enter the gift name.');$('addGiftBtn').disabled=true;$('giftMsg').className='muted';$('giftMsg').textContent='Submitting for approval…';await rpc('partner_submit_gift',{p_name:name,p_description:description||null});$('giftName').value='';$('giftDescription').value='';$('giftMsg').className='success';$('giftMsg').textContent='Gift submitted. Waiting for Admin approval.';await loadGifts()}catch(e){$('giftMsg').className='error';$('giftMsg').textContent=e.message}finally{$('addGiftBtn').disabled=false}};
'''
    p = p.replace(js_anchor, js + js_anchor, 1)
    start_anchor = "$('business').textContent=p[0].business_name;$('login').classList.add('hidden');$('app').classList.remove('hidden')"
    assert start_anchor in p, 'partner start anchor missing'
    p = p.replace(start_anchor, start_anchor + ";await loadGifts()", 1)

if AMARK not in a:
    anchor = '<section id="messages" class="panel">'
    assert anchor in a, 'admin messages anchor missing'
    html = '''<!-- WENIK ADMIN GIFTS APPROVAL UI -->
<section id="giftsApproval" class="panel"><div class="card"><div class="row"><div><h2>Partner Gifts</h2><div class="muted">Confirm or reject gifts submitted by partners. Approved gifts are ready for WIN.</div></div><button id="refreshGifts" class="btn secondary" style="width:auto">REFRESH</button></div></div><div id="pendingGifts"></div></section>

'''
    a = a.replace(anchor, html + anchor, 1)

    tabs_anchor = '<button class="tab" data-panel="messages">MESSAGES</button>'
    assert tabs_anchor in a, 'admin tab anchor missing'
    a = a.replace(tabs_anchor, '<button class="tab" data-panel="giftsApproval">GIFTS</button>'+tabs_anchor, 1)

    click_anchor = "if(b.dataset.panel==='messages')loadMessages();"
    assert click_anchor in a, 'admin tab JS anchor missing'
    a = a.replace(click_anchor, "if(b.dataset.panel==='giftsApproval')loadPendingGifts();"+click_anchor, 1)

    js_anchor = "async function loadAdmins(){"
    assert js_anchor in a, 'admin admins JS anchor missing'
    js = r'''
async function loadPendingGifts(){try{const list=await rpc('admin_pending_partner_gifts');$('pendingGifts').innerHTML=(list||[]).map(g=>'<div class="card"><div class="row"><div><b>'+esc(g.business_name)+'</b><h3>'+esc(g.name)+'</h3><div class="muted">'+esc(g.description||'')+'</div></div><span class="pill">PENDING</span></div><div class="actions"><button class="btn ok" onclick="reviewGift(\''+g.id+'\',\'approved\')">CONFIRM</button><button class="btn danger" onclick="reviewGift(\''+g.id+'\',\'rejected\')">REJECT</button></div></div>').join('')||'<div class="card muted">No pending gifts.</div>'}catch(e){$('pendingGifts').innerHTML='<div class="card error">'+esc(e.message)+'</div>'}}
window.reviewGift=async(id,status)=>{let note=null;if(status==='rejected'){note=prompt('Reason for rejection (optional):')||null}try{await rpc('admin_review_partner_gift',{p_gift_id:id,p_status:status,p_note:note});await loadPendingGifts()}catch(e){alert(e.message)}};
$('refreshGifts').onclick=loadPendingGifts;
'''
    a = a.replace(js_anchor, js + js_anchor, 1)

partner.write_text(p, encoding='utf-8')
admin.write_text(a, encoding='utf-8')

assert PMARK in partner.read_text(encoding='utf-8')
assert AMARK in admin.read_text(encoding='utf-8')
print('Partner Gifts UI + Admin approval UI patched safely')
