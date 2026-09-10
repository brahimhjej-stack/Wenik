from pathlib import Path

p=Path('admin.html')
s=p.read_text(encoding='utf-8')
MARK='WENIK ADMIN DASHBOARD UPLOAD FIX V2'
if MARK in s:
    raise SystemExit('already applied')
if 'WENIK ADMIN DASHBOARD MOBILE POLISH V1' not in s:
    raise SystemExit('V1 dashboard polish missing')

css=r'''
<style id="wenikAdminDashboardUploadFixV2">
/* WENIK ADMIN DASHBOARD UPLOAD FIX V2 */
@media(max-width:520px){
  #dashboard .card{margin:10px 0!important}
  .wenikDashHead{padding:13px 14px!important}
  .wenikDashHead .muted{font-size:13px;line-height:1.25}
  .wenikDashEditor{padding:14px!important}
  .wenikDashEditor .row{align-items:center!important}
  .wenikDashEditor h3{font-size:20px!important;margin:4px 0 7px!important}
  .wenikFieldLabel{margin:11px 0 3px!important}
  .wenikUploadBox{padding:10px!important;border-radius:15px!important}
  .wenikFileInput{font-size:13px;margin-bottom:5px!important}
  #homeAdUploadBtn{min-height:44px!important;padding:11px 12px!important;margin-top:6px!important}
  .wenikHint{margin-top:6px!important;font-size:11px!important}
  .wenikDashPreview{margin-top:8px!important;max-height:190px!important}
  .wenikAdvancedUrl{margin-top:7px!important}
  .wenikDashEditor .field,.wenikDashEditor select{min-height:44px!important;padding:11px 12px!important;margin-top:5px!important}
  .wenikAdvancedGrid{gap:7px!important;margin-top:5px!important}
  .wenikDashEditor .actions{margin-top:11px!important}
}
</style>
'''

js=r'''
<script id="wenikAdminDashboardUploadFixRuntimeV2">
(function(){
  function $(id){return document.getElementById(id)}
  function setMsg(msg,ok){
    const box=$('homeAdStatus');
    if(!box)return;
    box.textContent=msg||'';
    box.classList.toggle('good',!!ok);
    box.classList.toggle('error',!ok&&!!msg);
  }
  function preview(url){
    const p=$('homeAdPreview');
    if(!p)return;
    if(url){p.src=url;p.classList.remove('hidden')}else{p.removeAttribute('src');p.classList.add('hidden')}
  }
  async function uploadSelected(){
    const file=$('homeAdUpload'),btn=$('homeAdUploadBtn'),url=$('homeAdImage');
    if(!file||!btn||!url)return;
    const f=file.files&&file.files[0];
    if(!f){file.click();return}
    if(!/^image\//i.test(f.type)){setMsg('Please choose an image file.');return}
    if(f.size>8*1024*1024){setMsg('Image is too large. Maximum 8 MB.');return}
    if(btn.dataset.busy==='1')return;
    btn.dataset.busy='1';btn.disabled=true;btn.textContent='UPLOADING...';setMsg('Uploading image...',true);
    try{
      const auth=await sb.auth.getUser();
      const uid=auth&&auth.data&&auth.data.user&&auth.data.user.id;
      if(!uid)throw Error('Admin session expired. Please login again.');
      const ext=((f.name.split('.').pop()||'jpg').replace(/[^a-z0-9]/gi,'').toLowerCase()||'jpg');
      const name=Date.now()+'-'+Math.random().toString(36).slice(2,8)+'.'+ext;
      const candidates=[uid+'/home-dashboard/'+name,'home-dashboard/'+uid+'/'+name];
      let uploaded=null,lastErr=null;
      for(const path of candidates){
        const r=await sb.storage.from('partner-media').upload(path,f,{cacheControl:'3600',upsert:false,contentType:f.type});
        if(!r.error){uploaded=path;break}
        lastErr=r.error;
      }
      if(!uploaded)throw lastErr||Error('Upload failed.');
      const pub=sb.storage.from('partner-media').getPublicUrl(uploaded);
      const publicUrl=pub&&pub.data&&pub.data.publicUrl;
      if(!publicUrl)throw Error('Could not create image URL.');
      url.value=publicUrl;preview(publicUrl);setMsg('Image uploaded ✓ Now press SAVE BANNER.',true);
    }catch(e){
      setMsg((e&&e.message)||'Image upload failed.');
    }finally{
      btn.dataset.busy='0';btn.disabled=false;btn.textContent='UPLOAD IMAGE';
    }
  }
  function bind(){
    const file=$('homeAdUpload'),btn=$('homeAdUploadBtn'),url=$('homeAdImage');
    if(!file||!btn||!url)return;
    btn.onclick=function(ev){ev.preventDefault();ev.stopPropagation();uploadSelected()};
    file.onchange=function(){
      const f=file.files&&file.files[0];
      if(f){preview(URL.createObjectURL(f));setMsg('Image selected. Press UPLOAD IMAGE.',true)}
    };
    url.oninput=function(){preview(url.value.trim())};
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});else bind();
  setTimeout(bind,700);
})();
</script>
'''

s=s.replace('</head>',css+'\n</head>',1)
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Admin Dashboard upload V2 fix applied')
