from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker="<title>WENIK</title>"
if 'manifest.webmanifest' not in s:
    s=s.replace(marker,marker+'\n<link rel="manifest" href="/manifest.webmanifest">',1)
anchor="async function loadMe(){"
helper="""const WENIK_VAPID_PUBLIC_KEY='BHI2mvri3pacvHazW4kV-SXuKRMZsfdpNACT225u6jJyL2_oHB4Y_zExfjRAOFHqqkW5c8UnmGfpPlhCJh0H0V0';
function b64u8(s){const pad='='.repeat((4-s.length%4)%4),b=(s+pad).replace(/-/g,'+').replace(/_/g,'/'),raw=atob(b);return Uint8Array.from([...raw].map(c=>c.charCodeAt(0)))}
async function pushStateCard(){if(!('serviceWorker'in navigator)||!('PushManager'in window)||!('Notification'in window))return '<div class=\"card muted\">Push notifications are not supported on this browser.</div>';if(Notification.permission==='denied')return '<div class=\"card muted\">Phone notifications are blocked in browser settings.</div>';const reg=await navigator.serviceWorker.register('/sw.js');const sub=await reg.pushManager.getSubscription();return sub?'<div class=\"card\"><div class=\"row\"><b>Phone notifications</b><span class=\"badge\">ON</span></div><div class=\"muted\">WENIK can notify you even when the site is closed.</div></div>':'<div class=\"card\"><div class=\"row\"><b>Phone notifications</b><span class=\"badge\">OFF</span></div><div class=\"muted\">Turn on WIN, IZA and important WENIK alerts on this phone.</div><button class=\"btn\" style=\"margin-top:12px\" onclick=\"enablePush()\">ENABLE PHONE NOTIFICATIONS</button></div>'}
window.enablePush=async()=>{try{if(!('serviceWorker'in navigator)||!('PushManager'in window)||!('Notification'in window))throw Error('Push notifications are not supported on this browser.');const permission=await Notification.requestPermission();if(permission!=='granted')throw Error('Notification permission was not granted.');const reg=await navigator.serviceWorker.register('/sw.js');await navigator.serviceWorker.ready;let sub=await reg.pushManager.getSubscription();if(!sub)sub=await reg.pushManager.subscribe({userVisibleOnly:true,applicationServerKey:b64u8(WENIK_VAPID_PUBLIC_KEY)});const prof=await rpc('customer_my_profile');const customer=prof?.[0];if(!customer?.customer_id)throw Error('Customer profile not found.');const j=sub.toJSON();const row={customer_id:customer.customer_id,endpoint:j.endpoint,p256dh:j.keys?.p256dh,auth:j.keys?.auth,user_agent:navigator.userAgent,is_active:true,updated_at:new Date().toISOString()};const{error}=await sb.from('push_subscriptions').upsert(row,{onConflict:'endpoint'});if(error)throw error;alert('Phone notifications are ON for WENIK.');await loadMe()}catch(e){alert(e.message||String(e))}};
"""
if 'WENIK_VAPID_PUBLIC_KEY' not in s:
    if anchor not in s: raise SystemExit('GUARD FAILED: loadMe anchor not found')
    s=s.replace(anchor,helper+'\n'+anchor,1)
old="""  $('inbox').innerHTML=(i||[]).map(x=>'<div class=\"card '+(!x.seen_at?'unread':'')+'\" data-message=\"'+x.message_id+'\"><div class=\"row\"><b>'+esc(x.title)+'</b>'+(!x.seen_at?'<span class=\"badge\">NEW</span>':'')+'</div><div class=\"muted\">'+esc(x.body)+'</div></div>').join('')||'<div class=\"card muted\">No notifications.</div>';"""
new="""  const pushCard=await pushStateCard().catch(()=>'<div class=\"card muted\">Phone notifications unavailable.</div>');
  $('inbox').innerHTML=pushCard+((i||[]).map(x=>'<div class=\"card '+(!x.seen_at?'unread':'')+'\" data-message=\"'+x.message_id+'\"><div class=\"row\"><b>'+esc(x.title)+'</b>'+(!x.seen_at?'<span class=\"badge\">NEW</span>':'')+'</div><div class=\"muted\">'+esc(x.body)+'</div></div>').join('')||'<div class=\"card muted\">No notifications.</div>');"""
if old not in s: raise SystemExit('GUARD FAILED: inbox renderer not found')
s=s.replace(old,new,1)
if s.count('WENIK_VAPID_PUBLIC_KEY')!=2: raise SystemExit('GUARD FAILED: unexpected VAPID marker count')
p.write_text(s)
