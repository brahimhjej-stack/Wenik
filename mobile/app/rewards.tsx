import { useEffect, useState } from 'react';
import { Alert, Image, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import { supabase } from '../lib/supabase';
type Gift={prize_id:string;gift_title:string;gift_description?:string;partner_name?:string;partner_logo_url?:string;points_cost:number;remaining_quantity:number;gift_image_url?:string};
export default function Rewards(){
 const [gifts,setGifts]=useState<Gift[]>([]),[points,setPoints]=useState(0),[busy,setBusy]=useState('');
 async function load(){const [{data:g},{data:p}]=await Promise.all([supabase.rpc('customer_points_reward_catalog'),supabase.rpc('wenik_customer_points_balance')]);setGifts(g||[]);setPoints(Number(p||0))}
 useEffect(()=>{load()},[]);
 async function redeem(g:Gift){if(points<g.points_cost)return Alert.alert('WENIK','You need more points for this gift.');Alert.alert('Redeem gift',`Use ${g.points_cost.toLocaleString()} points for ${g.gift_title}?`,[{text:'Cancel',style:'cancel'},{text:'REDEEM',onPress:async()=>{setBusy(g.prize_id);const {error}=await supabase.rpc('customer_request_points_redemption',{p_prize_id:g.prize_id});setBusy('');if(error)return Alert.alert('WENIK',error.message);Alert.alert('WENIK','Redemption request sent.');load()}}])}
 return <SafeAreaView style={s.safe}><ScrollView contentContainerStyle={s.page}>
  <Text style={s.title}>GIFTS & REWARDS</Text><Text style={s.sub}>Turn your WENIK points into rewards.</Text>
  <View style={s.balance}><Text style={s.balanceLabel}>MY POINTS</Text><Text style={s.balanceValue}>{points.toLocaleString()}</Text></View>
  {gifts.map(g=><View key={g.prize_id} style={s.card}>{g.gift_image_url?<Image source={{uri:g.gift_image_url}} style={s.img}/>:<View style={[s.img,s.placeholder]}><Text style={s.placeholderText}>WENIK</Text></View>}
   <View style={s.body}><Text style={s.partner}>{g.partner_name||'WENIK'}</Text><Text style={s.gift}>{g.gift_title}</Text>{g.gift_description?<Text style={s.desc}>{g.gift_description}</Text>:null}
   <View style={s.row}><View><Text style={s.cost}>{Number(g.points_cost).toLocaleString()} POINTS</Text><Text style={s.qty}>{g.remaining_quantity} available</Text></View><Pressable disabled={busy===g.prize_id||g.remaining_quantity<1} onPress={()=>redeem(g)} style={[s.btn,(points<g.points_cost||g.remaining_quantity<1)&&s.btnDim]}><Text style={s.btnText}>{busy===g.prize_id?'WAIT…':'REDEEM'}</Text></Pressable></View></View>
  </View>)}
  {!gifts.length?<Text style={s.empty}>New WENIK gifts are coming.</Text>:null}
 </ScrollView></SafeAreaView>
}
const s=StyleSheet.create({safe:{flex:1,backgroundColor:'#09090d'},page:{padding:20,paddingBottom:40},title:{color:'#fff',fontSize:28,fontWeight:'900'},sub:{color:'#aaaab5',marginTop:4,marginBottom:16},balance:{backgroundColor:'#17131f',borderRadius:22,padding:18,marginBottom:16},balanceLabel:{color:'#ef159d',fontSize:11,fontWeight:'900',letterSpacing:1.5},balanceValue:{color:'#fff',fontSize:34,fontWeight:'900',marginTop:4},card:{backgroundColor:'#17131f',borderRadius:24,overflow:'hidden',marginBottom:14},img:{width:'100%',aspectRatio:1.7},placeholder:{backgroundColor:'#f4ebff',alignItems:'center',justifyContent:'center'},placeholderText:{color:'#7c3cff',fontSize:24,fontWeight:'900'},body:{padding:16},partner:{color:'#ff7a00',fontSize:11,fontWeight:'900'},gift:{color:'#fff',fontSize:21,fontWeight:'900',marginTop:5},desc:{color:'#aaaab5',marginTop:6,lineHeight:19},row:{flexDirection:'row',alignItems:'center',justifyContent:'space-between',marginTop:16},cost:{color:'#ffd43b',fontWeight:'900'},qty:{color:'#777783',fontSize:11,marginTop:3},btn:{backgroundColor:'#ef159d',paddingHorizontal:18,paddingVertical:12,borderRadius:16},btnDim:{opacity:.45},btnText:{color:'#fff',fontWeight:'900'},empty:{color:'#aaaab5',textAlign:'center',marginTop:30}});
