from pathlib import Path
p=Path('admin.html')
s=p.read_text(encoding='utf-8')

# Finance P&L panel
if '<!-- WENIK FINANCE PNL UI V1 -->' not in s:
    old='<button id="superTab" class="tab hidden" data-panel="super">SUPER ADMIN</button>'
    assert old in s
    s=s.replace(old,'<button id="financeTab" class="tab hidden" data-panel="finance">FINANCE · P&L</button>'+old,1)
    anchor='<section id="super" class="panel">'
    assert anchor in s
    block='''<!-- WENIK FINANCE PNL UI V1 -->
<section id="finance" class="panel">
<div class="card"><div class="row"><div><h2>Finance · P&amp;L</h2><div class="muted">WENIK operating revenue and expenses. Confirmed Partner subscription payments are counted automatically. Gifts and customer cashback balances stay separate.</div></div><span class="pill">SUPER ADMIN</span></div></div>
<div class="card"><div class="two"><select id="pnlPeriod" class="field"><option value="month">This month</option><option value="previous_month">Previous month</option><option value="ytd">Year to date</option><option value="year">This year</option></select><select id="pnlCurrency" class="field"><option value="USD">USD</option><option value="LBP">LBP</option></select></div><button id="refreshPnl" class="btn">REFRESH P&amp;L</button><div id="pnlStatus" class="status"></div></div>
<div id="pnlSummary" class="grid"></div><div class="cols"><div><h2>Revenue</h2><div id="pnlRevenue"></div></div><div><h2>Expenses</h2><div id="pnlExpenses"></div></div></div>
<!-- WENIK FINANCE LEDGER UI V1 -->
<div class="card"><div class="row"><div><h3>Finance Ledger · Audit Trail</h3><div class="muted">Permanent finance history. Entries are never deleted; corrections use a reversal.</div></div><button id="refreshFinanceLedger" class="btn secondary">REFRESH</button></div><div id="financeLedgerStatus" class="status"></div><div id="financeLedgerList"><div class="card muted">No finance entries loaded.</div></div></div>
<div class="card"><h3>Add finance entry</h3><div class="muted">Manual operating entries only. Do not re-enter Partner subscription payments; confirmed payments are automatic. Gift face value and customer cashback balance are excluded.</div><div class="two"><select id="financeType" class="field"><option value="revenue">Revenue</option><option value="expense">Expense</option></select><select id="financeCurrency" class="field"><option value="USD">USD</option><option value="LBP">LBP</option></select></div><select id="financeCategory" class="field"></select><input id="financeAmount" class="field" type="number" min="0" step="0.01" placeholder="Amount"><input id="financeNotes" class="field" placeholder="Note / reference"><button id="addFinanceEntry" class="btn">ADD ENTRY</button><div id="financeEntryStatus" class="status"></div></div>
</section>
'''
    s=s.replace(anchor,block+anchor,1)
    tabneedle="if(b.dataset.panel==='super')loadAdmins()"
    assert tabneedle in s
    s=s.replace(tabneedle,"if(b.dataset.panel==='finance'){loadPnl();loadFinanceLedger();}"+tabneedle,1)
    vis="if(profile.role==='super_admin')$('superTab').classList.remove('hidden');"
    assert vis in s
    s=s.replace(vis,"if(profile.role==='super_admin'){$('superTab').classList.remove('hidden');$('financeTab').classList.remove('hidden');}",1)
    js_anchor="$('loginBtn').onclick=async()=>"
    assert js_anchor in s
    js=r'''/* WENIK FINANCE PNL UI V2 */
const FINANCE_CATS={revenue:['Advertising','Cashback fees','WENIK+','IZA','Other operating revenue'],expense:['Payroll / Team','Marketing','Development / Maintenance','Hosting / Database / Tech','SMS / Communications','Support','Accounting / Admin','Taxes / Reserve','Other operating costs']};
function financeRange(period){const n=new Date(),y=n.getFullYear(),m=n.getMonth();let a,b;if(period==='previous_month'){a=new Date(y,m-1,1);b=new Date(y,m,1)}else if(period==='ytd'){a=new Date(y,0,1);b=new Date()}else if(period==='year'){a=new Date(y,0,1);b=new Date(y+1,0,1)}else{a=new Date(y,m,1);b=new Date(y,m+1,1)}return[a.toISOString(),b.toISOString()]}
function fillFinanceCats(){const t=$('financeType').value;$('financeCategory').innerHTML=FINANCE_CATS[t].map(x=>'<option>'+esc(x)+'</option>').join('')}
async function loadPnl(){try{$('pnlStatus').className='status';$('pnlStatus').textContent='Loading…';const [a,b]=financeRange($('pnlPeriod').value),cur=$('pnlCurrency').value;const x=(await rpc('admin_finance_pnl',{p_from:a,p_to:b,p_currency:cur}))?.[0]||{};const rows=await rpc('admin_finance_breakdown',{p_from:a,p_to:b,p_currency:cur});$('pnlSummary').innerHTML=[['Gross Revenue',x.gross_revenue||0],['Operating Expenses',x.operating_expenses??x.total_expenses??0],['Taxes / Reserve',x.taxes_reserve||0],['Net Profit',x.net_profit||0]].map(v=>'<div class="metric"><span class="muted">'+v[0]+'</span><b>'+cur+' '+Number(v[1]).toLocaleString()+'</b></div>').join('');for(const typ of ['revenue','expense']){const el=$(typ==='revenue'?'pnlRevenue':'pnlExpenses'),r=(rows||[]).filter(z=>z.entry_type===typ);el.innerHTML=r.map(z=>'<div class="card row"><span>'+esc(z.category)+'</span><b>'+cur+' '+Number(z.amount).toLocaleString()+'</b></div>').join('')||'<div class="card muted">No entries.</div>'}$('pnlStatus').textContent=''}catch(e){setStatus('pnlStatus',String(e?.message||e))}}
async function addFinance(){try{const amt=Number($('financeAmount').value);if(!Number.isFinite(amt)||amt<=0)throw Error('Enter an amount greater than zero.');$('financeEntryStatus').textContent='Saving…';await rpc('admin_add_finance_transaction',{p_occurred_at:new Date().toISOString(),p_entry_type:$('financeType').value,p_category:$('financeCategory').value,p_amount:amt,p_currency:$('financeCurrency').value,p_partner_id:null,p_source_type:null,p_source_id:null,p_notes:$('financeNotes').value.trim()||null});$('financeAmount').value='';$('financeNotes').value='';setStatus('financeEntryStatus','Saved.',true);await Promise.all([loadPnl(),loadFinanceLedger()])}catch(e){setStatus('financeEntryStatus',e.message)}}
async function loadFinanceLedger(){try{const cur=$('pnlCurrency').value;const rows=await rpc('admin_finance_entries',{p_from:'2000-01-01T00:00:00.000Z',p_to:'2100-01-01T00:00:00.000Z',p_currency:cur,p_limit:100});$('financeLedgerList').innerHTML=(rows||[]).map(x=>{const status=x.reversal_of?'reversal':(x.is_reversed?'reversed':'posted');return '<div class="card"><div class="row"><div><b>'+esc(x.category||'Finance entry')+'</b><div class="muted">'+esc(x.entry_type||'')+' · '+esc(x.currency||cur)+' '+Number(x.amount||0).toLocaleString()+' · '+new Date(x.occurred_at).toLocaleString()+'</div>'+(x.notes?'<div class="muted">'+esc(x.notes)+'</div>':'')+'</div><span class="pill">'+esc(status.toUpperCase())+'</span></div>'+(status==='posted'?'<div class="actions"><button class="btn danger" onclick="reverseFinanceEntry(\''+x.id+'\')">REVERSE</button></div>':'')+'</div>'}).join('')||'<div class="card muted">No finance entries.</div>';$('financeLedgerStatus').textContent=''}catch(e){setStatus('financeLedgerStatus',String(e?.message||e))}}
window.reverseFinanceEntry=async id=>{const reason=prompt('Reason for reversal:');if(reason===null)return;if(!reason.trim()){alert('A reversal reason is required.');return}if(!confirm('Reverse this finance entry? The original entry will remain in history.'))return;try{await rpc('admin_reverse_finance_transaction',{p_transaction_id:id,p_reason:reason.trim()});await Promise.all([loadPnl(),loadFinanceLedger()])}catch(e){alert(e.message)}};
$('financeType').addEventListener('change',fillFinanceCats);$('refreshPnl').addEventListener('click',loadPnl);$('addFinanceEntry').addEventListener('click',addFinance);$('refreshFinanceLedger').addEventListener('click',loadFinanceLedger);fillFinanceCats();
'''
    s=s.replace(js_anchor,js+js_anchor,1)

# Align gift ownership copy with WENIK contract rule when legacy text exists.
s=s.replace('Confirm or reject gifts submitted by partners. Approved gifts are ready for WIN.','WENIK Admin manages contracted Partner gifts. Approved gifts are ready for WIN.',1)
s=s.replace('The Partner then logs in and completes business details, images and gifts. A 3-month FREE trial starts automatically.','The Partner then logs in and completes business details and images. WENIK Admin manages contracted gifts. A 3-month FREE trial starts automatically.',1)

assert 'FINANCE · P&L' in s
assert 'admin_finance_pnl' in s
assert 'admin_finance_entries' in s
assert 'admin_reverse_finance_transaction' in s
p.write_text(s,encoding='utf-8')
print('Production Finance P&L UI patched safely')
