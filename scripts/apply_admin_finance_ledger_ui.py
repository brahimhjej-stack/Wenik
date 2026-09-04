from pathlib import Path
p=Path('admin.html')
s=p.read_text(encoding='utf-8')
MARK='<!-- WENIK FINANCE LEDGER UI V1 -->'
if MARK in s:
    print('Finance ledger UI already present'); raise SystemExit(0)

anchor='<div class="card"><h3>Add finance entry</h3>'
assert anchor in s
ledger='''<!-- WENIK FINANCE LEDGER UI V1 -->
<div class="card"><div class="row"><div><h3>Finance Ledger · Audit Trail</h3><div class="muted">Permanent finance history. Entries are never deleted; corrections use a reversal.</div></div><button id="refreshFinanceLedger" class="btn secondary">REFRESH</button></div><div id="financeLedgerStatus" class="status"></div><div id="financeLedgerList"><div class="card muted">Finance backend is not enabled in this preview yet.</div></div></div>
'''
s=s.replace(anchor,ledger+anchor,1)

js_anchor="$('addFinanceBtn').onclick=async()=>"
assert js_anchor in s
js=r'''async function loadFinanceLedger(){try{const cur=$('pnlCurrency').value;const rows=await rpc('admin_finance_ledger',{p_currency:cur,p_limit:100});$('financeLedgerList').innerHTML=(rows||[]).map(x=>'<div class="card"><div class="row"><div><b>'+esc(x.category||'Finance entry')+'</b><div class="muted">'+esc(x.entry_type||'')+' · '+esc(x.currency||cur)+' '+Number(x.amount||0).toLocaleString()+' · '+new Date(x.occurred_at).toLocaleString()+'</div>'+(x.notes?'<div class="muted">'+esc(x.notes)+'</div>':'')+'</div><span class="pill">'+esc(String(x.status||'posted').toUpperCase())+'</span></div>'+(x.status==='posted'?'<div class="actions"><button class="btn danger" onclick="reverseFinanceEntry(\''+x.id+'\')">REVERSE</button></div>':'')+'</div>').join('')||'<div class="card muted">No finance entries.</div>';$('financeLedgerStatus').textContent=''}catch(e){const msg=String(e?.message||e);if(/admin_finance_ledger|function .* does not exist|schema cache/i.test(msg))setStatus('financeLedgerStatus','Finance ledger backend is prepared but not enabled on Production yet.');else setStatus('financeLedgerStatus',msg)}}
window.reverseFinanceEntry=async id=>{const reason=prompt('Reason for reversal:');if(reason===null)return;if(!reason.trim()){alert('A reversal reason is required.');return}if(!confirm('Reverse this finance entry? The original entry will remain in history.'))return;try{await rpc('admin_reverse_finance_transaction',{p_transaction_id:id,p_reason:reason.trim()});await Promise.all([loadPnl(),loadFinanceLedger()])}catch(e){alert(e.message)}};
$('refreshFinanceLedger').onclick=loadFinanceLedger;
'''
s=s.replace(js_anchor,js+js_anchor,1)

old="if(b.dataset.panel==='finance')loadPnl();"
new="if(b.dataset.panel==='finance'){loadPnl();loadFinanceLedger();}"
assert old in s
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('Finance ledger audit UI patched safely')
