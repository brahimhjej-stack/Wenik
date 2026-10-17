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
