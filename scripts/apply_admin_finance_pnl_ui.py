from pathlib import Path
p=Path('admin.html')
s=p.read_text(encoding='utf-8')
MARK='<!-- WENIK FINANCE PNL UI V1 -->'
if MARK in s:
    print('Finance P&L UI already present'); raise SystemExit(0)
old='<button id="superTab" class="tab hidden" data-panel="super">SUPER ADMIN</button>'
assert old in s
new='<button id="financeTab" class="tab hidden" data-panel="finance">FINANCE · P&L</button>'+old
s=s.replace(old,new,1)
anchor='<section id="super" class="panel">'
assert anchor in s
block='''<!-- WENIK FINANCE PNL UI V1 -->
<section id="finance" class="panel">
  <div class="card"><div class="row"><div><h2>Finance · P&amp;L</h2><div class="muted">WENIK operating revenue and expenses. Gifts and cashback balances stay separate.</div></div><span class="pill">SUPER ADMIN</span></div></div>
  <div class="card">
    <div class="two"><select id="pnlPeriod" class="field"><option value="month">This month</option><option value="previous_month">Previous month</option><option value="ytd">Year to date</option><option value="year">This year</option></select><select id="pnlCurrency" class="field"><option value="USD">USD</option><option value="LBP">LBP</option></select></div>
    <button id="refreshPnl" class="btn">REFRESH P&amp;L</button><div id="pnlStatus" class="status"></div>
  </div>
  <div id="pnlSummary" class="grid"></div>
  <div class="cols"><div><h2>Revenue</h2><div id="pnlRevenue"></div></div><div><h2>Expenses</h2><div id="pnlExpenses"></div></div></div>
  <div class="card"><h3>Add finance entry</h3><div class="muted">Use only WENIK operating income/costs. Do not enter gift face value or customer cashback balance here.</div><div class="two"><select id="financeType" class="field"><option value="revenue">Revenue</option><option value="expense">Expense</option></select><select id="financeCurrency" class="field"><option value="USD">USD</option><option value="LBP">LBP</option></select></div><select id="financeCategory" class="field"></select><input id="financeAmount" class="field" type="number" min="0" step="0.01" placeholder="Amount"><input id="financeNotes" class="field" placeholder="Note / reference"><button id="addFinanceEntry" class="btn">ADD ENTRY</button><div id="financeEntryStatus" class="status"></div></div>
</section>
'''
s=s.replace(anchor,block+anchor,1)
# Super-admin visibility hook
needle="$('superTab').classList.remove('hidden');"
assert needle in s
s=s.replace(needle,needle+"$('financeTab').classList.remove('hidden');",1)
# JS helpers before auth boot marker
js_anchor='async function boot(){'
assert js_anchor in s
js=r'''const FINANCE_CATS={revenue:['Bronze','Silver','Gold','Advertising','Cashback fees','WENIK+','IZA','Other operating revenue'],expense:['Payroll / Team','Marketing','Development / Maintenance','Hosting / Database / Tech','SMS / Communications','Support','Accounting / Admin','Taxes / Reserve','Other operating costs']};
function financeRange(period){const n=new Date(), y=n.getFullYear(),m=n.getMonth();let a,b;if(period==='previous_month'){a=new Date(y,m-1,1);b=new Date(y,m,1)}else if(period==='ytd'||period==='year'){a=new Date(y,0,1);b=new Date(y+1,0,1)}else{a=new Date(y,m,1);b=new Date(y,m+1,1)}return[a.toISOString(),b.toISOString()]}
function fillFinanceCats(){const t=$('financeType').value;$('financeCategory').innerHTML=FINANCE_CATS[t].map(x=>'<option>'+x+'</option>').join('')}
async function loadPnl(){try{$('pnlStatus').textContent='Loading…';const [a,b]=financeRange($('pnlPeriod').value),cur=$('pnlCurrency').value;const x=(await rpc('admin_finance_pnl',{p_from:a,p_to:b,p_currency:cur}))?.[0]||{};const rows=await rpc('admin_finance_breakdown',{p_from:a,p_to:b,p_currency:cur});$('pnlSummary').innerHTML=[['Gross Revenue',x.gross_revenue||0],['Total Expenses',x.total_expenses||0],['Net Profit',x.net_profit||0]].map(v=>'<div class="metric"><span class="muted">'+v[0]+'</span><b>'+cur+' '+Number(v[1]).toLocaleString()+'</b></div>').join('');for(const typ of ['revenue','expense']){const el=$(typ==='revenue'?'pnlRevenue':'pnlExpenses'),r=(rows||[]).filter(z=>z.entry_type===typ);el.innerHTML=r.map(z=>'<div class="card row"><span>'+esc(z.category)+'</span><b>'+cur+' '+Number(z.amount).toLocaleString()+'</b></div>').join('')||'<div class="card muted">No entries.</div>'}$('pnlStatus').textContent=''}catch(e){$('pnlStatus').textContent=e.message}}
async function addFinance(){try{$('financeEntryStatus').textContent='Saving…';await rpc('admin_add_finance_transaction',{p_occurred_at:new Date().toISOString(),p_entry_type:$('financeType').value,p_category:$('financeCategory').value,p_amount:Number($('financeAmount').value||0),p_currency:$('financeCurrency').value,p_notes:$('financeNotes').value.trim()||null});$('financeAmount').value='';$('financeNotes').value='';$('financeEntryStatus').textContent='Saved';await loadPnl()}catch(e){$('financeEntryStatus').textContent=e.message}}
$('financeType').addEventListener('change',fillFinanceCats);$('refreshPnl').addEventListener('click',loadPnl);$('addFinanceEntry').addEventListener('click',addFinance);fillFinanceCats();
'''
s=s.replace(js_anchor,js+js_anchor,1)
p.write_text(s,encoding='utf-8')
print('Finance P&L UI patched')
