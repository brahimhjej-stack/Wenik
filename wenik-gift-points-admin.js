import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const U='https://zkrnzwnbdoaqanqzznlw.supabase.co';
const K='sb_publishable_Q8pOXn-3YAUo_6OX6c2bKg_mLKH8O0k';
const sb=createClient(U,K,{auth:{storageKey:'wenik-admin-auth'}});
const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function rpc(n,a={}){const{data,error}=await sb.rpc(n,a);if(error)throw error;return data}
function msg(id,text,ok=false){const e=$(id);if(!e)return;e.className='status '+(ok?'good':'error');e.textContent=text||''}

/* ---------------- GIFTS ---------------- */
async function waitForAdmin(){for(let i=0;i<80;i++){const gifts=$('giftsApproval');if(gifts)return gifts;await new Promise(r=>setTimeout(r,250))}return null}
async function installGifts(){
  const gifts=await waitForAdmin();
  if(!gifts||$('wenikAdminGiftEntry'))return;
  const card=document.createElement('div');
  card.className='card';card.id='wenikAdminGiftEntry';
  card.innerHTML=`<h2>Add Gift</h2><div class="muted">WENIK Admin enters each Partner gift and decides its Points value.</div><select id="wgPartner" class="field"><option value="">Select Partner</option></select><input id="wgName" class="field" placeholder="Gift name · e.g. $20 Voucher"><textarea id="wgDescription" class="field" rows="3" placeholder="Description (optional)"></textarea><input id="wgImage" class="field" type="file" accept="image/*"><img id="wgImagePreview" alt="Gift preview" style="display:none;width:100%;max-height:180px;object-fit:cover;border-radius:14px;margin:8px 0"><div class="two"><input id="wgQty" class="field" type="number" min="1" step="1" value="1" placeholder="Quantity"><input id="wgPoints" class="field" type="number" min="1" step="1" placeholder="Points required"></div><button id="wgSave" class="btn">SAVE GIFT + POINTS</button><div id="wgMsg" class="status"></div>`;
  gifts.prepend(card);
  async function loadPartners(){const rows=await rpc('admin_partner_subscriptions');const list=[...(rows||[])];if(!list.some(p=>p.business_name==='WENIK Gifts'))list.unshift({partner_id:'8c326b05-9a42-4ba0-bb70-ab4f8a146354',business_name:'WENIK Gifts'});$('wgPartner').innerHTML='<option value="">Select Partner</option>'+list.map(p=>`<option value="${p.partner_id}">${esc(p.business_name)}</option>`).join('')}
  $('wgImage').addEventListener('change',()=>{const f=$('wgImage').files?.[0],p=$('wgImagePreview');if(f){p.src=URL.createObjectURL(f);p.style.display='block'}else{p.removeAttribute('src');p.style.display='none'}});
  async function uploadGiftImage(){const f=$('wgImage').files?.[0];if(!f)return null;if(!/^image\\//i.test(f.type))throw Error('Please choose an image file.');if(f.size>8*1024*1024)throw Error('Image is too large. Maximum 8 MB.');const{data:{user},error}=await sb.auth.getUser();if(error)throw error;if(!user?.id)throw Error('Admin session expired.');const ext=((f.name.split('.').pop()||'jpg').replace(/[^a-z0-9]/gi,'').toLowerCase()||'jpg'),path=user.id+'/gift-images/'+Date.now()+'-'+Math.random().toString(36).slice(2,8)+'.'+ext;const up=await sb.storage.from('partner-media').upload(path,f,{cacheControl:'3600',upsert:false,contentType:f.type||undefined});if(up.error)throw up.error;return sb.storage.from('partner-media').getPublicUrl(path).data?.publicUrl||null}
  $('wgSave').onclick=async()=>{
    const partner=$('wgPartner').value,name=$('wgName').value.trim(),description=$('wgDescription').value.trim()||null,quantity=Number($('wgQty').value),points=Number($('wgPoints').value),box=$('wgMsg');
    if(!partner||!name||!Number.isInteger(quantity)||quantity<1||!Number.isInteger(points)||points<1){box.className='status error';box.textContent='Partner, Gift name, Quantity and Points are required.';return}
    $('wgSave').disabled=true;
    try{const created=await rpc('admin_create_partner_gift',{p_partner_id:partner,p_name:name,p_description:description,p_quantity:quantity,p_points_cost:points});const imageUrl=await uploadGiftImage();if(imageUrl){const row=Array.isArray(created)?created[0]:created;const giftId=row?.gift_id||row?.id||created;if(giftId)await rpc('admin_set_partner_gift_image',{p_gift_id:giftId,p_image_url:imageUrl})}box.className='status good';box.textContent=`Saved ✓ ${name} · ${points.toLocaleString()} Points`;$('wgName').value='';$('wgDescription').value='';$('wgQty').value='1';$('wgPoints').value='';$('wgImage').value='';$('wgImagePreview').style.display='none';$('refreshGifts')?.click()}
    catch(e){box.className='status error';box.textContent=e.message}
    finally{$('wgSave').disabled=false}
  };
  for(let i=0;i<40;i++){const{data:{session}}=await sb.auth.getSession();if(session){try{await loadPartners()}catch(e){$('wgMsg').className='status error';$('wgMsg').textContent=e.message}return}await new Promise(r=>setTimeout(r,250))}
}
installGifts();

async function installGiftQty(){
  const gifts=await waitForAdmin(); if(!gifts||$('giftQtyBox'))return;
  const card=document.createElement('div'); card.className='card'; card.id='giftQtyBox';
  card.innerHTML='<h3>Add Quantity to Existing Gift</h3><select id="giftQtySelect" class="field"><option value="">Select Gift</option></select><input id="giftQtyNumber" class="field" type="number" min="1" step="1" value="1"><button id="giftQtyButton" class="btn secondary">+ ADD QUANTITY</button><div id="giftQtyMsg" class="status"></div>';
  const entry=$('wenikAdminGiftEntry'); if(entry)entry.insertAdjacentElement('afterend',card); else gifts.prepend(card);
  async function load(){const rows=await rpc('admin_gift_inventory');$('giftQtySelect').innerHTML='<option value="">Select Gift</option>'+((rows||[]).map(g=>'<option value="'+g.gift_id+'">'+esc(g.partner_name)+' · '+esc(g.gift_name)+' · Qty '+Number(g.quantity||0)+'</option>').join(''))}
  $('giftQtyButton').onclick=async function(){const id=$('giftQtySelect').value,q=Number($('giftQtyNumber').value),box=$('giftQtyMsg');if(!id||!Number.isInteger(q)||q<1){box.className='status error';box.textContent='Select Gift and quantity.';return}this.disabled=true;try{const out=await rpc('admin_add_partner_gift_quantity',{p_gift_id:id,p_add_quantity:q});const row=Array.isArray(out)?out[0]:out;box.className='status good';box.textContent='Quantity updated. New total: '+Number(row&&row.new_quantity||0);$('giftQtyNumber').value='1';await load()}catch(e){box.className='status error';box.textContent=e.message}finally{this.disabled=false}};
  for(let i=0;i<40;i++){const s=await sb.auth.getSession();if(s.data.session){try{await load()}catch(e){$('giftQtyMsg').textContent=e.message}return}await new Promise(r=>setTimeout(r,250))}
}
installGiftQty();

/* ---------------- HOME BANNER UPLOAD ---------------- */
function ensureUploadStatus(){let box=$('homeAdUploadLiveStatus');if(box)return box;const btn=$('homeAdUploadBtn');if(!btn)return null;box=document.createElement('div');box.id='homeAdUploadLiveStatus';box.className='status';box.style.margin='8px 2px 0';box.style.fontWeight='800';btn.insertAdjacentElement('afterend',box);return box}
function uploadMsg(text,ok=false){const box=ensureUploadStatus();if(box){box.textContent=text||'';box.className='status '+(ok?'good':(text?'error':''))}const legacy=$('homeAdStatus');if(legacy){legacy.textContent=text||'';legacy.className='status '+(ok?'good':(text?'error':''))}}
function uploadPreview(url){const p=$('homeAdPreview');if(!p)return;if(url){p.src=url;p.classList.remove('hidden')}else{p.removeAttribute('src');p.classList.add('hidden')}}
async function doBannerUpload(ev){
  if(ev){ev.preventDefault();ev.stopPropagation();ev.stopImmediatePropagation?.()}
  const file=$('homeAdUpload'),btn=$('homeAdUploadBtn'),url=$('homeAdImage');if(!file||!btn||!url)return;
  const f=file.files?.[0];if(!f){uploadMsg('Choose an image first.');file.click();return}if(!/^image\//i.test(f.type)){uploadMsg('Please choose an image file.');return}if(f.size>8*1024*1024){uploadMsg('Image is too large. Maximum 8 MB.');return}if(btn.dataset.busy==='1')return;
  btn.dataset.busy='1';btn.disabled=true;btn.textContent='UPLOADING...';uploadMsg('Uploading image...',true);
  try{const{data:{user},error:authError}=await sb.auth.getUser();if(authError)throw authError;if(!user?.id)throw Error('Admin session expired. Please login again.');const ext=((f.name.split('.').pop()||'jpg').replace(/[^a-z0-9]/gi,'').toLowerCase()||'jpg');const name=Date.now()+'-'+Math.random().toString(36).slice(2,8)+'.'+ext;const paths=[user.id+'/home-dashboard/'+name,'home-dashboard/'+user.id+'/'+name];let uploaded=null,lastErr=null;for(const path of paths){const{error}=await sb.storage.from('partner-media').upload(path,f,{cacheControl:'3600',upsert:false,contentType:f.type||undefined});if(!error){uploaded=path;break}lastErr=error}if(!uploaded)throw lastErr||Error('Upload failed.');const{data}=sb.storage.from('partner-media').getPublicUrl(uploaded);if(!data?.publicUrl)throw Error('Could not create image URL.');url.value=data.publicUrl;uploadPreview(data.publicUrl);uploadMsg('Image uploaded ✓ Now press SAVE BANNER.',true)}catch(e){uploadMsg(e?.message||'Image upload failed.')}finally{btn.dataset.busy='0';btn.disabled=false;btn.textContent='UPLOAD IMAGE'}
}
function installUploadController(){const file=$('homeAdUpload'),btn=$('homeAdUploadBtn'),url=$('homeAdImage');if(!file||!btn||!url)return false;ensureUploadStatus();file.addEventListener('change',()=>{const f=file.files?.[0];if(f){uploadPreview(URL.createObjectURL(f));uploadMsg('Image selected ✓ Press UPLOAD IMAGE.',true)}else{uploadPreview('');uploadMsg('')}},true);url.addEventListener('input',()=>uploadPreview(url.value.trim()),true);return true}
document.addEventListener('click',e=>{if(e.target?.closest?.('#homeAdUploadBtn'))doBannerUpload(e)},true);
if(!installUploadController()){let tries=0;const timer=setInterval(()=>{tries++;if(installUploadController()||tries>40)clearInterval(timer)},250)}

/* ---------------- PARTNER TAXONOMY + MULTI BRANCH AREAS ---------------- */
const WENIK_PARTNER_CATEGORIES=['Restaurant','Café','Bakery & Sweets','Desserts','Clothing','Shoes','Accessories','Sportswear','Beauty Salon','Beauty Center','Barber Shop','Spa','Gym & Fitness','Hotel','Furniture','Home Décor','Home Appliances','Electronics','Mobile & Electronics','Kids & Toys','Kids & Baby','Jewelry','Florist','Pet Shop','Optical','Dental Clinic','Clinic','Pharmacy','Supermarket','Car Care','Car Rental','Education / Institute','Books & Stationery','Gifts & Handicrafts','Others'];
const WENIK_PARTNER_AREAS=['Beirut – Achrafieh','Beirut – Badaro','Beirut – Downtown','Beirut – Gemmayzeh','Beirut – Hamra','Beirut – Mar Mikhael','Beirut – Raouche','Beirut – Verdun','Beirut – Ras Beirut','Beirut – Clemenceau','Beirut – Mazraa','Beirut – Mar Elias','Beirut – Jnah','Beirut – Bir Hassan','Beirut – Ain El Mreisseh','Beirut – Saifi','Dahieh – Haret Hreik','Dahieh – Ghobeiry','Dahieh – Bourj El Barajneh','Dahieh – Chiyah','Dahieh – Mcharafieh','Dahieh – Hadath','Dahieh – Laylakeh','Dahieh – Hay El Sellom','Mount Lebanon – Baabda','Mount Lebanon – Hazmieh','Mount Lebanon – Furn El Chebbak','Mount Lebanon – Ain El Remmaneh','Mount Lebanon – Sin El Fil','Mount Lebanon – Dekwaneh','Mount Lebanon – Mkalles','Mount Lebanon – Jdeideh','Mount Lebanon – Baouchriyeh','Mount Lebanon – Bourj Hammoud','Mount Lebanon – Dora','Mount Lebanon – Zalka','Mount Lebanon – Jal El Dib','Mount Lebanon – Antelias','Mount Lebanon – Naccache','Mount Lebanon – Dbayeh','Mount Lebanon – Rabieh','Mount Lebanon – Bsalim','Mount Lebanon – Beit Mery','Mount Lebanon – Broummana','Mount Lebanon – Mansourieh','Mount Lebanon – Fanar','Mount Lebanon – Aley','Mount Lebanon – Bhamdoun','Mount Lebanon – Choueifat','Mount Lebanon – Jounieh','Mount Lebanon – Kaslik','Mount Lebanon – Zouk Mikael','Mount Lebanon – Zouk Mosbeh','Mount Lebanon – Ghazir','Mount Lebanon – Jbeil','Mount Lebanon – Batroun','Nabatieh – Nabatieh','South – Saida','South – Tyre','Bekaa – Zahle','North – Tripoli','Akkar – Halba','Other Area'];
const selectedPartnerAreas=[];
function setOptions(sel,placeholder,values){if(!sel)return;const current=sel.value;sel.innerHTML='<option value="">'+placeholder+'</option>'+values.map(v=>'<option value="'+esc(v)+'">'+esc(v)+'</option>').join('');if(values.includes(current))sel.value=current}
function renderAreaChips(){const box=$('newPartnerAreasSelected');if(!box)return;box.innerHTML=selectedPartnerAreas.map((a,i)=>`<span style="display:inline-flex;align-items:center;gap:7px;padding:8px 10px;border-radius:999px;background:#21192f;border:1px solid rgba(178,92,255,.35);font-size:12px;font-weight:800">${esc(a)}<button type="button" data-i="${i}" style="border:0;background:transparent;color:#ff93a8;font-weight:1000;font-size:16px;line-height:1">×</button></span>`).join('');box.querySelectorAll('button').forEach(b=>b.onclick=()=>{selectedPartnerAreas.splice(Number(b.dataset.i),1);renderAreaChips()})}
function installPartnerTaxonomy(){
  let cat=$('newPartnerCategory'),area=$('newPartnerArea');if(!cat||!area)return false;
  if(cat.tagName!=='SELECT'){const s=document.createElement('select');s.id='newPartnerCategory';s.className=cat.className||'field';cat.replaceWith(s);cat=s}setOptions(cat,'Select Category',WENIK_PARTNER_CATEGORIES);
  if(area.tagName!=='SELECT'){const s=document.createElement('select');s.id='newPartnerArea';s.className=area.className||'field';area.replaceWith(s);area=s}setOptions(area,'Select branch area',WENIK_PARTNER_AREAS);area.required=false;
  if(!$('addPartnerAreaBtn')){const wrap=document.createElement('div');wrap.style.display='grid';wrap.style.gridTemplateColumns='1fr auto';wrap.style.gap='8px';area.parentNode.insertBefore(wrap,area);wrap.appendChild(area);const add=document.createElement('button');add.id='addPartnerAreaBtn';add.type='button';add.className='btn secondary';add.style.width='auto';add.style.minWidth='110px';add.textContent='ADD AREA';wrap.appendChild(add);const chips=document.createElement('div');chips.id='newPartnerAreasSelected';chips.style.display='flex';chips.style.flexWrap='wrap';chips.style.gap='8px';chips.style.marginTop='8px';wrap.insertAdjacentElement('afterend',chips);const hint=document.createElement('div');hint.className='muted';hint.style.fontSize='12px';hint.style.marginTop='6px';hint.textContent='Add every branch area for this Partner.';chips.insertAdjacentElement('afterend',hint);add.onclick=()=>{const a=area.value.trim();if(!a)return msg('createPartnerStatus','Choose an Area first.');if(!selectedPartnerAreas.includes(a))selectedPartnerAreas.push(a);area.value='';renderAreaChips();msg('createPartnerStatus',selectedPartnerAreas.length+' branch area'+(selectedPartnerAreas.length===1?'':'s')+' selected.',true)}}
  return true;
}
if(!installPartnerTaxonomy()){let n=0;const t=setInterval(()=>{n++;if(installPartnerTaxonomy()||n>40)clearInterval(t)},250)}

// Override legacy Add Partner click so one account can have many branch areas.
document.addEventListener('click',async e=>{
  const btn=e.target?.closest?.('#createPartnerBtn');if(!btn)return;
  e.preventDefault();e.stopPropagation();e.stopImmediatePropagation?.();
  const pending=$('newPartnerArea')?.value?.trim();if(pending&&!selectedPartnerAreas.includes(pending))selectedPartnerAreas.push(pending);
  const business_name=$('newPartnerBusiness')?.value.trim(),category=$('newPartnerCategory')?.value.trim(),display_name=$('newPartnerName')?.value.trim(),username=$('newPartnerUsername')?.value.trim().toLowerCase(),password=$('newPartnerPassword')?.value||'',areas=[...selectedPartnerAreas];
  if(!business_name||!category||!areas.length||!username||!password){msg('createPartnerStatus','Business, category, at least one branch area, username and password are required.');return}
  if(password.length<8){msg('createPartnerStatus','Password must be at least 8 characters.');return}
  btn.disabled=true;msg('createPartnerStatus','Creating Partner account...',true);
  try{
    const{data,error}=await sb.functions.invoke('admin-create-partner',{body:{business_name,category,area:areas[0],display_name:display_name||business_name,username,password}});if(error)throw error;if(data?.error)throw Error(data.error);
    const partnerId=data?.partner?.id||data?.partner_id;if(!partnerId)throw Error('Partner created, but branch areas could not be linked.');
    await rpc('admin_set_partner_areas',{p_partner_id:partnerId,p_areas:areas});
    for(const id of ['newPartnerBusiness','newPartnerCategory','newPartnerArea','newPartnerName','newPartnerUsername','newPartnerPassword'])if($(id))$(id).value='';selectedPartnerAreas.splice(0);renderAreaChips();
    msg('createPartnerStatus','Partner created ✓ '+areas.length+' branch area'+(areas.length===1?'':'s')+' linked · 3 months FREE until '+new Date(data.partner.trial_ends_at).toLocaleDateString()+'.',true);$('refreshSubscriptions')?.click();
  }catch(err){msg('createPartnerStatus',err?.message||'Could not create Partner.')}
  finally{btn.disabled=false}
},true);
