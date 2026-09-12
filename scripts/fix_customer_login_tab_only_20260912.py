from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='<!-- WENIK CUSTOMER LOGIN TAB DIRECT BIND 20260912 -->'
if marker in s:
    raise SystemExit('already applied')
needle='  <section id="shell" class="hidden">'
if s.count(needle)!=1:
    raise SystemExit('unexpected auth/shell structure')
patch='''  <!-- WENIK CUSTOMER LOGIN TAB DIRECT BIND 20260912 -->\n  <script>\n  (function(){\n    const join=document.getElementById('joinTab');\n    const login=document.getElementById('loginTab');\n    const joinForm=document.getElementById('joinForm');\n    const loginForm=document.getElementById('loginForm');\n    const title=document.getElementById('authTitle');\n    const msg=document.getElementById('msg');\n    if(!join||!login||!joinForm||!loginForm||!title)return;\n    function setMode(mode){\n      const isJoin=mode==='join';\n      joinForm.classList.toggle('hidden',!isJoin);\n      loginForm.classList.toggle('hidden',isJoin);\n      join.classList.toggle('active',isJoin);\n      login.classList.toggle('active',!isJoin);\n      title.textContent=isJoin?'JOIN US':'LOGIN';\n      if(msg)msg.textContent='';\n    }\n    join.addEventListener('click',()=>setMode('join'));\n    login.addEventListener('click',()=>setMode('login'));\n  })();\n  </script>\n\n'''
s=s.replace(needle,patch+needle,1)
p.write_text(s,encoding='utf-8')
print('Patched only JOIN/LOGIN tab switching.')
