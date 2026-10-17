import {useEffect, useState} from 'react';
import {Pressable, StyleSheet, Text, View} from 'react-native';
import {supabase} from '../lib/supabase';

type Billing = {monthlyFee:number; currency:string; billingEnabled:boolean; paidUntil:string|null; active:boolean};
export default function Membership(){
 const [billing,setBilling]=useState<Billing|null>(null),[message,setMessage]=useState('Loading membership…'),[busy,setBusy]=useState(false);
 async function load(){
  setBusy(true);
  try{
   const {data,error}=await supabase.rpc('customer_my_billing_status');
   if(error||!data)throw Error('Membership information is not available yet.');
   setBilling(data as Billing);setMessage('');
  }catch(e){setBilling(null);setMessage(e instanceof Error?e.message:'Unable to load membership.');}
  finally{setBusy(false);}
 }
 useEffect(()=>{void load()},[]);
 return <View style={s.card}>
  <Text style={s.title}>MY MEMBERSHIP</Text>
  {billing?<>
   <Text style={s.price}>{Number(billing.monthlyFee).toFixed(2)} {billing.currency} / month</Text>
   <Text style={s.body}>{billing.active?'Active until '+new Date(billing.paidUntil!).toLocaleDateString():billing.billingEnabled?'No active paid membership.':'Membership payments will open at launch.'}</Text>
   <Text style={s.body}>Monthly payments do not renew automatically.</Text>
  </>:<Text accessibilityRole="alert" style={s.body}>{message}</Text>}
  <Pressable accessibilityRole="button" disabled={busy} onPress={()=>void load()} style={s.button}><Text style={s.label}>{busy?'LOADING…':'REFRESH STATUS'}</Text></Pressable>
 </View>;
}
const s=StyleSheet.create({card:{backgroundColor:'#17131f',borderRadius:20,padding:18,marginTop:18},title:{color:'#fff',fontWeight:'900'},price:{color:'#ffd43b',fontSize:20,fontWeight:'800',marginTop:10},body:{color:'#aaaab5',marginTop:8,lineHeight:20},button:{borderWidth:1,borderColor:'#7c3cff',borderRadius:12,padding:12,marginTop:14,alignItems:'center'},label:{color:'#fff',fontWeight:'800'}});
