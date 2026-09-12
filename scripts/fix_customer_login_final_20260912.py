from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = """$('login').onclick=async()=>{
  const p=ph($('loginPhone').value),password=$('loginPassword').value;
  if(!$('loginPhone').value.trim()||!password)return $('msg').textContent='Mobile and password are required.';
  $('msg').textContent='Signing in…';
  const{error}=await sb.auth.signInWithPassword({phone:p,password});
  if(error)return $('msg').textContent=error.message;
  enter()
};
$('loginPassword').addEventListener('keydown',e=>{if(e.key==='Enter')$('login').click()});"""

new = """document.querySelectorAll('button#login').forEach(btn=>{
  btn.onclick=async()=>{
    const form=btn.closest('#loginForm')||document;
    const phoneInput=form.querySelector('#loginPhone');
    const passInput=form.querySelector('#loginPassword');
    const msg=[...document.querySelectorAll('#msg')].find(el=>el.offsetParent!==null)||document.querySelector('#msg');
    const raw=phoneInput?.value?.trim()||'';
    const password=passInput?.value||'';
    if(!raw||!password){if(msg)msg.textContent='Mobile and password are required.';return;}
    if(msg)msg.textContent='Signing in…';
    const{error}=await sb.auth.signInWithPassword({phone:ph(raw),password});
    if(error){if(msg)msg.textContent=error.message;return;}
    enter();
  };
});
document.querySelectorAll('#loginPassword').forEach(input=>input.addEventListener('keydown',e=>{
  if(e.key==='Enter')input.closest('#loginForm')?.querySelector('button#login')?.click();
}));"""

if old not in s:
    raise SystemExit('Original customer login block not found; refusing to touch anything else')
s = s.replace(old, new, 1)

start='<!-- WENIK VISIBLE CUSTOMER LOGIN BRIDGE 20260912 START -->'
end='<!-- WENIK VISIBLE CUSTOMER LOGIN BRIDGE 20260912 END -->'
if start in s and end in s:
    a=s.index(start)
    b=s.index(end,a)+len(end)
    s=s[:a]+s[b:]

p.write_text(s,encoding='utf-8')
