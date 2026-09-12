from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

start='<!-- WENIK CUSTOMER LOGIN SELF-CONTAINED 20260912 START -->'
end='<!-- WENIK CUSTOMER LOGIN SELF-CONTAINED 20260912 END -->'
if start in s and end in s:
    a=s.index(start); b=s.index(end,a)+len(end); s=s[:a]+s[b:]

# Remove the previous bridge too, if present. Nothing else is touched.
old_start='<!-- WENIK VISIBLE CUSTOMER LOGIN BRIDGE 20260912 START -->'
old_end='<!-- WENIK VISIBLE CUSTOMER LOGIN BRIDGE 20260912 END -->'
if old_start in s and old_end in s:
    a=s.index(old_start); b=s.index(old_end,a)+len(old_end); s=s[:a]+s[b:]

block=r'''<!-- WENIK CUSTOMER LOGIN SELF-CONTAINED 20260912 START -->
<script type="module" id="wenikCustomerLoginSelfContained20260912">
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
const wenikLoginSb=createClient('https://zkrnzwnbdoaqanqzznlw.supabase.co','sb_publishable_Q8pOXn-3YAUo_6OX6c2bKg_mLKH8O0k');
const wenikLoginPhone=v=>{let d=String(v||'').replace(/\D/g,'');if(d.startsWith('961'))return'+'+d;if(d.startsWith('0'))d=d.slice(1);return'+961'+d};
function visibleLoginForm(){
  const forms=[...document.querySelectorAll('#loginForm')];
  return forms.find(f=>!f.classList.contains('hidden')&&f.offsetParent!==null)||forms.find(f=>!f.classList.contains('hidden'))||forms[0]||null;
}
function visibleMsg(){return [...document.querySelectorAll('#msg')].find(m=>m.offsetParent!==null)||document.querySelector('#msg')}
async function runCustomerLogin(btn){
  const form=btn.closest('#loginForm')||visibleLoginForm();
  if(!form)return;
  const phone=form.querySelector('#loginPhone');
  const pass=form.querySelector('#loginPassword');
  const msg=visibleMsg();
  const raw=(phone?.value||'').trim();
  const password=pass?.value||'';
  if(!raw||!password){if(msg)msg.textContent='Mobile and password are required.';return;}
  btn.disabled=true;
  if(msg)msg.textContent='Signing in…';
  try{
    const {error}=await wenikLoginSb.auth.signInWithPassword({phone:wenikLoginPhone(raw),password});
    if(error)throw error;
    location.reload();
  }catch(err){
    if(msg)msg.textContent=err?.message||'Login failed.';
    btn.disabled=false;
  }
}
document.addEventListener('click',e=>{
  const btn=e.target.closest('button#login');
  if(!btn)return;
  const form=btn.closest('#loginForm');
  if(!form)return;
  e.preventDefault();
  e.stopImmediatePropagation();
  runCustomerLogin(btn);
},true);
document.addEventListener('keydown',e=>{
  if(e.key!=='Enter'||!e.target.matches('#loginPassword'))return;
  const form=e.target.closest('#loginForm');
  const btn=form?.querySelector('button#login');
  if(!btn)return;
  e.preventDefault();
  runCustomerLogin(btn);
},true);
</script>
<!-- WENIK CUSTOMER LOGIN SELF-CONTAINED 20260912 END -->'''

if '</body>' not in s:
    raise SystemExit('No body close; refusing to change anything')
s=s.replace('</body>',block+'\n</body>',1)
p.write_text(s,encoding='utf-8')
