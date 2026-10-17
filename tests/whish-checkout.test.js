import test from 'node:test';import assert from 'node:assert/strict';
import {createCheckoutService,callbackToken} from '../lib/whish-checkout.js';
const id='c5256ee6-7ac0-4e9d-bd2b-1d6ae7cfae68',secret='sandbox-callback-key-for-tests-only-123';
function harness(){let paid=0,checks=0,url=null;const order={id,auth_user_id:'user',environment:'sandbox',amount:'3.00',currency:'USD'};let state='pending';let fulfilled=false;
 const store={prepare:async()=>({...order,collect_url:url}),get:async()=>order,setCollectUrl:async(_,u)=>{url=u},reconcile:async(_,env,s)=>{if(s==='success'&&!fulfilled){fulfilled=true;paid++}return{state:s,sandbox:env==='sandbox'}}};
 const provider={createPayment:async args=>{assert.equal(args.amount,'3.00');assert.equal(args.externalId,id);assert.equal(args.successCallbackUrl,args.failureCallbackUrl);return{collectUrl:'https://whish.money/pay/test'}},getPaymentStatus:async()=>{checks++;return{state}}};
 return{app:createCheckoutService({store,provider,origin:'https://wenik.co',callbackSecret:secret}),store,setState:s=>state=s,paid:()=>paid,checks:()=>checks};}
test('uses persisted server price, reuses URL on repeated create',async()=>{const h=harness();assert.equal((await h.app.create('user','customer')).amount,'3.00');assert.equal((await h.app.create('user','customer')).collectUrl,'https://whish.money/pay/test');assert.equal(h.paid(),0)});
test('cannot read another user order',async()=>{const h=harness();await assert.rejects(h.app.status('other',id));assert.equal(h.checks(),0)});
test('forged callback cannot trigger verification or fulfilment',async()=>{const h=harness();await assert.rejects(h.app.callback(id,'0'.repeat(64)));assert.equal(h.checks(),0)});
test('failure signal leaves pending; verified success is idempotent',async()=>{const h=harness(),token=callbackToken(id,secret);assert.equal((await h.app.callback(id,token)).state,'pending');assert.equal(h.paid(),0);h.setState('success');await h.app.callback(id,token);await h.app.callback(id,token);assert.equal(h.paid(),1);assert.equal(h.checks(),3)});
test('trial bypasses provider and returns trial end',async()=>{const h=harness();h.store.prepare=async()=>({trial:true,trialEndsAt:'2027-01-17'});assert.equal((await h.app.create('user','partner')).trial,true);assert.equal(h.checks(),0)});
test('sandbox cannot reconcile production order',async()=>{const h=harness();h.store.get=async()=>({auth_user_id:'user',environment:'production'});await assert.rejects(h.app.status('user',id));assert.equal(h.checks(),0)});
