import {createWhishPay,WhishError} from '../../lib/whish-pay.js';
import {createCheckoutService} from '../../lib/whish-checkout.js';

export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');
 res.setHeader('Content-Type','application/json');
 res.setHeader('Referrer-Policy','no-referrer');
 const send=(status,data)=>res.status(status).json(data);
 try{
  const env=process.env;
  const environment=env.WHISH_ENVIRONMENT||'sandbox';
  const liveApproved=environment==='production'&&env.VERCEL_ENV==='production'&&env.WHISH_LIVE_CHECKOUT_APPROVED==='true';
  const checkoutEnabled=env.WHISH_CHECKOUT_ENABLED==='true'&&(environment==='sandbox'||liveApproved);
  if(req.query.action==='config'){
   if(req.method!=='GET')return send(405,{error:'Method not allowed'});
   if(!env.SUPABASE_URL||!env.SUPABASE_PUBLISHABLE_KEY)return send(503,{error:'Payment page is not configured yet'});
   return send(200,{supabaseUrl:env.SUPABASE_URL,publishableKey:env.SUPABASE_PUBLISHABLE_KEY,environment,checkoutEnabled,nativeCheckoutEnabled:false});
  }
  if(env.WHISH_CHECKOUT_ENABLED!=='true')return send(503,{error:'Checkout is not enabled yet'});
  // Production credentials must never enable a preview or bypass release approval.
  if(environment!=='sandbox'&&!liveApproved)return send(503,{error:'Live checkout is not enabled yet'});
  const supabase=env.SUPABASE_URL,serviceKey=env.SUPABASE_SERVICE_ROLE_KEY;
  if(!supabase||!serviceKey)throw Error('Missing server configuration');
  const origin=new URL(env.VERCEL_ENV==='preview'&&env.VERCEL_URL?'https://'+env.VERCEL_URL:env.WHISH_SITE_URL).origin;
  async function rest(path,{body,token=serviceKey,method=body?'POST':'GET'}={}){
   const r=await fetch(supabase+'/rest/v1/'+path,{method,redirect:'error',signal:AbortSignal.timeout(10000),headers:{apikey:serviceKey,Authorization:'Bearer '+token,'Content-Type':'application/json'},...(body?{body:JSON.stringify(body)}:{})});
   if(!r.ok)throw Error('Database operation failed');
   return r.status===204?null:r.json();
  }
  const rpc=(name,body)=>rest('rpc/'+name,{body});
  const store={
   prepareStatement:(user,statement,environment)=>rpc('whish_prepare_statement_order',{p_user:user,p_statement:statement,p_environment:environment}),
   prepare:(user,kind,environment)=>rpc('whish_prepare_order',{p_user:user,p_kind:kind,p_environment:environment}),
   get:async id=>(await rest('whish_checkout_orders?id=eq.'+encodeURIComponent(id)+'&select=*'))?.[0],
   setCollectUrl:(id,url)=>rest('whish_checkout_orders?id=eq.'+encodeURIComponent(id),{method:'PATCH',body:{collect_url:url}}),
   reconcile:(id,environment,state)=>rpc('whish_reconcile_order',{p_order:id,p_environment:environment,p_state:state})
  };
  const provider=createWhishPay({channel:env.WHISH_CHANNEL,secret:env.WHISH_SECRET,websiteUrl:env.WHISH_WEBSITE_URL,userAgent:'WENIK/1.0 ('+origin+'; billing)',environment,allowProduction:liveApproved});
  const app=createCheckoutService({store,provider,origin,callbackSecret:env.WHISH_CALLBACK_SECRET,environment});
  const action=req.query.action;
  if(action==='callback'){
   if(req.method!=='GET')return send(405,{error:'Method not allowed'});
   const result=await app.callback(req.query.externalId,req.query.token);
   return send(200,{received:true,state:result.state});
  }
  const match=String(req.headers.authorization||'').match(/^Bearer (\S+)$/);
  if(!match)return send(401,{error:'Sign in required'});
  const userResponse=await fetch(supabase+'/auth/v1/user',{headers:{apikey:serviceKey,Authorization:'Bearer '+match[1]},signal:AbortSignal.timeout(10000),redirect:'error'});
  if(!userResponse.ok)return send(401,{error:'Sign in required'});
  const user=await userResponse.json();if(!user.id)return send(401,{error:'Sign in required'});
  if(action==='create'){
   if(req.method!=='POST')return send(405,{error:'Method not allowed'});
   if(req.headers.origin&&req.headers.origin!==origin)return send(403,{error:'Origin not allowed'});
   const pilotUsers=(env.WHISH_LIVE_ALLOWED_USERS||'').split(',').map(x=>x.trim()).filter(Boolean);
   if(environment==='production'&&pilotUsers.length&&!pilotUsers.includes(user.id))return send(503,{error:'Live payments are being verified. Please try again later.'});
   const body=typeof req.body==='string'?JSON.parse(req.body):req.body;
   return send(200,await app.create(user.id,body?.kind,body?.statementId));
  }
  if(action==='status'){
   if(req.method!=='GET')return send(405,{error:'Method not allowed'});
   const result=await app.status(user.id,req.query.externalId);const order=await store.get(req.query.externalId);return send(200,{...result,kind:order.kind,amount:order.amount,currency:order.currency,invoiceNo:order.invoice_no,environment:order.environment});
  }
  return send(404,{error:'Not found'});
 }catch(e){
  // Provider text, secret headers, user data and callback tokens are not logged.
  if(e instanceof WhishError)return send(e.uncertain?202:502,{state:e.uncertain?'unknown':'pending',error:e.uncertain?'Payment is being verified. Check again shortly.':'Payment provider could not create or verify this payment.'});
  return send(400,{error:'Unable to process this payment. Please sign in and try again.'});
 }
}
