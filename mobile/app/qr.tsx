import { useEffect,useState } from 'react';
import { Pressable,SafeAreaView,StyleSheet,Text,View } from 'react-native';
import QRCode from 'react-native-qrcode-svg';
import { supabase } from '../lib/supabase';
export default function CustomerQr(){
 const [token,setToken]=useState(''),[expiry,setExpiry]=useState('');
 async function refresh(){const {data}=await supabase.rpc('customer_refresh_qr');const r=Array.isArray(data)?data[0]:data;if(r){setToken(String(r.qr_token||''));setExpiry(r.qr_expires_at?new Date(r.qr_expires_at).toLocaleTimeString():'')}}
 useEffect(()=>{refresh()},[]);
 return <SafeAreaView style={s.safe}><View style={s.page}><Text style={s.title}>MY QR</Text><Text style={s.sub}>Show this QR at a WENIK partner.</Text><View style={s.box}>{token?<QRCode value={token} size={260} backgroundColor="white" color="black"/>:<Text>Loading…</Text>}</View>{expiry?<Text style={s.exp}>Valid until {expiry}</Text>:null}<Pressable style={s.btn} onPress={refresh}><Text style={s.btnText}>REFRESH QR</Text></Pressable></View></SafeAreaView>}
const s=StyleSheet.create({safe:{flex:1,backgroundColor:'#09090d'},page:{flex:1,padding:20,alignItems:'center'},title:{alignSelf:'flex-start',color:'#fff',fontSize:30,fontWeight:'900'},sub:{alignSelf:'flex-start',color:'#aaaab5',marginTop:4,marginBottom:32},box:{backgroundColor:'#fff',padding:20,borderRadius:28,minWidth:300,minHeight:300,alignItems:'center',justifyContent:'center'},exp:{color:'#aaaab5',marginTop:16},btn:{backgroundColor:'#ef159d',borderRadius:17,paddingHorizontal:28,paddingVertical:15,marginTop:18},btnText:{color:'#fff',fontWeight:'900'}});
