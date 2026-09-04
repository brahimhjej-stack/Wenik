from pathlib import Path
p=Path('partner.html')
s=p.read_text(encoding='utf-8')
if 'function escHtml(v)' not in s:
    anchor="async function loadMedia(){"
    helper="function escHtml(v){return String(v??'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]))}\n"
    assert anchor in s, 'loadMedia anchor missing'
    s=s.replace(anchor,helper+anchor,1)
s=s.replace('giftEsc(a.image_url)','escHtml(a.image_url)').replace('giftEsc(String(a.approval_status||\'pending\').toUpperCase())','escHtml(String(a.approval_status||\'pending\').toUpperCase())')
assert 'giftEsc(' not in s
assert 'function escHtml(v)' in s
p.write_text(s,encoding='utf-8')
print('Fixed Partner media escaping helper after gift-management removal.')
