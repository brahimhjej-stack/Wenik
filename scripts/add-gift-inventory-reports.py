from pathlib import Path

partner=Path('partner.html')
admin=Path('admin.html')
p=partner.read_text(encoding='utf-8')
a=admin.read_text(encoding='utf-8')

# Partner quantity input + display
if 'id="giftQuantity"' not in p:
    anchor='<input id="giftDescription" class="field" placeholder="Short description (optional)">'
    assert anchor in p
    p=p.replace(anchor, anchor+'\n    <input id="giftQuantity" class="field" type="number" min="1" step="1" value="1" placeholder="Quantity">',1)
    p=p.replace("<div class=\"muted\">Status: '+String(g.approval_status||'pending').toUpperCase()+'</div>","<div class=\"muted\">Quantity: '+Number(g.quantity||1)+' · Status: '+String(g.approval_status||'pending').toUpperCase()+'</div>",1)
    p=p.replace("const name=$('giftName').value.trim(),description=$('giftDescription').value.trim();","const name=$('giftName').value.trim(),description=$('giftDescription').value.trim(),quantity=Math.max(1,Number($('giftQuantity').value||1));",1)
    p=p.replace("await rpc('partner_submit_gift',{p_name:name,p_description:description||null});","await rpc('partner_submit_gift',{p_name:name,p_description:description||null,p_quantity:quantity});",1)
    p=p.replace("$('giftName').value='';$('giftDescription').value='';","$('giftName').value='';$('giftDescription').value='';$('giftQuantity').value='1';",1)

# Admin report section
MARK='<!-- WENIK GIFT INVENTORY REPORT -->'
if MARK not in a:
    anchor='<h2>Partner Reports</h2><div id="partners"></div>'
    assert anchor in a
    block='''<h2>Gift Inventory</h2>\n<div id="giftInventorySummary" class="grid"></div>\n<div id="giftInventoryPartners"></div>\n<!-- WENIK GIFT INVENTORY REPORT -->\n'''
    a=a.replace(anchor, block+anchor,1)

    js_anchor='async function loadReports(){try{'
    assert js_anchor in a
    # add helper before loadReports
    helper=r'''async function loadGiftInventoryReport(){
  try{
    const s=(await rpc('admin_gift_inventory_summary'))?.[0]||{};
    $('giftInventorySummary').innerHTML=[['Total gifts',s.total_gifts||0],['Approved',s.approved_gifts||0],['Won',s.won_gifts||0],['Remaining',s.remaining_gifts||0]].map(x=>'<div class="metric"><span class="muted">'+x[0]+'</span><b>'+x[1]+'</b></div>').join('');
    const rows=await rpc('admin_partner_gift_inventory');
    $('giftInventoryPartners').innerHTML=(rows||[]).filter(r=>Number(r.total_gifts||0)>0).map(r=>'<div class="card"><div class="row"><h3>'+esc(r.business_name)+'</h3><span class="pill">'+Number(r.remaining_gifts||0)+' remaining</span></div><div class="muted">Total '+Number(r.total_gifts||0)+' · Approved '+Number(r.approved_gifts||0)+' · Won '+Number(r.won_gifts||0)+' · Remaining '+Number(r.remaining_gifts||0)+'</div></div>').join('')||'<div class="card muted">No partner gifts yet.</div>';
  }catch(e){$('giftInventoryPartners').innerHTML='<div class="card error">'+esc(e.message)+'</div>'}
}
'''
    a=a.replace(js_anchor, helper+js_anchor,1)
    # ensure every report refresh also refreshes gifts inventory
    old="async function loadReports(){try{$('refreshReports').disabled=true;"
    new="async function loadReports(){try{$('refreshReports').disabled=true;await loadGiftInventoryReport();"
    assert old in a
    a=a.replace(old,new,1)

partner.write_text(p,encoding='utf-8')
admin.write_text(a,encoding='utf-8')
print('Gift quantity + inventory reports patched')
