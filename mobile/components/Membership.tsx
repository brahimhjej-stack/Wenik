import {useCallback, useEffect, useState} from 'react';
import {AppState, Pressable, StyleSheet, Text, View} from 'react-native';
import {supabase} from '../lib/supabase';

type Billing = {monthlyFee:number; currency:string; billingEnabled:boolean; paidUntil:string|null; active:boolean};
export default function Membership({onView,refreshKey=0}:{onView?:()=>void;refreshKey?:number}){
 const [billing,setBilling]=useState<Billing|null>(null),[message,setMessage]=useState('Loading membership…'),[busy,setBusy]=useState(false);
 const load=useCallback(async ()=>{
  setBusy(true);
  try{
   const {data,error}=await supabase.rpc('customer_my_billing_status');
   if(error||!data)throw Error('Membership information is not available yet.');
   setBilling(data as Billing);setMessage('');
  }catch(e){setBilling(null);setMessage(e instanceof Error?e.message:'Unable to load membership.');}
  finally{setBusy(false);}
 },[]);
 useEffect(()=>{void load()},[load,refreshKey]);
 useEffect(()=>{
  let previous=AppState.currentState;
  const listener=AppState.addEventListener('change',next=>{
   if(next==='active'&&previous!=='active')void load();
   previous=next;
  });
  return ()=>listener.remove();
 },[load]);
 const expiry=billing?.paidUntil?new Date(billing.paidUntil):null;
 const daysLeft=expiry?Math.ceil((expiry.getTime()-Date.now())/86400000):null;
 const expiresSoon=billing?.billingEnabled&&billing.active&&daysLeft!==null&&daysLeft<=7;
 return <View style={s.card}>
  <Text style={s.title}>MY MEMBERSHIP · اشتراكي</Text>
  {billing?<>
   <Text style={s.price}>{Number(billing.monthlyFee).toFixed(2)} {billing.currency} / month</Text>
   <Text style={s.body}>{billing.active?'Active until '+new Date(billing.paidUntil!).toLocaleDateString()+' · اشتراكك فعّال':billing.billingEnabled?'No active paid membership · لا يوجد اشتراك فعّال':'Membership payments will open at launch.'}</Text>
   <Text style={s.body}>Monthly payments do not renew automatically.</Text>
   {expiresSoon?<Text accessibilityRole="alert" style={s.notice}>Your membership expires soon. There is no automatic monthly charge.</Text>:null}
  </>:<Text accessibilityRole="alert" style={s.body}>{message}</Text>}
  {onView?<Pressable accessibilityRole="button" onPress={onView} style={s.viewButton}><Text style={s.viewLabel}>VIEW MEMBERSHIP · عرض الاشتراك</Text></Pressable>:null}
  <Pressable accessibilityRole="button" disabled={busy} onPress={()=>void load()} style={s.button}><Text style={s.label}>{busy?'LOADING…':'REFRESH STATUS'}</Text></Pressable>
 </View>;
}
const s=StyleSheet.create({card:{backgroundColor:'#fff',borderRadius:24,padding:20,marginTop:18,marginBottom:4,borderWidth:1,borderColor:'rgba(143,36,255,.12)'},title:{color:'#18141d',fontWeight:'900',fontSize:17},price:{color:'#8f24ff',fontSize:20,fontWeight:'800',marginTop:10},notice:{color:'#8f24ff',marginTop:10,lineHeight:22},body:{color:'#77717e',marginTop:8,lineHeight:20},button:{borderWidth:1,borderColor:'#7c3cff',borderRadius:12,padding:12,marginTop:14,alignItems:'center'},label:{color:'#8f24ff',fontWeight:'800'},viewButton:{backgroundColor:'#8f24ff',padding:15,borderRadius:16,alignItems:'center',marginTop:16},viewLabel:{color:'#fff',fontWeight:'900'}});
