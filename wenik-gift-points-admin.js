import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const U='https://zkrnzwnbdoaqanqzznlw.supabase.co';
const K='sb_publishable_Q8pOXn-3YAUo_6OX6c2bKg_mLKH8O0k';
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

// Final Admin Dashboard upload controller.
// Replaces the button node after parsing, removing all legacy/conflicting handlers in admin.html.
(function installDashboardUploadFinal(){
  function preview(url){
    const p=$('homeAdPreview');
    if(!p)return;
    if(url){p.src=url;p.classList.remove('hidden')}
    else{p.removeAttribute('src');p.classList.add('hidden')}
  }
  function statusBox(){
    let box=$('homeAdUploadLiveStatus');
    if(box)return box;
    const btn=$('homeAdUploadBtn');
    if(!btn)return null;
    box=document.createElement('div');
    box.id='homeAdUploadLiveStatus';
    box.className='status';
    box.style.margin='8px 2px 0';
    box.style.fontWeight='800';
    btn.insertAdjacentElement('afterend',box);
    return box;
  }
  function setMsg(msg,ok=false){
    const box=statusBox();
    if(box){box.textContent=msg||'';box.className='status '+(ok?'good':(msg?'error':''));}
    const legacy=$('homeAdStatus');
    if(legacy){legacy.textContent=msg||'';legacy.className='status '+(ok?'good':(msg?'error':''));}
  }
  function bind(){
    const file=$('homeAdUpload'),oldBtn=$('homeAdUploadBtn'),url=$('homeAdImage');
    if(!file||!oldBtn||!url)return false;
    if(oldBtn.dataset.finalUpload==='1')return true;

    const btn=oldBtn.cloneNode(true);
    btn.dataset.finalUpload='1';
    oldBtn.replaceWith(btn);
    statusBox();

    file.onchange=()=>{
      const f=file.files&&file.files[0];
      if(!f){preview('');setMsg('');return}
      preview(URL.createObjectURL(f));
      setMsg('Image selected ✓ Press UPLOAD IMAGE.',true);
    };
    url.oninput=()=>preview(url.value.trim());

    btn.onclick=async ev=>{
      ev.preventDefault();
      ev.stopPropagation();
      const f=file.files&&file.files[0];
      if(!f){setMsg('Choose an image first.');file.click();return}
      if(!/^image\//i.test(f.type)){setMsg('Please choose an image file.');return}
      if(f.size>8*1024*1024){setMsg('Image is too large. Maximum 8 MB.');return}
      if(btn.dataset.busy==='1')return;
      btn.dataset.busy='1';btn.disabled=true;btn.textContent='UPLOADING...';setMsg('Uploading image...',true);
      try{
        const {data:{user},error:authError}=await sb.auth.getUser();
        if(authError)throw authError;
        if(!user?.id)throw Error('Admin session expired. Please login again.');
        const ext=((f.name.split('.').pop()||'jpg').replace(/[^a-z0-9]/gi,'').toLowerCase()||'jpg');
        const name=Date.now()+'-'+Math.random().toString(36).slice(2,8)+'.'+ext;
        const paths=[user.id+'/home-dashboard/'+name,'home-dashboard/'+user.id+'/'+name];
        let uploaded=null,lastErr=null;
        for(const path of paths){
          const {error}=await sb.storage.from('partner-media').upload(path,f,{cacheControl:'3600',upsert:false,contentType:f.type||undefined});
          if(!error){uploaded=path;break}
          lastErr=error;
        }
        if(!uploaded)throw lastErr||Error('Upload failed.');
        const {data}=sb.storage.from('partner-media').getPublicUrl(uploaded);
        if(!data?.publicUrl)throw Error('Could not create image URL.');
        url.value=data.publicUrl;
        preview(data.publicUrl);
        setMsg('Image uploaded ✓ Now press SAVE BANNER.',true);
      }catch(e){
        console.error('WENIK banner upload',e);
        setMsg(e?.message||'Image upload failed.');
      }finally{
        btn.dataset.busy='0';btn.disabled=false;btn.textContent='UPLOAD IMAGE';
      }
    };
    return true;
  }
  if(bind())return;
  let tries=0;
  const timer=setInterval(()=>{tries++;if(bind()||tries>40)clearInterval(timer)},250);
})();
