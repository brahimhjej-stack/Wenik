from pathlib import Path
p=Path('partner.html')
s=p.read_text(encoding='utf-8')
start=s.index('  <!-- WENIK PARTNER GIFTS UI -->')
end=s.index('  <button id="logoutBtn"',start)
s=s[:start]+s[end:]
s=s.replace('await Promise.all([loadGifts(),loadMedia()])','await loadMedia()')
js_start=s.index('\nfunction giftEsc(v)')
js_end=s.index("\n$('logoutBtn').onclick",js_start)
s=s[:js_start]+s[js_end:]
assert 'partner_submit_gift' not in s
assert 'partner_update_gift' not in s
assert 'partner_delete_gift' not in s
assert 'partner_my_gifts' not in s
assert 'giftsCard' not in s
assert 'loadMedia()' in s
p.write_text(s,encoding='utf-8')
print('Removed Partner gift management; Admin remains responsible for contracted gifts.')
