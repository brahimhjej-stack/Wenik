from pathlib import Path

p=Path('admin.html')
s=p.read_text(encoding='utf-8')
old='''  <div class="card" id="missingPartnerAccessCard"><h2>Missing Partner Access</h2><div class="muted">Create Login access for the 9 Partners that were added as directory data only. Existing Partner data stays unchanged.</div><button id="createMissingPartnerAccessBtn" class="btn">CREATE ACCESS FOR 9 PARTNERS</button><div id="missingPartnerAccessStatus" class="status"></div><div id="missingPartnerAccessResults"></div></div>'''
new='''  <div class="card" id="missingPartnerAccessCard"><h2>Partner Access Created</h2><div class="muted">All 9 directory Partners now have active Login access. Use Partner Access above to reset any Partner password.</div><div id="missingPartnerAccessStatus" class="status good">9 of 9 Partner access accounts active.</div><div id="missingPartnerAccessResults"></div></div>'''
if s.count(old)!=1:
    raise SystemExit(f'Expected exact card once, found {s.count(old)}')
s=s.replace(old,new,1)
start=s.index('// WENIK MISSING PARTNER ACCESS BULK V1')
end=s.index("$('logoutBtn').onclick",start)
replacement='''// WENIK EXISTING PARTNER ACCESS STATUS V2\nconst WENIK_EXISTING_PARTNERS=[\n  ['Farouj Chahine','faroujchahine'],['Kashmir Wears','kashmirwears'],["L'Atelier de Vera",'atelierdevera'],['Labneh w Jebneh','labnehwjebneh'],['Ghazi Issa Electrical','ghaziissaelectrical'],['Jaber Jewelry','jaberjewelry'],['Lilandi Coffee','lilandicoffee'],['Eat Vite','eatvite'],['Salon Mohammad Sabah','salonmohammadsabah']\n];\n$('missingPartnerAccessResults').innerHTML=WENIK_EXISTING_PARTNERS.map(r=>'<div class="card" style="padding:14px"><b>'+esc(r[0])+'</b><div class="muted">Username: '+esc(r[1])+'</div><div class="good">Access active · Reset password above when needed.</div></div>').join('');\n'''
s=s[:start]+replacement+s[end:]
p.write_text(s,encoding='utf-8')
print('Patched only existing Partner Access status UI in admin.html')
