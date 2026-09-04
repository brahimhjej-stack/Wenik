from pathlib import Path
p=Path('admin.html')
s=p.read_text(encoding='utf-8')

old="const rows=await rpc('admin_finance_ledger',{p_currency:cur,p_limit:100});$('financeLedgerList').innerHTML=(rows||[]).map(x=>'<div class=\"card\"><div class=\"row\"><div><b>'+esc(x.category||'Finance entry')+'</b><div class=\"muted\">'+esc(x.entry_type||'')+' · '+esc(x.currency||cur)+' '+Number(x.amount||0).toLocaleString()+' · '+new Date(x.occurred_at).toLocaleString()+'</div>'+(x.notes?'<div class=\"muted\">'+esc(x.notes)+'</div>':'')+'</div><span class=\"pill\">'+esc(String(x.status||'posted').toUpperCase())+'</span></div>'+(x.status==='posted'?'<div class=\"actions\"><button class=\"btn danger\" onclick=\"reverseFinanceEntry(\\\''+x.id+'\\\')\">REVERSE</button></div>':'')+'</div>').join('')||'<div class=\"card muted\">No finance entries.</div>'"
new="const rows=await rpc('admin_finance_entries',{p_from:'2000-01-01T00:00:00.000Z',p_to:'2100-01-01T00:00:00.000Z',p_currency:cur,p_limit:100});$('financeLedgerList').innerHTML=(rows||[]).map(x=>{const status=x.reversal_of?'reversal':(x.is_reversed?'reversed':'posted');return '<div class=\"card\"><div class=\"row\"><div><b>'+esc(x.category||'Finance entry')+'</b><div class=\"muted\">'+esc(x.entry_type||'')+' · '+esc(x.currency||cur)+' '+Number(x.amount||0).toLocaleString()+' · '+new Date(x.occurred_at).toLocaleString()+'</div>'+(x.notes?'<div class=\"muted\">'+esc(x.notes)+'</div>':'')+'</div><span class=\"pill\">'+esc(status.toUpperCase())+'</span></div>'+(status==='posted'?'<div class=\"actions\"><button class=\"btn danger\" onclick=\"reverseFinanceEntry(\\\''+x.id+'\\\')\">REVERSE</button></div>':'')+'</div>'}).join('')||'<div class=\"card muted\">No finance entries.</div>'"
assert old in s, 'finance ledger anchor missing'
s=s.replace(old,new,1)
s=s.replace("/admin_finance_ledger|function .* does not exist|schema cache/i.test(msg)","/admin_finance_entries|function .* does not exist|schema cache/i.test(msg)",1)

s=s.replace('Confirm or reject gifts submitted by partners. Approved gifts are ready for WIN.','WENIK Admin manages contracted Partner gifts. Approved gifts are ready for WIN.',1)
s=s.replace('The Partner then logs in and completes business details, images and gifts. A 3-month FREE trial starts automatically.','The Partner then logs in and completes business details and images. WENIK Admin manages contracted gifts. A 3-month FREE trial starts automatically.',1)

assert "admin_finance_ledger" not in s
assert "rpc('admin_finance_entries'" in s
assert 'completes business details, images and gifts' not in s
assert 'gifts submitted by partners' not in s
p.write_text(s,encoding='utf-8')
print('Hardened Admin finance ledger contract and Partner gift ownership copy.')
