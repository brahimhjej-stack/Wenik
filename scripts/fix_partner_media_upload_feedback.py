from pathlib import Path
p=Path('partner.html')
s=p.read_text()
marker='/* WENIK PARTNER MEDIA UPLOAD DIAGNOSTICS V1 */'
if marker in s:
    raise SystemExit('already applied')
old="""async function uploadMedia(slot){try{if(!partnerProfile?.partner_id)throw Error('Partner profile not loaded.');const f=$('mediaFile-'+slot).files?.[0];if(!f)throw Error('Choose an image first.');if(f.size>8*1024*1024)throw Error('Image is too large. Maximum 8 MB.');$('mediaMsg').className='muted';$('mediaMsg').textContent='Uploading image '+slot+'…';const ext=(f.name.split('.').pop()||'jpg').replace(/[^a-z0-9]/gi,'').toLowerCase()||'jpg',path=partnerProfile.partner_id+'/slot-'+slot+'-'+Date.now()+'.'+ext;const up=await sb.storage.from('partner-media').upload(path,f,{upsert:false,contentType:f.type||undefined});if(up.error)throw up.error;const pub=sb.storage.from('partner-media').getPublicUrl(path).data.publicUrl;await rpc('partner_submit_ad',{p_slot_no:slot,p_image_url:pub,p_title:partnerProfile.business_name,p_description:null,p_cta_label:null,p_cta_url:null});$('mediaMsg').className='success';$('mediaMsg').textContent='Image submitted. Waiting for Admin approval.';await loadMedia()}catch(e){$('mediaMsg').className='error';$('mediaMsg').textContent=e.message}}
"""
new="""/* WENIK PARTNER MEDIA UPLOAD DIAGNOSTICS V1 */
function mediaErrorMessage(e,stage='upload'){
  const raw=String(e?.message||e?.error_description||e?.error||e||'Unknown error');
  const low=raw.toLowerCase();
  if(low.includes('row-level security')||low.includes('rls')||low.includes('policy')||low.includes('unauthorized')||low.includes('403'))return 'Image upload is blocked by WENIK Storage permission. Please contact WENIK Admin. ('+raw+')';
  if(low.includes('bucket')&&low.includes('not found'))return 'WENIK image storage is not available. Please contact WENIK Admin. ('+raw+')';
  if(stage==='register')return 'The image uploaded, but WENIK could not submit it for Admin approval. Please retry. ('+raw+')';
  return 'Image upload failed. '+raw;
}
async function uploadMedia(slot){
  const btn=document.querySelector('[data-upload-slot="'+slot+'"]');
  let uploadedPath='';
  try{
    if(!partnerProfile?.partner_id)throw Error('Partner profile not loaded.');
    const input=$('mediaFile-'+slot),f=input?.files?.[0];
    if(!f)throw Error('Choose an image first.');
    if(!String(f.type||'').startsWith('image/'))throw Error('Please choose an image file.');
    if(f.size>8*1024*1024)throw Error('Image is too large. Maximum 8 MB.');
    if(btn){btn.disabled=true;btn.dataset.oldText=btn.textContent;btn.textContent='UPLOADING…'}
    $('mediaMsg').className='muted';$('mediaMsg').textContent='Uploading image '+slot+'…';
    const ext=(f.name.split('.').pop()||'jpg').replace(/[^a-z0-9]/gi,'').toLowerCase()||'jpg';
    uploadedPath=partnerProfile.partner_id+'/slot-'+slot+'-'+Date.now()+'.'+ext;
    const up=await sb.storage.from('partner-media').upload(uploadedPath,f,{upsert:false,contentType:f.type||'image/jpeg',cacheControl:'3600'});
    if(up.error)throw Object.assign(up.error,{wenikStage:'upload'});
    const pubData=sb.storage.from('partner-media').getPublicUrl(uploadedPath)?.data;
    const pub=pubData?.publicUrl;
    if(!pub)throw Object.assign(Error('Public image URL was not created.'),{wenikStage:'public-url'});
    $('mediaMsg').textContent='Image uploaded. Sending for Admin approval…';
    try{
      await rpc('partner_submit_ad',{p_slot_no:slot,p_image_url:pub,p_title:partnerProfile.business_name,p_description:null,p_cta_label:null,p_cta_url:null});
    }catch(regErr){
      regErr.wenikStage='register';
      try{await sb.storage.from('partner-media').remove([uploadedPath])}catch{}
      throw regErr;
    }
    $('mediaMsg').className='success';$('mediaMsg').textContent='Image submitted successfully. Waiting for WENIK Admin approval.';
    if(input)input.value='';
    await loadMedia();
  }catch(e){
    console.error('WENIK partner image error',{slot,stage:e?.wenikStage||'upload',error:e});
    $('mediaMsg').className='error';$('mediaMsg').textContent=mediaErrorMessage(e,e?.wenikStage||'upload');
  }finally{
    if(btn){btn.disabled=false;btn.textContent=btn.dataset.oldText||('UPLOAD / REPLACE IMAGE '+slot)}
  }
}
"""
if old not in s:
    raise SystemExit('uploadMedia anchor missing')
s=s.replace(old,new,1)
p.write_text(s)
print('patched Partner media upload diagnostics')
