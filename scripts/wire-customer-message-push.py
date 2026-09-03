from pathlib import Path
p=Path('admin.html')
s=p.read_text()
old="$('sendMsg').onclick=async()=>{try{const title=$('msgTitle').value.trim(),body=$('msgBody').value.trim();if(!title||!body)throw Error('Title and body are required.');const partners=$('msgAudience').value==='partners';const id=await rpc('admin_create_message',{p_title:title,p_body:body,p_channel:partners?'partner_inbox':'in_app',p_audience:{type:partners?'all_partners':'all_customers'},p_send_now:false,p_scheduled_at:null});const n=await rpc('admin_send_message',{p_message_id:id});setStatus('msgStatus','Sent to '+n+' recipients.',true);$('msgTitle').value='';$('msgBody').value='';await loadMessages()}catch(e){setStatus('msgStatus',e.message)}};"
new="$('sendMsg').onclick=async()=>{try{const title=$('msgTitle').value.trim(),body=$('msgBody').value.trim();if(!title||!body)throw Error('Title and body are required.');const partners=$('msgAudience').value==='partners';const id=await rpc('admin_create_message',{p_title:title,p_body:body,p_channel:partners?'partner_inbox':'in_app',p_audience:{type:partners?'all_partners':'all_customers'},p_send_now:false,p_scheduled_at:null});const n=await rpc('admin_send_message',{p_message_id:id});let pushText='';if(!partners){const r=await sendExternalPush(id);pushText=r?' + phone push':' + in-app; phone push could not be confirmed'}setStatus('msgStatus','Sent to '+n+' recipients'+pushText+'.',true);$('msgTitle').value='';$('msgBody').value='';await loadMessages()}catch(e){setStatus('msgStatus',e.message)}};"
if old not in s: raise SystemExit('GUARD FAILED: exact sendMsg block not found')
if s.count(old)!=1: raise SystemExit('GUARD FAILED: unexpected sendMsg block count')
s=s.replace(old,new,1)
if s.count("sendExternalPush(id)")!=1: raise SystemExit('GUARD FAILED: customer message push not unique')
p.write_text(s)
