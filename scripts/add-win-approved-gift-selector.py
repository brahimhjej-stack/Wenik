from pathlib import Path
p=Path('admin.html'); s=p.read_text()
if 'WENIK WIN APPROVED GIFT SELECTOR' in s: raise SystemExit('already applied')
old='<section id="wins" class="panel"><div class="card"><div class="row"><div><h2>WIN Campaigns</h2><div class="muted">Draw is only enabled when entries are locked and prizes exist.</div></div><button id="refreshWins" class="btn secondary" style="width:auto">REFRESH</button></div></div><div id="winList"></div></section>'
if old not in s: raise SystemExit('WIN section anchor missing')
new='''<section id="wins" class="panel"><div class="card"><div class="row"><div><h2>WIN Campaigns</h2><div class="muted">Draw is only enabled when entries are locked and prizes exist.</div></div><button id="refreshWins" class="btn secondary" style="width:auto">REFRESH</button></div></div>
<!-- WENIK WIN APPROVED GIFT SELECTOR -->
<div class="card"><h2>Add Approved Partner Gift to WIN</h2><div class="muted">Only approved gifts with remaining stock can be assigned.</div><select id="winGiftCampaign" class="field"></select><select id="winGiftSelect" class="field"></select><input id="winGiftQty" class="field" type="number" min="1" step="1" value="1" placeholder="Quantity"><button id="assignWinGift" class="btn">ADD GIFT TO WIN</button><div id="winGiftStatus" class="status"></div></div>
<div id="winList"></div></section>'''
s=s.replace(old,new,1)
# Ensure opening WIN loads selector data too
s=s.replace("if(b.dataset.panel==='wins')loadWins();","if(b.dataset.panel==='wins'){loadWins();loadWinGiftOptions();}",1)
# Insert JS before loadWins or before refresh handler as fallback
anchor='async function loadWins()'
if anchor not in s: raise SystemExit('loadWins anchor missing')
js="""async function loadWinGiftOptions(){try{const[camps,gifts]=await Promise.all([rpc('admin_campaign_list'),rpc('admin_available_partner_gifts')]);const usable=(camps||[]).filter(c=>['draft','active','closed'].includes(String(c.status)));$('winGiftCampaign').innerHTML=usable.map(c=>'<option value="'+c.id+'">'+esc(c.title)+' · '+esc(String(c.status).toUpperCase())+'</option>').join('')||'<option value="">No available WIN campaign</option>';$('winGiftSelect').innerHTML=(gifts||[]).filter(g=>Number(g.available_quantity)>0).map(g=>'<option value="'+g.gift_id+'" data-max="'+Number(g.available_quantity)+'">'+esc(g.business_name)+' · '+esc(g.gift_name)+' · Remaining '+Number(g.available_quantity)+'</option>').join('')||'<option value="">No approved gifts with stock</option>'}catch(e){setStatus('winGiftStatus',e.message)}}
$('assignWinGift').onclick=async()=>{try{const campaign=$('winGiftCampaign').value,gift=$('winGiftSelect').value,qty=Number($('winGiftQty').value||0),opt=$('winGiftSelect').selectedOptions[0],max=Number(opt?.dataset.max||0);if(!campaign)throw Error('Choose a WIN campaign.');if(!gift)throw Error('No approved gift available.');if(!Number.isInteger(qty)||qty<1)throw Error('Quantity must be 1 or more.');if(qty>max)throw Error('Only '+max+' remaining.');$('assignWinGift').disabled=true;setStatus('winGiftStatus','Adding gift to WIN...',true);await rpc('admin_assign_partner_gift_to_campaign',{p_campaign_id:campaign,p_gift_id:gift,p_quantity:qty});setStatus('winGiftStatus','Gift added to WIN successfully.',true);$('winGiftQty').value='1';await Promise.all([loadWinGiftOptions(),loadWins(),loadGiftInventoryReport()])}catch(e){setStatus('winGiftStatus',e.message)}finally{$('assignWinGift').disabled=false}};

"""
s=s.replace(anchor,js+anchor,1)
p.write_text(s)
print('patched admin.html WIN gift selector')
