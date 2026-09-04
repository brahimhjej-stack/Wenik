from pathlib import Path
p=Path('admin.html')
s=p.read_text(encoding='utf-8')
MARK='/* WENIK FINANCE PNL UI V2 */'
if MARK in s:
    print('Finance P&L UI V2 already present'); raise SystemExit(0)

old_note='<div class="card"><div class="row"><div><h2>Finance · P&amp;L</h2><div class="muted">WENIK operating revenue and expenses. Gifts and cashback balances stay separate.</div></div><span class="pill">SUPER ADMIN</span></div></div>'
new_note='<div class="card"><div class="row"><div><h2>Finance · P&amp;L</h2><div class="muted">WENIK operating revenue and expenses. Confirmed Partner subscription payments are counted automatically. Gifts and customer cashback balances stay separate.</div></div><span class="pill">SUPER ADMIN</span></div></div>'
assert old_note in s
s=s.replace(old_note,new_note,1)

old_add='<div class="card"><h3>Add finance entry</h3><div class="muted">Operating entries only. Gift face value and customer cashback balance are excluded.</div>'
new_add='<div class="card"><h3>Add finance entry</h3><div class="muted">Manual operating entries only. Do not re-enter Partner subscription payments; confirmed payments are automatic. Gift face value and customer cashback balance are excluded.</div>'
assert old_add in s
s=s.replace(old_add,new_add,1)

old_cats="const FINANCE_CATS={revenue:['Bronze','Silver','Gold','Advertising','Cashback fees','WENIK+','IZA','Other operating revenue'],expense:['Payroll / Team','Marketing','Development / Maintenance','Hosting / Database / Tech','SMS / Communications','Support','Accounting / Admin','Taxes / Reserve','Other operating costs']};"
new_cats="/* WENIK FINANCE PNL UI V2 */\nconst FINANCE_CATS={revenue:['Advertising','Cashback fees','WENIK+','IZA','Other operating revenue'],expense:['Payroll / Team','Marketing','Development / Maintenance','Hosting / Database / Tech','SMS / Communications','Support','Accounting / Admin','Taxes / Reserve','Other operating costs']};"
assert old_cats in s
s=s.replace(old_cats,new_cats,1)

old_load="async function loadPnl(){try{$('pnlStatus').textContent='Loading…';const [a,b]=financeRange($('pnlPeriod').value),cur=$('pnlCurrency').value;const x=(await rpc('admin_finance_pnl',{p_from:a,p_to:b,p_currency:cur}))?.[0]||{};const rows=await rpc('admin_finance_breakdown',{p_from:a,p_to:b,p_currency:cur});$('pnlSummary').innerHTML=[['Gross Revenue',x.gross_revenue||0],['Total Expenses',x.total_expenses||0],['Net Profit',x.net_profit||0]].map(v=>'<div class=\"metric\"><span class=\"muted\">'+v[0]+'</span><b>'+cur+' '+Number(v[1]).toLocaleString()+'</b></div>').join('');for(const typ of ['revenue','expense']){const el=$(typ==='revenue'?'pnlRevenue':'pnlExpenses'),r=(rows||[]).filter(z=>z.entry_type===typ);el.innerHTML=r.map(z=>'<div class=\"card row\"><span>'+esc(z.category)+'</span><b>'+cur+' '+Number(z.amount).toLocaleString()+'</b></div>').join('')||'<div class=\"card muted\">No entries.</div>'}$('pnlStatus').textContent=''}catch(e){setStatus('pnlStatus',e.message)}}"
new_load="async function loadPnl(){try{$('pnlStatus').className='status';$('pnlStatus').textContent='Loading…';const [a,b]=financeRange($('pnlPeriod').value),cur=$('pnlCurrency').value;const x=(await rpc('admin_finance_pnl',{p_from:a,p_to:b,p_currency:cur}))?.[0]||{};const rows=await rpc('admin_finance_breakdown',{p_from:a,p_to:b,p_currency:cur});$('pnlSummary').innerHTML=[['Gross Revenue',x.gross_revenue||0],['Operating Expenses',x.operating_expenses??x.total_expenses??0],['Taxes / Reserve',x.taxes_reserve||0],['Net Profit',x.net_profit||0]].map(v=>'<div class=\"metric\"><span class=\"muted\">'+v[0]+'</span><b>'+cur+' '+Number(v[1]).toLocaleString()+'</b></div>').join('');for(const typ of ['revenue','expense']){const el=$(typ==='revenue'?'pnlRevenue':'pnlExpenses'),r=(rows||[]).filter(z=>z.entry_type===typ);el.innerHTML=r.map(z=>'<div class=\"card row\"><span>'+esc(z.category)+'</span><b>'+cur+' '+Number(z.amount).toLocaleString()+'</b></div>').join('')||'<div class=\"card muted\">No entries.</div>'}$('pnlStatus').textContent=''}catch(e){const msg=String(e?.message||e);if(/admin_finance_pnl|admin_finance_breakdown|function .* does not exist|schema cache/i.test(msg)){setStatus('pnlStatus','Finance backend is prepared but not enabled on Production yet. Preview UI is safe; no accounting data was changed.')}else setStatus('pnlStatus',msg)}}"
assert old_load in s
s=s.replace(old_load,new_load,1)

p.write_text(s,encoding='utf-8')
print('Finance P&L UI V2 patched safely')
