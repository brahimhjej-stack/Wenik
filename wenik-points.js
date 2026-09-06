import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
import QRCode from 'https://esm.sh/qrcode@1.5.4';

const U='https://zkrnzwnbdoaqanqzznlw.supabase.co';
const K='sb_publishable_Q8pOXn-3YAUo_6OX6c2bKg_mLKH8O0k';
const sb=createClient(U,K);
const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function rpc(n,a={}){const{data,error}=await sb.rpc(n,a);if(error)throw error;return data}
const style=document.createElement('style');
style.textContent=`
.wenikPointsHero{position:relative;overflow:hidden;border:1px solid rgba(178,92,255,.28);border-radius:26px;padding:22px;margin:14px 0;background:radial-gradient(circle at 0 0,rgba(143,36,255,.32),transparent 42%),radial-gradient(circle at 100% 100%,rgba(255,111,33,.22),transparent 45%),linear-gradient(145deg,rgba(30,14,60,.97),rgba(17,11,31,.96));box-shadow:0 18px 50px rgba(0,0,0,.28)}
.wenikPointsHero:before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,#8f24ff,#ef159d,#ff6f21,#ffd21c)}
.wenikPointsBalance{font-size:42px;font-weight:1000;line-height:1;margin:10px 0}.wenikPointsRule{font-weight:900;color:#ffd7ef}.wenikRewardGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:12px}.wenikReward{border:1px solid rgba(178,92,255,.22);border-radius:20px;padding:14px;background:#100d19}.wenikReward>b{display:block;color:#fff!important;font-size:18px;font-weight:900;line-height:1.25;margin-bottom:4px}.wenikReward img{width:100%;aspect-ratio:1.4/1;object-fit:cover;border-radius:14px;margin-bottom:9px}.wenikRewardCost{font-weight:1000;font-size:18px;color:#ffd553}.wenikMini{font-size:12px;color:#b9b4c8}.wenikRedeemCode{font-family:monospace;word-break:break-all;font-size:12px;color:#ffd553}.wenikQr{display:block;width:180px;max-width:100%;margin:12px auto;border-radius:14px;background:#fff;padding:8px}.wenikPointsTabPanel{display:none}.wenikPointsTabPanel.active{display:block}@media(max-width:520px){.wenikRewardGrid{grid-template-columns:1fr}.wenikPointsBalance{font-size:36px}}
`;
document.head.appendChild(style);

async function waitSession(){for(let i=0;i<40;i++){const{data:{session}}=await sb.auth.getSession();if(session)return session;await new Promise(r=>setTimeout(r,250))}return null}

async function installCustomer(){
  const win=$('win'); if(!win)return;
  const host=document.createElement('div');host.id='wenikPointsCustomer';
  const hero=win.querySelector('.hero'); hero?.insertAdjacentElement('afterend',host);
  async function render(){
    try{
      const balance=Number(await rpc('wenik_customer_points_balance')||0);
      const [catalog,my]=await Promise.all([rpc('customer_points_reward_catalog'),rpc('customer_my_points_redemptions')]);
      host.innerHTML=`<div class="wenikPointsHero"><div class="eyebrow">WENIK POINTS</div><div class="wenikPointsBalance">${balance.toLocaleString()} PTS</div><div class="wenikPointsRule">$5 = 10 Points</div><div class="muted">Use your WENIK Points to choose gifts. Points are not cash.</div></div><div class="sectionTitle"><h3>POINTS GIFTS</h3><span class="muted">Choose your gift</span></div><div class="wenikRewardGrid" id="wenikRewardGrid"></div><div class="sectionTitle"><h3>MY POINTS REQUESTS</h3></div><div id="wenikMyRedemptions"></div>`;
      const grid=$('wenikRewardGrid');
      grid.innerHTML=(catalog||[]).map(g=>`<div class="wenikReward">${g.partner_logo_url?`<img src="${esc(g.partner_logo_url)}" alt="">`:''}<b>${esc(g.gift_title)}</b><div class="wenikMini">${esc(g.partner_name)}</div><div class="wenikRewardCost">${Number(g.points_cost).toLocaleString()} PTS</div><div class="wenikMini">${Number(g.remaining_quantity)} available</div><button class="btn" data-points-prize="${g.prize_id}" ${balance<Number(g.points_cost)?'disabled':''}>${balance<Number(g.points_cost)?'NOT ENOUGH POINTS':'GET THIS GIFT'}</button></div>`).join('')||'<div class="card muted">No Points gifts available right now.</div>';
      grid.querySelectorAll('[data-points-prize]').forEach(b=>b.onclick=async()=>{if(!confirm('Use your WENIK Points for this gift?'))return;try{b.disabled=true;await rpc('customer_request_points_redemption',{p_prize_id:b.dataset.pointsPrize});alert('Request sent to WENIK for approval.');await render()}catch(e){alert(e.message);b.disabled=false}});
      const box=$('wenikMyRedemptions');box.innerHTML='';
      for(const r of (my||[])){
        const d=document.createElement('div');d.className='card';d.innerHTML=`<div class="row"><b>${esc(r.gift_title)}</b><span class="badge">${esc(String(r.status).toUpperCase())}</span></div><div class="muted">${esc(r.partner_name)} · ${Number(r.points_cost).toLocaleString()} PTS</div>${r.redeem_token?`<div class="wenikRedeemCode">${esc(r.redeem_token)}</div><img class="wenikQr" alt="Redeem QR">`:''}`;box.appendChild(d);if(r.redeem_token){const img=d.querySelector('.wenikQr');img.src=await QRCode.toDataURL(String(r.redeem_token),{width:300,margin:1})}
      }
      if(!(my||[]).length)box.innerHTML='<div class="card muted">No Points gift requests yet.</div>';
    }catch(e){host.innerHTML='<div class="card error">Points are temporarily unavailable.</div>';console.error(e)}
  }
  const oldTab=window.tab;if(typeof oldTab==='function'&&!oldTab.__wenikPoints){window.tab=function(id,b){const r=oldTab(id,b);if(id==='win')render();return r};window.tab.__wenikPoints=true}
  await render();
}

