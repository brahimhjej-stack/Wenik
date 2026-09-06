import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const U='https://zkrnzwnbdoaqanqzznlw.supabase.co';
const K='sb_publishable_Q8pOXn-3YAUo_6OX6c2bKg_mLKH8O0k';
// IMPORTANT: share the exact Admin auth session used by admin.html.
const sb=createClient(U,K,{auth:{storageKey:'wenik-admin-auth'}});
const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function rpc(n,a={}){const{data,error}=await sb.rpc(n,a);if(error)throw error;return data}

async function waitForAdmin(){
  for(let i=0;i<80;i++){
    const gifts=$('giftsApproval');
    if(gifts)return gifts;
    await new Promise(r=>setTimeout(r,250));
  }
  return null;
}

async function install(){
  const gifts=await waitForAdmin();
  if(!gifts||$('wenikAdminGiftEntry'))return;

  const card=document.createElement('div');
  card.className='card';
  card.id='wenikAdminGiftEntry';
  card.innerHTML=`
    <h2>Add Gift</h2>
    <div class="muted">WENIK Admin enters each Partner gift and decides its Points value.</div>
    <select id="wgPartner" class="field"><option value="">Select Partner</option></select>
    <input id="wgName" class="field" placeholder="Gift name · e.g. $20 Voucher">
    <textarea id="wgDescription" class="field" rows="3" placeholder="Description (optional)"></textarea>
    <div class="two">
      <input id="wgQty" class="field" type="number" min="1" step="1" value="1" placeholder="Quantity">
      <input id="wgPoints" class="field" type="number" min="1" step="1" placeholder="Points required">
    </div>
    <button id="wgSave" class="btn">SAVE GIFT + POINTS</button>
    <div id="wgMsg" class="status"></div>`;

  // Always place the form at the very top of GIFTS so it is impossible to miss on mobile.
  gifts.prepend(card);

  async function loadPartners(){
    const rows=await rpc('admin_partner_subscriptions');
    $('wgPartner').innerHTML='<option value="">Select Partner</option>'+((rows||[]).map(p=>`<option value="${p.partner_id}">${esc(p.business_name)}</option>`).join(''));
  }

  $('wgSave').onclick=async()=>{
    const partner=$('wgPartner').value;
    const name=$('wgName').value.trim();
    const description=$('wgDescription').value.trim()||null;
    const quantity=Number($('wgQty').value);
    const points=Number($('wgPoints').value);
    const msg=$('wgMsg');
    if(!partner||!name||!Number.isInteger(quantity)||quantity<1||!Number.isInteger(points)||points<1){
      msg.className='status error';
      msg.textContent='Partner, Gift name, Quantity and Points are required.';
      return;
    }
    $('wgSave').disabled=true;
    try{
      await rpc('admin_create_partner_gift',{p_partner_id:partner,p_name:name,p_description:description,p_quantity:quantity,p_points_cost:points});
      msg.className='status good';
      msg.textContent=`Saved ✓ ${name} · ${points.toLocaleString()} Points`;
      $('wgName').value='';$('wgDescription').value='';$('wgQty').value='1';$('wgPoints').value='';
      $('refreshGifts')?.click();
    }catch(e){msg.className='status error';msg.textContent=e.message}
    finally{$('wgSave').disabled=false}
  };

  // Wait for the logged-in Admin session before loading protected Partner data.
  for(let i=0;i<40;i++){
    const {data:{session}}=await sb.auth.getSession();
    if(session){
      try{await loadPartners();$('wgMsg').textContent=''}catch(e){$('wgMsg').className='status error';$('wgMsg').textContent=e.message}
      return;
    }
    await new Promise(r=>setTimeout(r,250));
  }
  $('wgMsg').className='status error';
  $('wgMsg').textContent='Log in as WENIK Admin, then open GIFTS.';
}

install();
