from pathlib import Path
p=Path('admin.html')
s=p.read_text(encoding='utf-8')
old='''<!-- WENIK ADMIN GIFTS APPROVAL UI -->
<section id="giftsApproval" class="panel"><div class="card"><div class="row"><div><h2>Partner Gifts</h2><div class="muted">WENIK Admin manages contracted Partner gifts. Approved gifts are ready for WIN.</div></div><button id="refreshGifts" class="btn secondary" style="width:auto">REFRESH</button></div></div><div id="pendingGifts"></div></section>'''
new='''<!-- WENIK ADMIN CONTRACT GIFTS UI -->
<section id="giftsApproval" class="panel">
<div class="card"><div class="row"><div><h2>Contract Gifts</h2><div class="muted">WENIK enters and manages the gifts agreed in each Partner contract. Partners do not edit gifts.</div></div><button id="refreshGifts" class="btn secondary" style="width:auto">REFRESH</button></div></div>
<div class="card"><h3>Add Contract Gift</h3><input id="contractGiftPartner" class="field" placeholder="Partner ID"><input id="contractGiftName" class="field" placeholder="Gift name · e.g. Dinner for Two"><div class="two"><select id="contractGiftType" class="field"><option value="voucher">Voucher</option><option value="discount">Discount</option><option value="experience">Experience</option><option value="item">Item</option><option value="service">Service</option><option value="other">Other</option></select><input id="contractGiftValue" class="field" placeholder="Display value · e.g. $50 or 30%"></div><input id="contractGiftQty" class="field" type="number" min="1" step="1" value="1" placeholder="Quantity"><textarea id="contractGiftDescription" class="field" rows="3" placeholder="Description / conditions"></textarea><button id="createContractGift" class="btn">ADD CONTRACT GIFT</button><div id="contractGiftStatus" class="status"></div></div>
<div id="pendingGifts"></div></section>'''
assert old in s, 'gift section anchor missing'
s=s.replace(old,new,1)
anchor="$('refreshGifts').onclick=loadPendingGifts;"
insert="""
$('createContractGift').onclick=async()=>{try{const partner=$('contractGiftPartner').value.trim(),name=$('contractGiftName').value.trim(),type=$('contractGiftType').value,value=$('contractGiftValue').value.trim(),qty=Number($('contractGiftQty').value),description=$('contractGiftDescription').value.trim();if(!partner||!name)throw Error('Partner and gift name are required.');if(!Number.isInteger(qty)||qty<1)throw Error('Quantity must be at least 1.');setStatus('contractGiftStatus','Saving contract gift...',true);await rpc('admin_create_partner_gift',{p_partner_id:partner,p_name:name,p_description:description||null,p_quantity:qty,p_gift_type:type,p_display_value:value||null});$('contractGiftName').value='';$('contractGiftValue').value='';$('contractGiftQty').value='1';$('contractGiftDescription').value='';setStatus('contractGiftStatus','Contract gift added by WENIK.',true);await loadPendingGifts();await loadWinGiftOptions()}catch(e){const msg=String(e?.message||e);if(/admin_create_partner_gift|function .* does not exist|schema cache/i.test(msg))setStatus('contractGiftStatus','Admin contract-gift backend is prepared but not enabled on Production yet.');else setStatus('contractGiftStatus',msg)}};
"""
assert anchor in s
s=s.replace(anchor,anchor+insert,1)
p.write_text(s,encoding='utf-8')
print('Prepared simple Admin-only contract gift entry UI.')
