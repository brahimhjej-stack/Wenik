from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old_import="import QRCode from'https://esm.sh/qrcode@1.5.4';\n"
old_qr="  $('qrImage').src=await QRCode.toDataURL(String(r.qr_token),{width:360,margin:1});"
new_qr="  const{default:QRCode}=await import('https://esm.sh/qrcode@1.5.4');\n  $('qrImage').src=await QRCode.toDataURL(String(r.qr_token),{width:360,margin:1});"
if s.count(old_import)!=1:
    raise SystemExit('Expected exactly one static QRCode import')
if s.count(old_qr)!=1:
    raise SystemExit('Expected exactly one QRCode usage')
new=s.replace(old_import,'',1).replace(old_qr,new_qr,1)
if new==s:
    raise SystemExit('No change')
p.write_text(new,encoding='utf-8')
print('Moved QRCode import inside loadQr only; customer auth module can initialize independently.')