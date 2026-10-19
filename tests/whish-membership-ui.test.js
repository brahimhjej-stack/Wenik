import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const script=readFileSync(new URL('../customer-billing.html',import.meta.url),'utf8').match(/<script type="module">([\s\S]*?)<\/script>/)[1].replace(/^import[^\n]+\n/m,'');
async function render({environment='production',enabled=true,active=true,days=3,signedIn=true}={}){
 const nodes={};const now=Date.UTC(2026,9,19,12);
 class Clock extends Date{constructor(...args){super(...(args.length?args:[now]));}static now(){return now;}}
 const context={Date:Clock,document:{getElementById:id=>nodes[id]??={textContent:'',hidden:false,disabled:false}},fetch:async()=>({ok:true,json:async()=>({environment,checkoutEnabled:enabled,supabaseUrl:'https://test.example',publishableKey:'test'})}),createClient:()=>({auth:{getSession:async()=>({data:{session:signedIn?{}:null}})},rpc:async()=>({data:{monthlyFee:3,currency:'USD',active,paidUntil:new Date(now+days*86400000).toISOString()}})})};
 vm.runInNewContext(script,context);await new Promise(r=>setImmediate(r));return nodes;
}
test('near-expiry membership invites an explicitly confirmed renewal',async()=>{const n=await render();assert.match(n.renewal.textContent,/expires soon/);assert.match(n.renewal.textContent,/confirmation/);assert.equal(n.pay.textContent,'Renew for another month');assert.equal(n.pay.hidden,false);});
test('seven-day reminder excludes memberships with more than seven days left',async()=>{assert.match((await render({days:7})).renewal.textContent,/expires soon/);assert.equal((await render({days:8})).renewal.textContent,'');});
test('expired membership offers activation without an automatic charge',async()=>{const n=await render({active:false,days:-1});assert.equal(n.pay.textContent,'Activate membership with Whish');assert.match(n.renewal.textContent,/no automatic monthly charge/);});
test('sandbox never claims a real renewal is required',async()=>{const n=await render({environment:'sandbox'});assert.equal(n.renewal.textContent,'');assert.match(n.status.textContent,/real membership is unchanged/);assert.equal(n.pay.textContent,'Test payment with Whish');});
test('disabled checkout and signed-out users cannot see a payment action',async()=>{for(const options of [{enabled:false},{signedIn:false}]){const n=await render(options);assert.equal(n.pay.hidden,true);assert.equal(n.renewal.textContent,'');assert.equal(n.refresh.disabled,false);}});
