from pathlib import Path

p = Path('partner.html')
s = p.read_text(encoding='utf-8')
old = "input.type=showing?'password'*'text';"
new = "input.type=showing?'password':'text';"
count = s.count(old)
if count != 1:
    raise SystemExit(f'Expected exactly one password-eye syntax target, found {count}')
p.write_text(s.replace(old, new, 1), encoding='utf-8')
print('Fixed exactly one staging partner password-eye syntax error')
