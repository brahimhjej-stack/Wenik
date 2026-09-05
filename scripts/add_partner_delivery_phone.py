from pathlib import Path

p = Path('partner.html')
s = p.read_text()
marker = '<!-- WENIK PARTNER DELIVERY PHONE V1 -->'
if marker in s:
    raise SystemExit(0)

anchor = '  <div id="customerCard" class="card hidden">'
card = '''  <!-- WENIK PARTNER DELIVERY PHONE V1 -->
  <div id="deliveryPhoneCard" class="card">
    <div class="eyebrow">DELIVERY ORDER</div>
    <h2>Enter Customer Phone</h2>
    <div class="muted">For delivery orders, enter the customer phone number instead of scanning the QR.</div>
    <input id="deliveryPhone" class="field" inputmode="tel" autocomplete="tel" placeholder="Customer phone number">
    <button id="deliveryFindBtn" class="btn secondary">FIND CUSTOMER</button>
    <div id="deliveryLookupMsg" class="muted"></div>
    <div id="deliveryResult" class="hidden" style="margin-top:18px">
      <div id="deliveryCustomer" class="result"></div>
      <input id="deliveryAmount" class="field amount" type="number" min="0.01" step="0.01" placeholder="Bill amount">
      <button id="deliveryRecordBtn" class="btn">RECORD DELIVERY VISIT</button>
      <button id="deliveryResetBtn" class="btn secondary">CANCEL</button>
      <div id="deliverySaveMsg" class="muted"></div>
    </div>
  </div>
'''
if anchor not in s:
    raise SystemExit('customerCard anchor not found')
s = s.replace(anchor, card + anchor, 1)

script = r'''
<script type="module">
import{createClient}from'https://esm.sh/@supabase/supabase-js@2';
const U='https://zkrnzwnbdoaqanqzznlw.supabase.co',K='sb_publishable_Q8pOXn-3YAUo_6OX6c2bKg_mLKH8O0k';
const sbDelivery=createClient(U,K),D=id=>document.getElementById(id);
let deliveryPhoneValue='';
async function deliveryRpc(name,args={}){const{data,error}=await sbDelivery.rpc(name,args);if(error)throw error;return data}
function resetDelivery(){deliveryPhoneValue='';D('deliveryPhone').value='';D('deliveryLookupMsg').textContent='';D('deliverySaveMsg').textContent='';D('deliveryAmount').value='';D('deliveryAmount').disabled=false;D('deliveryResult').classList.add('hidden');D('deliveryRecordBtn').disabled=false}
D('deliveryFindBtn').onclick=async()=>{try{const phone=D('deliveryPhone').value.trim();if(!phone)throw Error('Enter customer phone number.');D('deliveryFindBtn').disabled=true;D('deliveryLookupMsg').className='muted';D('deliveryLookupMsg').textContent='Checking customer…';const rows=await deliveryRpc('partner_lookup_customer_by_phone_v1',{p_phone:phone});if(!rows?.length)throw Error('Customer not found on WENIK.');const x=rows[0];deliveryPhoneValue=phone;D('deliveryCustomer').innerHTML='<b>'+String(x.first_name||'Customer')+'</b><br>WENIK ID: '+String(x.wenik_id||'')+'<br>Benefit: '+String(x.benefit_title||'None');D('deliveryLookupMsg').textContent='';D('deliveryResult').classList.remove('hidden');D('deliveryAmount').focus()}catch(e){D('deliveryLookupMsg').className='error';D('deliveryLookupMsg').textContent=e.message||'Unable to find customer.'}finally{D('deliveryFindBtn').disabled=false}};
D('deliveryRecordBtn').onclick=async()=>{const amount=Number(D('deliveryAmount').value);if(!(amount>0))return D('deliverySaveMsg').textContent='Enter the bill amount.';try{D('deliveryRecordBtn').disabled=true;D('deliverySaveMsg').className='muted';D('deliverySaveMsg').textContent='Recording…';const rows=await deliveryRpc('partner_record_transaction_by_phone_v1',{p_phone:deliveryPhoneValue,p_original_amount:amount,p_idempotency_key:crypto.randomUUID(),p_notes:'Partner delivery by phone'});const x=rows?.[0];D('deliverySaveMsg').className='success';D('deliverySaveMsg').textContent='Delivery visit recorded successfully. Final amount: $'+Number(x?.final_amount||0).toFixed(2);D('deliveryAmount').disabled=true;D('deliveryRecordBtn').disabled=true}catch(e){D('deliverySaveMsg').className='error';D('deliverySaveMsg').textContent=e.message||'Unable to record visit.';D('deliveryRecordBtn').disabled=false}};
D('deliveryResetBtn').onclick=resetDelivery;
</script>
'''
if '</body>' not in s:
    raise SystemExit('body end not found')
s = s.replace('</body>', script + '\n</body>', 1)
p.write_text(s)
