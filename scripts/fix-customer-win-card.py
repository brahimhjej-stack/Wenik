from pathlib import Path
p=Path('index.html')
s=p.read_text()
old="$('wins').innerHTML=(w||[]).map(x=>'<div class=\"card\"><div class=\"eyebrow\">YOUR WIN</div><h3>'+esc(x.prize_title||x.title||'Prize')+'</h3></div>').join('')||'<div class=\"card muted\">No wins yet.</div>';"
new="$('wins').innerHTML=(w||[]).map(x=>'<div class=\"card\"><div class=\"eyebrow\">YOUR WIN</div><h3>🎉 '+esc(x.prize_name||'Prize')+'</h3><div class=\"muted\">Congratulations! You won with WENIK.</div></div>').join('')||'<div class=\"card muted\">No wins yet.</div>';"
if old not in s: raise SystemExit('GUARD FAILED: WIN card line not found')
s2=s.replace(old,new,1)
if s2.count("x.prize_name||'Prize'")!=1: raise SystemExit('GUARD FAILED: prize_name replacement count')
p.write_text(s2)