async function installPartner(){
  const app=$('app');if(!app)return;
  const card=document.createElement('div');card.className='card';card.id='wenikPartnerPointsCard';
  card.innerHTML=`<div class="eyebrow">POINTS GIFT COLLECTION</div><h2>Redeem Customer Gift</h2><div class="muted">$5 = 10 Points. Scan the one-time QR shown in the customer's WENIK account.</div><video id="pointsRedeemCamera" playsinline muted style="margin-top:14px"></video><input id="pointsRedeemCode" class="field" placeholder="Redeem code (manual fallback)"><button id="pointsRedeemScan" class="btn">SCAN REDEEM QR</button><button id="pointsRedeemConfirm" class="btn secondary">CONFIRM CODE</button><div id="pointsRedeemMsg" class="muted"></div>`;
  const scanCard=$('scanCard');scanCard?.insertAdjacentElement('afterend',card);
  let stream=null,scanning=false;
  const stop=()=>{scanning=false;if(stream)stream.getTracks().forEach(t=>t.stop());stream=null;if($('pointsRedeemCamera'))$('pointsRedeemCamera').srcObject=null};
  async function redeem(raw){const token=String(raw||'').trim();if(!/^[0-9a-f-]{36}$/i.test(token))return $('pointsRedeemMsg').textContent='Invalid redeem code.';if(!confirm('Confirm that you are handing this gift to the customer now?'))return;try{stop();$('pointsRedeemMsg').textContent='Confirming collection…';const r=await rpc('partner_redeem_points_gift',{p_redeem_token:token});const x=r?.[0];$('pointsRedeemMsg').className='success';$('pointsRedeemMsg').textContent=`Collected ✓ ${x?.customer_name||''} · ${x?.gift_title||''}`;$('pointsRedeemCode').value=''}catch(e){$('pointsRedeemMsg').className='error';$('pointsRedeemMsg').textContent=e.message}}
  $('pointsRedeemConfirm').onclick=()=>redeem($('pointsRedeemCode').value);
  $('pointsRedeemScan').onclick=async()=>{try{if(!('BarcodeDetector'in window))throw Error('QR camera is not supported. Use the code field instead.');const detector=new BarcodeDetector({formats:['qr_code']});stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:{ideal:'environment'}}});$('pointsRedeemCamera').srcObject=stream;await $('pointsRedeemCamera').play();scanning=true;$('pointsRedeemMsg').textContent='Point the camera at the customer gift QR.';const loop=async()=>{if(!scanning)return;try{const codes=await detector.detect($('pointsRedeemCamera'));if(codes[0])return redeem(codes[0].rawValue)}catch{}requestAnimationFrame(loop)};loop()}catch(e){stop();$('pointsRedeemMsg').className='error';$('pointsRedeemMsg').textContent=e.message}};
  addEventListener('pagehide',stop);
}

