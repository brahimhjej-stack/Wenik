import test from 'node:test';
import assert from 'node:assert/strict';
import { Webhook } from 'standardwebhooks';
import handler, { __test } from '../api/send-sms-hook.js';

const secret = Buffer.from('isolated-test-webhook-secret-32-bytes').toString('base64');
process.env.SEND_SMS_HOOK_SECRET = 'v1,whsec_' + secret;
process.env.BSB_API_KEY = 'synthetic-key';
process.env.BSB_API_SECRET = 'synthetic-secret';

function signedRequest() {
 const body = JSON.stringify({user:{phone:'+96176468506'},sms:{otp:'123456'}});
 const stamp = new Date(); const id = 'synthetic-hook';
 return {method:'POST',body,headers:{'webhook-id':id,'webhook-timestamp':String(Math.floor(stamp.getTime()/1000)),'webhook-signature':new Webhook(secret).sign(id,stamp,body)}};
}
function response() {return {code:0,body:null,setHeader(){},status(n){this.code=n;return this},json(body){this.body=body;return this}}}

test('Lebanese phone normalization and invalid inputs',()=>{
 assert.equal(__test.normalizeDestination('76 468506'),'96176468506');
 assert.equal(__test.normalizeDestination('0096176468506'),'96176468506');
 assert.throws(()=>__test.normalizeDestination('123'));
 assert.throws(()=>__test.smsRequest('76468506','123'));
});
test('provider rejection and malformed response are not treated as success',()=>{
 assert.deepEqual(__test.assertAccepted('[{"status":201}]'),[{status:201}]);
 for(const body of ['', 'not json', '[{"status":400}]', '[{"status":201},{"status":400}]'])assert.throws(()=>__test.assertAccepted(body));
});
test('signed hook, invalid signature, and provider failure without sending SMS',async()=>{
 const oldFetch=globalThis.fetch, oldError=console.error, oldInfo=console.info;
 let calls=0; console.error=()=>{};console.info=()=>{};
 try {
  globalThis.fetch=async(_url,options)=>{calls++;const payload=JSON.parse(options.body);assert.equal(payload[0].destination,'96176468506');return {ok:true,text:async()=> '[{"status":201}]'}};
  const good=response();await handler(signedRequest(),good);assert.equal(good.code,200);assert.equal(calls,1);
  const badReq=signedRequest();badReq.headers['webhook-signature']='v1,invalid';const bad=response();await handler(badReq,bad);assert.equal(bad.code,500);assert.equal(calls,1);
  globalThis.fetch=async()=>{calls++;return {ok:true,text:async()=> '[{"status":400,"message":"Rejected"}]'}};
  const failed=response();await handler(signedRequest(),failed);assert.equal(failed.code,500);assert.equal(calls,2);
  const wrong=response();await handler({method:'GET'},wrong);assert.equal(wrong.code,405);assert.equal(calls,2);
 }finally{globalThis.fetch=oldFetch;console.error=oldError;console.info=oldInfo;}
});
