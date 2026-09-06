from pathlib import Path

# Admin: add Partner password reset UI and handler.
p=Path('admin.html')
s=p.read_text()
marker='<!-- WENIK ADMIN PARTNER PASSWORD RESET PREVIEW -->'
if marker not in s:
    anchor='''  <div class="card"><div class="row"><div><h2>Partner Subscriptions</h2><div class="muted">3 months FREE, then Manual or Whish payment.</div></div><button id="refreshSubscriptions" class="btn secondary" style="width:auto">REFRESH</button></div></div>'''
    block='''  <!-- WENIK ADMIN PARTNER PASSWORD RESET PREVIEW -->\n  <div class="card"><h2>Partner Access</h2><div class="muted">Reset a Partner password and clear any login lock. The Partner must change the temporary password after login.</div>\n    <input id="resetPartnerUsername" class="field" placeholder="Partner username" autocomplete="off">\n    <input id="resetPartnerPassword" class="field" type="password" minlength="10" placeholder="New temporary password · 10+ characters">\n    <button id="resetPartnerPasswordBtn" class="btn">RESET PASSWORD</button>\n    <div id="resetPartnerPasswordStatus" class="status"></div>\n  </div>\n'''
    if anchor not in s: raise SystemExit('ADMIN UI ANCHOR NOT FOUND')
    s=s.replace(anchor,block+anchor,1)

    js_anchor="$('refreshSubscriptions').onclick=loadSubscriptions;"
    js='''\n$('resetPartnerPasswordBtn').onclick=async()=>{\n  const username=$('resetPartnerUsername').value.trim().toLowerCase(),password=$('resetPartnerPassword').value;\n  if(!username)return setStatus('resetPartnerPasswordStatus','Enter Partner username.');\n  if(password.length<10||!/[A-Z]/.test(password)||!/[a-z]/.test(password)||!/[0-9]/.test(password))return setStatus('resetPartnerPasswordStatus','Password needs 10+ characters with uppercase, lowercase and a number.');\n  if(!confirm('Reset password for '+username+'?'))return;\n  $('resetPartnerPasswordBtn').disabled=true;setStatus('resetPartnerPasswordStatus','Resetting password...',true);\n  try{\n    const{data,error}=await sb.functions.invoke('admin-reset-partner-password',{body:{username,password}});\n    if(error)throw error;if(data?.error)throw Error(data.error);\n    $('resetPartnerPassword').value='';\n    setStatus('resetPartnerPasswordStatus','Password reset successfully. Login lock cleared.',true);\n  }catch(e){setStatus('resetPartnerPasswordStatus',e.message||'Could not reset password.')}\n  finally{$('resetPartnerPasswordBtn').disabled=false}\n};\n'''
    if js_anchor not in s: raise SystemExit('ADMIN JS ANCHOR NOT FOUND')
    s=s.replace(js_anchor,js_anchor+js,1)
    p.write_text(s)

