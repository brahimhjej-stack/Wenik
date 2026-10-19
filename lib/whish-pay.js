// Server-only Whish Pay v1.4.4 adapter. Never import into a browser bundle.
const BASES = Object.freeze({sandbox:'https://partner.api.sbx.whish.money/itel-service/api',production:'https://api.whish.money/itel-service/api'});
export class WhishError extends Error {
  constructor(code, uncertain=false) { super('Whish request '+(uncertain?'requires reconciliation':'was rejected')); this.code=code; this.uncertain=uncertain; }
}
export function paymentState(envelope) {
  if (envelope?.status !== true || envelope?.code != null) return 'unknown';
  const state=envelope?.data?.collectStatus;
  return ['pending','success','failed','refunded'].includes(state) ? state : 'unknown';
}
function publicUrl(value) {
  const u=new URL(value);
  if(u.protocol!=='https:' || u.username || u.password || !u.hostname.includes('.') || /(^|\.)(localhost|local|internal)$/.test(u.hostname) || /^[\d.]+$/.test(u.hostname) || u.hostname.includes(':')) throw new Error('Public HTTPS callback/redirect URL required');
  return u;
}
export function createWhishPay({channel,secret,websiteUrl,userAgent,environment='sandbox',allowProduction=false,fetchImpl=fetch,timeoutMs=12000}) {
  if(!channel || !secret || !websiteUrl || !userAgent) throw new Error('Whish server configuration incomplete');
  if(!BASES[environment] || (environment==='production' && !allowProduction)) throw new Error('Production is disabled');
  async function request(path,body) {
    let response;
    try { response=await fetchImpl(BASES[environment]+path,{method:body?'POST':'GET',redirect:'error',signal:AbortSignal.timeout(timeoutMs),headers:{channel:String(channel),secret,websiteUrl,'User-Agent':userAgent,...(body?{'Content-Type':'application/json'}:{})},...(body?{body:JSON.stringify(body)}:{})}); }
    catch { throw new WhishError('transport.unknown',true); }
    if(!response.ok) throw new WhishError('http.'+response.status,true);
    let result;try {result=await response.json();}catch {throw new WhishError('response.invalid',true);}
    if(result?.status!==true || result?.code!=null) throw new WhishError(typeof result?.code==='string'?result.code:'response.invalid',result?.code==='500' || result?.code==null);
    return result;
  }
  return Object.freeze({
    async createPayment({amount,currency,externalId,invoice='',successCallbackUrl,failureCallbackUrl,successRedirectUrl,failureRedirectUrl}) {
      // Caller must persist a server-priced order and externalId BEFORE this call.
      // Reuse that ID on timeout; never generate a second charge reference implicitly.
      if(typeof amount!=='string' || !/^(?:0|[1-9]\d*)(?:\.\d{1,2})?$/.test(amount) || !Number.isFinite(Number(amount))) throw new Error('Amount must be a decimal string');
      if(!['USD','LBP'].includes(currency) || Number(amount)<(currency==='USD'?1:1000) || (currency==='LBP' && amount.includes('.'))) throw new Error('Invalid amount or currency');
      if(typeof externalId!=='string'||!externalId.trim()||externalId.length>128) throw new Error('Persisted externalId required');
      const callbacks={successCallbackUrl,failureCallbackUrl,successRedirectUrl,failureRedirectUrl};
      for(const key of Object.keys(callbacks)) {
        const u=publicUrl(callbacks[key]);
        if(key.includes('Callback')) u.searchParams.set('externalId',externalId);
        callbacks[key]=u.href;
      }
      const result=await request('/payment/whish',{amount,currency,externalId,invoice,...callbacks});
      const url=result?.data?.collectUrl;
      if(typeof url!=='string') throw new WhishError('collect_url.missing',true);
      const u=new URL(url);
      if(u.protocol!=='https:'||u.username||u.password||!(u.hostname==='whish.money'||u.hostname.endsWith('.whish.money'))) throw new WhishError('collect_url.invalid',true);
      return {collectUrl:u.href,externalId,state:'pending'};
    },
    async getPaymentStatus({currency,externalId}) {
      if(!['USD','LBP'].includes(currency)||typeof externalId!=='string'||!externalId) throw new Error('Payment reference required');
      const result=await request('/payment/collect/status',{currency,externalId});
      // Callback/redirect query strings are never proof of payment.
      return {state:paymentState(result)};
    },
    async checkConnection(currency='USD') {
      if(!['USD','LBP'].includes(currency)) throw new Error('Unsupported currency');
      await request('/payment/account/balance?currency='+currency);
      return {connected:true,environment}; // Do not log the merchant balance or credentials.
    }
  });
}