async function installAdmin(){
  const tabs=document.querySelector('.tabs'),app=$('app');if(!tabs||!app)return;
  const tabBtn=document.createElement('button');tabBtn.className='tab';tabBtn.textContent='POINTS';tabBtn.dataset.panel='points';tabs.appendChild(tabBtn);
  const panel=document.createElement('section');panel.id='points';panel.className='panel wenikPointsTabPanel';
  panel.innerHTML=`<div class="card"><div class="row"><div><h2>WENIK Points</h2><div class="muted">Current conversion and redemption control.</div></div><button id="pointsRefresh" class="btn secondary" style="width:auto">REFRESH</button></div><div class="two"><input id="pointsPerUsd" class="field" type="number" min="0.01" step="0.01" placeholder="Points per $1"><input id="pointsPendingUsd" class="field" type="number" min="1" step="1" placeholder="Large bill review threshold"></div><button id="pointsSaveSettings" class="btn">SAVE POINTS SETTINGS</button><div id="pointsSettingsMsg" class="status"></div></div><div class="card"><h2>Points Gift Catalog</h2><div class="muted">Choose any active WIN gift and set how many Points it costs.</div><div id="pointsCatalogAdmin"></div></div><h2>Points Gift Requests</h2><div id="pointsRedemptionsAdmin"></div>`;
  app.appendChild(panel);
  tabBtn.onclick=()=>{document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));panel.classList.add('active');tabBtn.classList.add('active');load()};
  async function load(){try{const [s,gifts,reds]=await Promise.all([rpc('admin_points_settings'),rpc('public_active_win_gifts',{p_limit:300}),rpc('admin_points_redemptions')]);const st=s?.[0]||{};$('pointsPerUsd').value=st.points_per_usd??2;$('pointsPendingUsd').value=st.pending_net_amount_usd??500;$('pointsCatalogAdmin').innerHTML=(gifts||[]).map(g=>`<div class="card"><div class="row"><div><b>${esc(g.gift_title)}</b><div class="muted">${esc(g.partner_name)} · ${Number(g.remaining_quantity)} left</div></div><input id="pc-${g.prize_id}" class="field" type="number" min="1" step="1" placeholder="Points cost" style="max-width:150px"></div><button class="btn secondary" data-set-reward="${g.prize_id}">SET AS POINTS GIFT</button></div>`).join('')||'<div class="muted">No active WIN gifts.</div>';document.querySelectorAll('[data-set-reward]').forEach(b=>b.onclick=async()=>{const cost=Number($('pc-'+b.dataset.setReward).value);if(!Number.isInteger(cost)||cost<1)return alert('Enter a valid Points cost.');try{await rpc('admin_set_points_reward',{p_prize_id:b.dataset.setReward,p_points_cost:cost,p_active:true});alert('Points gift saved.')}catch(e){alert(e.message)}});$('pointsRedemptionsAdmin').innerHTML=(reds||[]).map(r=>`<div class="card"><div class="row"><div><b>${esc(r.customer_name)}</b><div class="muted">${esc(r.customer_wenik_id)} · ${esc(r.gift_title)} · ${esc(r.partner_name)}</div></div><span class="pill">${esc(String(r.status).toUpperCase())}</span></div><div><b>${Number(r.points_cost).toLocaleString()} PTS</b></div>${r.status==='pending'?`<div class="actions"><button class="btn ok" data-red-approve="${r.redemption_id}">APPROVE</button><button class="btn danger" data-red-reject="${r.redemption_id}">REJECT</button></div>`:''}</div>`).join('')||'<div class="card muted">No Points gift requests.</div>';document.querySelectorAll('[data-red-approve]').forEach(b=>b.onclick=()=>review(b.dataset.redApprove,true));document.querySelectorAll('[data-red-reject]').forEach(b=>b.onclick=()=>review(b.dataset.redReject,false));}catch(e){$('pointsSettingsMsg').textContent=e.message}}
  async function review(id,approve){let note=null;if(!approve)note=prompt('Reason for rejection (optional):')||null;try{await rpc('admin_review_points_redemption',{p_redemption_id:id,p_approve:approve,p_note:note});await load()}catch(e){alert(e.message)}}
  $('pointsSaveSettings').onclick=async()=>{try{const a=Number($('pointsPerUsd').value),b=Number($('pointsPendingUsd').value);await rpc('admin_set_points_settings',{p_points_per_usd:a,p_pending_net_amount_usd:b});$('pointsSettingsMsg').className='status good';$('pointsSettingsMsg').textContent=`Saved · $5 = ${Math.round(a*5)} Points`;await load()}catch(e){$('pointsSettingsMsg').className='status error';$('pointsSettingsMsg').textContent=e.message}};
  $('pointsRefresh').onclick=load;
}

(async()=>{await waitSession();if($('win')&&$('shell'))return installCustomer();if(document.title.includes('Partner'))return installPartner();if(document.title.includes('Management'))return installAdmin()})();