# Customer: phone OTP forgot-password flow.
p=Path('index.html')
s=p.read_text()
marker='<!-- WENIK CUSTOMER FORGOT PASSWORD PREVIEW -->'
if marker not in s:
    anchor='''      <button id="login" class="btn">LOGIN</button>\n    </div>'''
    block='''      <button id="login" class="btn">LOGIN</button>\n      <!-- WENIK CUSTOMER FORGOT PASSWORD PREVIEW -->\n      <button id="forgotPassword" class="btn secondary" type="button">FORGOT PASSWORD?</button>\n    </div>'''
    if anchor not in s: raise SystemExit('CUSTOMER LOGIN UI ANCHOR NOT FOUND')
    s=s.replace(anchor,block,1)

    js_anchor="$('loginPassword').addEventListener('keydown',e=>{if(e.key==='Enter')$('login').click()});"
    js=r'''\n\nlet resetPhone='';\nfunction showResetOtp(phone){\n  resetPhone=phone;\n  $('joinForm').classList.add('hidden');$('loginForm').classList.add('hidden');\n  $('authTitle').textContent='RESET PASSWORD';\n  let box=$('resetPasswordBox');\n  if(!box){\n    box=document.createElement('div');box.id='resetPasswordBox';\n    box.innerHTML='<div class="muted" style="margin:8px 0 14px">We sent a 6-digit code to your mobile.</div><input id="resetOtpCode" class="field" inputmode="numeric" autocomplete="one-time-code" maxlength="6" placeholder="6-digit code"><button id="verifyResetOtpBtn" class="btn" type="button">VERIFY CODE</button><button id="resetBackBtn" class="btn secondary" type="button">BACK TO LOGIN</button><div id="resetMsg" class="muted" style="margin-top:10px"></div>';\n    $('loginForm').parentElement.appendChild(box);\n    $('resetOtpCode').addEventListener('input',e=>{e.target.value=e.target.value.replace(/\D/g,'').slice(0,6)});\n    $('verifyResetOtpBtn').onclick=verifyResetOtp;\n    $('resetBackBtn').onclick=()=>{box.classList.add('hidden');authMode('login')};\n  }\n  box.classList.remove('hidden');$('resetMsg').textContent='Code sent. Enter it below.';\n}\nasync function verifyResetOtp(){\n  const token=$('resetOtpCode').value.replace(/\D/g,'');\n  if(token.length!==6)return $('resetMsg').textContent='Enter the 6-digit code.';\n  $('verifyResetOtpBtn').disabled=true;$('resetMsg').textContent='Verifying...';\n  const{data,error}=await sb.auth.verifyOtp({phone:resetPhone,token,type:'sms'});\n  $('verifyResetOtpBtn').disabled=false;\n  if(error||!data?.session)return $('resetMsg').textContent=error?.message||'Could not verify code.';\n  const box=$('resetPasswordBox');\n  box.innerHTML='<div class="muted" style="margin:8px 0 14px">Choose your new password.</div><input id="resetNewPassword" class="field" type="password" minlength="6" autocomplete="new-password" placeholder="New password"><input id="resetConfirmPassword" class="field" type="password" minlength="6" autocomplete="new-password" placeholder="Confirm new password"><button id="saveResetPasswordBtn" class="btn" type="button">SAVE NEW PASSWORD</button><div id="resetMsg" class="muted" style="margin-top:10px"></div>';\n  $('saveResetPasswordBtn').onclick=saveCustomerResetPassword;\n}\nasync function saveCustomerResetPassword(){\n  const a=$('resetNewPassword').value,b=$('resetConfirmPassword').value;\n  if(a.length<6)return $('resetMsg').textContent='Password must be at least 6 characters.';\n  if(a!==b)return $('resetMsg').textContent='Passwords do not match.';\n  $('saveResetPasswordBtn').disabled=true;$('resetMsg').textContent='Saving new password...';\n  const{error}=await sb.auth.updateUser({password:a});\n  $('saveResetPasswordBtn').disabled=false;\n  if(error)return $('resetMsg').textContent=error.message;\n  $('resetMsg').textContent='Password changed ✓';setTimeout(()=>enter(),500);\n}\n$('forgotPassword').onclick=async()=>{\n  if(!$('loginPhone').value.trim())return $('msg').textContent='Enter your mobile number first.';\n  const phone=ph($('loginPhone').value);$('msg').textContent='Sending reset code...';$('forgotPassword').disabled=true;\n  const{error}=await sb.auth.signInWithOtp({phone,options:{shouldCreateUser:false}});\n  $('forgotPassword').disabled=false;\n  if(error)return $('msg').textContent=error.message;\n  $('msg').textContent='';showResetOtp(phone);\n};\n'''
    if js_anchor not in s: raise SystemExit('CUSTOMER LOGIN JS ANCHOR NOT FOUND')
    s=s.replace(js_anchor,js_anchor+js,1)
    p.write_text(s)

print('Partner reset + Customer forgot-password preview patch applied')
