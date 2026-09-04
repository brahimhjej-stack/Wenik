from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove only the abandoned social-auth experiment; preserve phone/password and all other customer code.
s=re.sub(r'\n?/\* WENIK SOCIAL LOGIN V1 \*/\n\.socialAuth\{.*?\.socialBtn:active\{transform:scale\(\.985\)\}\n?', '\n', s, count=1, flags=re.S)
s=re.sub(r'\n\s*<div class="socialAuth">.*?</div>\s*<div id="msg"', '\n    <div id="msg"', s, count=1, flags=re.S)
s=re.sub(r'\n\n/\* WENIK SOCIAL LOGIN V1 \*/\nasync function wenikSocialLogin\(provider\)\{.*?\n\}\n\$\(\'googleLogin\'\)\.onclick=.*?\n\$\(\'facebookLogin\'\)\.onclick=.*?\n', '\n', s, count=1, flags=re.S)
for forbidden in ['id="googleLogin"','id="facebookLogin"','function wenikSocialLogin','WENIK SOCIAL LOGIN V1']:
    assert forbidden not in s, forbidden
assert "id=\"loginPassword\"" in s
p.write_text(s,encoding='utf-8')
print('Removed abandoned social login UI; phone/password preserved')
