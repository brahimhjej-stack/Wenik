from pathlib import Path
p=Path('admin.html')
s=p.read_text()
anchor="async function rpc(n,a={}){const{data,error}=await sb.rpc(n,a);if(error)throw error;return data}\n"
helper="async function rpc(n,a={}){const{data,error}=await sb.rpc(n,a);if(error)throw error;return data}\nasync function sendExternalPush(messageId){if(!messageId)return null;try{const{data,error}=await sb.functions.invoke('send-push-message',{body:{message_id:messageId}});if(error)throw error;return data}catch(e){console.error('External push failed:',e);return null}}\n"
if anchor not in s: raise SystemExit('GUARD FAILED: rpc anchor not found')
s=s.replace(anchor,helper,1)
old_iza="window.publishIza=async id=>{try{const n=await rpc('admin_publish_iza_campaign',{p_iza_campaign_id:id});alert('IZA published to '+n+' customers.');await loadIza()}catch(e){alert(e.message)}};"
new_iza="window.publishIza=async id=>{try{const n=await rpc('admin_publish_iza_campaign',{p_iza_campaign_id:id});let pushed=false;try{const messageId=await rpc('admin_push_message_for_iza',{p_iza_campaign_id:id});const r=await sendExternalPush(messageId);pushed=!!r}catch(pushErr){console.error(pushErr)}alert('IZA published to '+n+' customers.'+(pushed?' Phone push sent.':' In-app sent; phone push could not be confirmed.'));await loadIza()}catch(e){alert(e.message)}};"
if old_iza not in s: raise SystemExit('GUARD FAILED: publishIza block not found')
s=s.replace(old_iza,new_iza,1)
old_win="window.publishWinner=async id=>{if(!confirm('Publish this winner and notify the customer?'))return;try{await rpc('admin_publish_winner',{p_winner_id:id,p_public_name:null});alert('Winner published and customer notified.');await loadWins()}catch(e){alert(e.message)}};"
new_win="window.publishWinner=async id=>{if(!confirm('Publish this winner and notify the customer?'))return;try{await rpc('admin_publish_winner',{p_winner_id:id,p_public_name:null});let pushed=false;try{const messageId=await rpc('admin_push_message_for_winner',{p_winner_id:id});const r=await sendExternalPush(messageId);pushed=!!r}catch(pushErr){console.error(pushErr)}alert(pushed?'Winner published. In-app + phone push sent.':'Winner published. In-app sent; phone push could not be confirmed.');await loadWins()}catch(e){alert(e.message)}};"
if old_win not in s: raise SystemExit('GUARD FAILED: publishWinner block not found')
s=s.replace(old_win,new_win,1)
if s.count("send-push-message")!=1: raise SystemExit('GUARD FAILED: unexpected push sender count')
if s.count("admin_push_message_for_iza")!=1: raise SystemExit('GUARD FAILED: IZA push lookup count')
if s.count("admin_push_message_for_winner")!=1: raise SystemExit('GUARD FAILED: WIN push lookup count')
p.write_text(s)
