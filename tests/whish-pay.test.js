import test from 'node:test';
import assert from 'node:assert/strict';
import {createWhishPay,paymentState} from '../lib/whish-pay.js';
const opts={channel:'test-channel',secret:'test-secret',websiteUrl:'wenik.co',userAgent:'WENIK/Test'};
const order={amount:'3.00',currency:'USD',externalId:'persisted-order-1',successCallbackUrl:'https://wenik.co/api/whish/callback?attempt=success',failureCallbackUrl:'https://wenik.co/api/whish/callback?attempt=failure',successRedirectUrl:'https://wenik.co/payment',failureRedirectUrl:'https://wenik.co/payment'};
const reply=data=>new Response(JSON.stringify(data),{status:200});
test('sandbox by default; creation stays pending, callbacks include persisted reference',async()=>{
 let captured;
 const api=createWhishPay({...opts,fetchImpl:async(url,init)=>{captured={url,init};return reply({status:true,code:null,data:{collectUrl:'https://whish.money/pay/test'}});}});
 const r=await api.createPayment(order);assert.equal(r.state,'pending');assert.ok(captured.url.startsWith('https://partner.api.sbx.whish.money/'));
 const body=JSON.parse(captured.init.body);assert.equal(body.amount,'3.00');assert.equal(new URL(body.failureCallbackUrl).searchParams.get('externalId'),order.externalId);assert.equal(captured.init.headers.secret,'test-secret');
});
test('HTTP 200 business failure is not a payment',async()=>{
 const api=createWhishPay({...opts,fetchImpl:async()=>reply({status:false,code:'collect.wrong_denomination'})});
 await assert.rejects(api.createPayment(order),e=>e.code==='collect.wrong_denomination'&&!e.uncertain);
});
test('500 and transport errors remain unknown, for reconciliation',async()=>{
 for(const fetchImpl of [async()=>reply({status:false,code:'500'}),async()=>{throw Error('timeout')}]){
 const api=createWhishPay({...opts,fetchImpl});await assert.rejects(api.createPayment(order),e=>e.uncertain);
 }
});
test('failed attempt can still be pending and then succeed on same reference',async()=>{
 const seen=[];let call=0;const api=createWhishPay({...opts,fetchImpl:async(_,init)=>{seen.push(JSON.parse(init.body).externalId);return reply({status:true,code:null,data:{collectStatus:call++?'success':'pending'}})}});
 assert.equal((await api.getPaymentStatus(order)).state,'pending');assert.equal((await api.getPaymentStatus(order)).state,'success');assert.deepEqual(seen,[order.externalId,order.externalId]);
});
test('unknown/malformed states never grant entitlement',()=>{
 for(const v of [null,{status:true,data:{}},{status:false,data:{collectStatus:'success'}},{status:true,code:'500',data:{collectStatus:'success'}}])assert.equal(paymentState(v),'unknown');
 assert.equal(paymentState({status:true,code:null,data:{collectStatus:'refunded'}}),'refunded');
});
test('production and invalid amounts/URLs fail before network call',async()=>{
 assert.throws(()=>createWhishPay({...opts,environment:'production'}));
 let calls=0;const api=createWhishPay({...opts,fetchImpl:async()=>{calls++;return reply({})}});
 for(const changes of [{amount:3},{amount:'0.01'},{amount:'NaN'},{currency:'EUR'},{currency:'LBP',amount:'1000.50'},{successCallbackUrl:'http://localhost/x'},{failureCallbackUrl:'https://127.0.0.1/x'}])await assert.rejects(api.createPayment({...order,...changes}));
 assert.equal(calls,0);
});
test('untrusted checkout host rejected',async()=>{
 const api=createWhishPay({...opts,fetchImpl:async()=>reply({status:true,code:null,data:{collectUrl:'https://whish.money.evil.example/pay'}})});
 await assert.rejects(api.createPayment(order),e=>e.code==='collect_url.invalid');
});
