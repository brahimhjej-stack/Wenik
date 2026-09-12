from pathlib import Path

p=Path('partner.html')
s=p.read_text(encoding='utf-8')
marker='<!-- WENIK PARTNER LOGIN CLICK FIX V1 -->'
if marker not in s:
    patch=r'''\n<!-- WENIK PARTNER LOGIN CLICK FIX V1 -->
<script type="module">
import{createClient as _wenikCreateClient}from'https://esm.sh/@supabase/supabase-js@2';
const _wenikU='https://zkrnzwnbdoaqanqzznlw.supabase.co',_wenikK='sb_publishable_Q8pOXn-3YAUo_6OX6c2bKg_mLKH8O0k';
const _wenikSb=_wenikCreateClient(_wenikU,_wenikK);
const _wenik$=id=>document.getElementById(id);
async function _wenikPartnerLogin(ev){
  if(ev){ev.preventDefault();ev.stopImmediatePropagation();}
  const btn=_wenik$('loginBtn'),msg=_wenik$('loginMsg');
  try{
    const username=String(_wenik$('username')?.value||'').trim().toLowerCase();
    const password=String(_wenik$('password')?.value||'');
    if(!username||!password)throw Error('Enter username and password.');
    if(btn)btn.disabled=true;
    if(msg){msg.className='muted';msg.textContent='Signing in…';}
    const{data,error}=await _wenikSb.functions.invoke('partner-login',{body:{username,password}});
    if(error)throw error;
    if(data?.error)throw Error(data.error==='account_locked'?'Account temporarily locked. Try again later.':'Invalid username or password.');
    const r=await _wenikSb.auth.setSession({access_token:data.access_token,refresh_token:data.refresh_token});
    if(r.error)throw r.error;
    location.reload();
  }catch(e){
    if(msg){msg.className='error';msg.textContent=e?.message||'Login failed.';}
    if(btn)btn.disabled=false;
  }
}
const _wenikLoginBtn=_wenik$('loginBtn');
if(_wenikLoginBtn){
  _wenikLoginBtn.type='button';
  _wenikLoginBtn.addEventListener('click',_wenikPartnerLogin,true);
}
for(const id of ['username','password']){
  const el=_wenik$(id);
  if(el)el.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();_wenikPartnerLogin(e);}});
}
</script>
<!-- /WENIK PARTNER LOGIN CLICK FIX V1 -->'''
    pos=s.lower().rfind('</body>')
    if pos<0: raise SystemExit('partner.html missing </body>')
    s=s[:pos]+patch+'\n'+s[pos:]
    p.write_text(s,encoding='utf-8')
    print('partner login click fix applied')
else:
    print('partner login click fix already present')
