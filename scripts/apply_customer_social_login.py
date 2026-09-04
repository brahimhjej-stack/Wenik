from pathlib import Path
p=Path('index.html')
s=p.read_text()

css='''\n/* WENIK SOCIAL LOGIN V1 */\n.socialAuth{margin:14px 0 4px}.socialDivider{display:flex;align-items:center;gap:10px;color:#888;font-size:11px;margin:13px 0}.socialDivider:before,.socialDivider:after{content:"";height:1px;background:rgba(120,90,150,.18);flex:1}.socialBtns{display:grid;grid-template-columns:1fr 1fr;gap:8px}.socialBtn{border:1px solid rgba(120,90,150,.18);background:#fff;color:#17131e;border-radius:15px;padding:12px 8px;font-weight:900;box-shadow:0 8px 22px rgba(45,20,65,.06)}.socialBtn:active{transform:scale(.985)}\n'''
if '/* WENIK SOCIAL LOGIN V1 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

social='''\n    <div class="socialAuth">\n      <div class="socialDivider"><span>OR CONTINUE WITH</span></div>\n      <div class="socialBtns">\n        <button id="googleLogin" class="socialBtn" type="button">G&nbsp;&nbsp; GOOGLE</button>\n        <button id="facebookLogin" class="socialBtn" type="button">f&nbsp;&nbsp; FACEBOOK</button>\n      </div>\n      <div class="muted" style="margin-top:9px;text-align:center">Mobile verification is still required to activate WENIK.</div>\n    </div>\n'''
needle='    <div id="msg" class="muted" style="margin-top:10px"></div>'
if 'id="googleLogin"' not in s:
    s=s.replace(needle,social+needle,1)

js='''\n\n/* WENIK SOCIAL LOGIN V1 */\nasync function wenikSocialLogin(provider){\n  $('msg').textContent='Opening '+(provider==='google'?'Google':'Facebook')+'…';\n  const redirectTo=location.origin+location.pathname;\n  const {error}=await sb.auth.signInWithOAuth({provider,options:{redirectTo,queryParams:provider==='google'?{prompt:'select_account'}:{}}});\n  if(error)$('msg').textContent=error.message;\n}\n$('googleLogin').onclick=()=>wenikSocialLogin('google');\n$('facebookLogin').onclick=()=>wenikSocialLogin('facebook');\n'''
anchor="$('loginPassword').addEventListener('keydown',e=>{if(e.key==='Enter')$('login').click()});"
if 'function wenikSocialLogin' not in s:
    s=s.replace(anchor,anchor+js,1)

p.write_text(s)
