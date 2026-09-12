from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
start = '<!-- WENIK CUSTOMER LOGIN BUTTON FIX 20260912 START -->'
end = '<!-- WENIK CUSTOMER LOGIN BUTTON FIX 20260912 END -->'
block = r'''<!-- WENIK CUSTOMER LOGIN BUTTON FIX 20260912 START -->
<script type="module">
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
const U='https://zkrnzwnbdoaqanqzznlw.supabase.co',K='sb_publishable_Q8pOXn-3YAUo_6OX6c2bKg_mLKH8O0k';
const customerLoginSb=createClient(U,K);
function wenikCustomerPhone(v){
  let d=String(v||'').replace(/\D/g,'');
  if(d.startsWith('961')) return '+'+d;
  if(d.startsWith('0')) d=d.slice(1);
  return '+961'+d;
}
function visibleCustomerLoginForm(){
  return [...document.querySelectorAll('#loginForm')].find(el=>!el.classList.contains('hidden') && el.offsetParent!==null)
      || [...document.querySelectorAll('#loginForm')].find(el=>!el.classList.contains('hidden'))
      || document.querySelector('#loginForm');
}
document.addEventListener('click', async (e)=>{
  const btn=e.target.closest('button#login');
  if(!btn) return;
  e.preventDefault();
  e.stopImmediatePropagation();
  const form=btn.closest('#loginForm') || visibleCustomerLoginForm();
  if(!form) return;
  const phoneInput=form.querySelector('#loginPhone');
  const passInput=form.querySelector('#loginPassword');
  const msg=[...document.querySelectorAll('#msg')].find(el=>el.offsetParent!==null) || document.querySelector('#msg');
  const raw=phoneInput?.value?.trim()||'';
  const password=passInput?.value||'';
  if(!raw||!password){if(msg)msg.textContent='Mobile and password are required.';return;}
  btn.disabled=true;
  if(msg)msg.textContent='Signing in…';
  try{
    const {error}=await customerLoginSb.auth.signInWithPassword({phone:wenikCustomerPhone(raw),password});
    if(error) throw error;
    location.reload();
  }catch(err){
    if(msg)msg.textContent=err?.message||'Login failed.';
    btn.disabled=false;
  }
}, true);
</script>
<!-- WENIK CUSTOMER LOGIN BUTTON FIX 20260912 END -->'''
if start in s and end in s:
    a=s.index(start); b=s.index(end,a)+len(end); s=s[:a]+block+s[b:]
else:
    s=s.replace('</body>', block+'\n</body>')
p.write_text(s,encoding='utf-8')
