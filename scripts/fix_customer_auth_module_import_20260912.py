from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="import QRCode from'https://esm.sh/qrcode@1.5.4';"
if s.count(old)!=1:
    raise SystemExit(f'Expected exactly one QRCode static import, found {s.count(old)}')
s=s.replace(old,"",1)
old_load="async function loadQr(){\n  const r=(await rpc('customer_refresh_qr'))?.[0];"
new_load="async function loadQr(){\n  const {default:QRCode}=await import('https://esm.sh/qrcode@1.5.4');\n  const r=(await rpc('customer_refresh_qr'))?.[0];"
if s.count(old_load)!=1:
    raise SystemExit(f'Expected exactly one loadQr marker, found {s.count(old_load)}')
s=s.replace(old_load,new_load,1)
p.write_text(s,encoding='utf-8')
print('Moved QRCode import to loadQr only; customer auth module can initialize independently.')
