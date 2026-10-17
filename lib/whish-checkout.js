import {createHmac,timingSafeEqual} from 'node:crypto';
const uuid=/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
export function callbackToken(id,secret){return createHmac('sha256',secret).update(id).digest('hex');}
export function createCheckoutService({store,provider,origin,callbackSecret,environment='sandbox'}) {
 if(!callbackSecret||callbackSecret.length<32)throw Error('Callback secret not configured');
 const site=new URL(origin);if(site.protocol!=='https:')throw Error('HTTPS site required');
 async function reconcile(order){
  if(order.environment!==environment)throw Error('Environment mismatch');
  const result=await provider.getPaymentStatus({externalId:order.id,currency:order.currency});
  return store.reconcile(order.id,environment,result.state);
 }
 return {
  async create(user,kind,statementId){
   if(!user||!['customer','partner'].includes(kind))throw Error('Invalid checkout');
   if(kind==='partner'&&!uuid.test(statementId||''))throw Error('Choose a monthly statement');
   let order=kind==='partner'?await store.prepareStatement(user,statementId,environment):await store.prepare(user,kind,environment);
   if(order.trial)return order;
   if(order.environment!==environment||order.auth_user_id!==user)throw Error('Order ownership mismatch');
   if(order.collect_url){
    const verified=await reconcile(order);
    if(verified.state==='success')return {externalId:order.id,state:'success'};
    if(verified.state==='refunded')throw Error('Refunded order needs review');
    if(verified.state==='failed'){
     const previousId=order.id;
     order=kind==='partner'?await store.prepareStatement(user,statementId,environment):await store.prepare(user,kind,environment);
     if(order.id===previousId||order.environment!==environment||order.auth_user_id!==user||order.collect_url)throw Error('Unable to renew expired payment');
    }else return {externalId:order.id,collectUrl:order.collect_url,amount:order.amount,currency:order.currency};
   }
   const callback=new URL('/api/whish/callback',site);callback.searchParams.set('externalId',order.id);callback.searchParams.set('token',callbackToken(order.id,callbackSecret));
   const redirect=new URL('/whish-payment.html',site);redirect.searchParams.set('order',order.id);
   const result=await provider.createPayment({amount:Number(order.amount).toFixed(2),currency:order.currency,externalId:order.id,invoice:kind==='partner'?'WENIK monthly statement '+order.invoice_no:'WENIK customer monthly subscription',successCallbackUrl:callback.href,failureCallbackUrl:callback.href,successRedirectUrl:redirect.href,failureRedirectUrl:redirect.href});
   await store.setCollectUrl(order.id,result.collectUrl);
   return {externalId:order.id,collectUrl:result.collectUrl,amount:order.amount,currency:order.currency};
  },
  async status(user,id){
   if(!uuid.test(id))throw Error('Invalid reference');
   const o=await store.get(id);if(!o||o.auth_user_id!==user)throw Error('Not authorized');
   return reconcile(o);
  },
  async callback(id,token){
   if(!uuid.test(id)||!/^\w{64}$/.test(token||''))throw Error('Invalid callback');
   const expected=callbackToken(id,callbackSecret);if(!timingSafeEqual(Buffer.from(expected),Buffer.from(token)))throw Error('Invalid callback');
   const o=await store.get(id);if(!o)throw Error('Unknown order');
   // Both failure and success callbacks execute the SAME verified status flow.
   return reconcile(o);
  }
 };
}
