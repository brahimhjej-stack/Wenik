from pathlib import Path

p=Path('partner.html')
s=p.read_text(encoding='utf-8')
marker='<!-- WENIK PARTNER PROFILE AREA SYNC V1 -->'
if marker in s:
    raise SystemExit('already applied')
old='<input id="profileArea" class="field" placeholder="Area / city">'
new='''<!-- WENIK PARTNER PROFILE AREA SYNC V1 -->
    <select id="profileArea" class="field" aria-label="Area / city">
      <option value="">Select Area / City</option>
      <optgroup label="Beirut"><option>Beirut</option><option>Dahieh</option></optgroup>
      <optgroup label="Mount Lebanon"><option>Baabda</option><option>Metn</option><option>Jounieh</option><option>Jbeil</option><option>Aley</option><option>Chouf</option></optgroup>
      <optgroup label="South Lebanon"><option>Saida</option><option>Tyre</option><option>Jezzine</option></optgroup>
      <optgroup label="Nabatieh"><option>Nabatieh</option><option>Bint Jbeil</option><option>Marjayoun</option><option>Hasbaya</option></optgroup>
      <optgroup label="Bekaa"><option>Zahle</option><option>Baalbek</option><option>Hermel</option></optgroup>
      <optgroup label="North Lebanon"><option>Tripoli</option><option>Zgharta</option><option>Batroun</option><option>Bsharri</option><option>Akkar</option></optgroup>
    </select>'''
if old not in s:
    raise SystemExit('profileArea input not found; refusing unsafe patch')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Partner profile area selector synced with customer areas')
