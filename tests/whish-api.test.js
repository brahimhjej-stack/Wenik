import test from 'node:test';
import assert from 'node:assert/strict';
import handler from '../api/whish/[action].js';

test('public configuration never exposes server credentials or enables native purchases',async()=>{
 const keys=['SUPABASE_URL','SUPABASE_PUBLISHABLE_KEY','SUPABASE_SERVICE_ROLE_KEY','WHISH_SECRET','WHISH_CALLBACK_SECRET','WHISH_ENVIRONMENT','WHISH_CHECKOUT_ENABLED'];
 const saved=Object.fromEntries(keys.map(k=>[k,process.env[k]]));
 try{
  Object.assign(process.env,{SUPABASE_URL:'https://test.supabase.co',SUPABASE_PUBLISHABLE_KEY:'public-key',SUPABASE_SERVICE_ROLE_KEY:'private-service-key',WHISH_SECRET:'private-provider-secret',WHISH_CALLBACK_SECRET:'private-callback-secret',WHISH_ENVIRONMENT:'sandbox',WHISH_CHECKOUT_ENABLED:'false'});
  let code,payload;const res={setHeader(){},status(n){code=n;return this},json(data){payload=data}};
  await handler({query:{action:'config'},method:'GET'},res);
  assert.equal(code,200);assert.equal(payload.checkoutEnabled,false);assert.equal(payload.nativeCheckoutEnabled,false);
  const serialized=JSON.stringify(payload);for(const secret of ['private-service-key','private-provider-secret','private-callback-secret'])assert.ok(!serialized.includes(secret));
  process.env.WHISH_CHECKOUT_ENABLED='true';process.env.WHISH_ENVIRONMENT='production';
  await handler({query:{action:'create'},method:'POST'},res);assert.equal(code,503);assert.match(payload.error,/Live checkout/);
 }finally{for(const key of keys){if(saved[key]===undefined)delete process.env[key];else process.env[key]=saved[key];}}
});

test('anonymous payment create and status are rejected before network access',async()=>{
 const names=['WHISH_ENVIRONMENT','WHISH_CHECKOUT_ENABLED','SUPABASE_URL','SUPABASE_SERVICE_ROLE_KEY','WHISH_SITE_URL','WHISH_CHANNEL','WHISH_SECRET','WHISH_WEBSITE_URL','WHISH_CALLBACK_SECRET'];
 const saved=Object.fromEntries(names.map(k=>[k,process.env[k]]));
 const originalFetch=globalThis.fetch;let networkCalls=0;
 try{
  Object.assign(process.env,{WHISH_ENVIRONMENT:'sandbox',WHISH_CHECKOUT_ENABLED:'true',SUPABASE_URL:'https://test.supabase.co',SUPABASE_SERVICE_ROLE_KEY:'test-service',WHISH_SITE_URL:'https://test.example',WHISH_CHANNEL:'test-channel',WHISH_SECRET:'test-secret',WHISH_WEBSITE_URL:'https://test.example',WHISH_CALLBACK_SECRET:'test-callback-secret-at-least-32-characters'});
  globalThis.fetch=async()=>{networkCalls++;throw Error('Anonymous request must not reach the network');};
  for(const action of ['create','status']){
   let code,payload;const res={setHeader(){},status(n){code=n;return this},json(data){payload=data}};
   await handler({query:{action},method:action==='create'?'POST':'GET',headers:{},body:{kind:'customer'}},res);
   assert.equal(code,401);assert.equal(payload.error,'Sign in required');
  }
  assert.equal(networkCalls,0);
 }finally{
  globalThis.fetch=originalFetch;
  for(const key of names){if(saved[key]===undefined)delete process.env[key];else process.env[key]=saved[key];}
 }
});
