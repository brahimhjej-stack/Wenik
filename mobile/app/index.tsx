import { useEffect, useState } from 'react';
import { ActivityIndicator, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import Partners from './partners';
import Rewards from './rewards';
import Wins from './wins';
import type { Session } from '@supabase/supabase-js';
import Auth from '../components/Auth';
import { supabase } from '../lib/supabase';

const colors={background:'#09090d',surface:'#14141b',text:'#fff',muted:'#aaaab5',pink:'#ef159d',orange:'#ff7a00',yellow:'#ffd43b',purple:'#7c3cff'};
const items=[['WIN','Gifts & rewards'],['IZA','Vote & participate'],['QR','Scan at partners'],['Partners','Discover WENIK partners']];

function Home(){
  const [screen,setScreen]=useState<'home'|'partners'|'rewards'|'wins'>('home');
  const [profile,setProfile]=useState<any>(null);
  useEffect(()=>{(async()=>{
    const {data,error}=await supabase.rpc('customer_my_profile');
    if(!error) setProfile(Array.isArray(data)?data[0]:data);
  })()},[]);
  const points=profile?.points_balance??profile?.points??0;
  const name=profile?.first_name||'';
  if(screen!=='home'){const Page=screen==='partners'?Partners:screen==='rewards'?Rewards:Wins;return <View style={{flex:1}}><Pressable onPress={()=>setScreen('home')} style={{backgroundColor:'#09090d',paddingHorizontal:20,paddingTop:12}}><Text style={{color:'#ef159d',fontWeight:'900'}}>‹ HOME</Text></Pressable><Page/></View>}
  return <SafeAreaView style={s.safe}><ScrollView contentContainerStyle={s.page}>
    <View style={s.brand}><Text style={s.logo}>WENIK</Text><Text style={s.winwin}>WIN WIN</Text></View>
    <View style={s.hero}><Text style={s.eyebrow}>{name?'WELCOME '+String(name).toUpperCase():'WELCOME TO WENIK'}</Text><Text style={s.title}>Everything starts here.</Text><Text style={s.copy}>Discover partners, collect points and unlock rewards.</Text></View>
    <View style={s.points}><Text style={s.pointsLabel}>MY POINTS</Text><Text style={s.pointsValue}>{Number(points||0).toLocaleString()}</Text><Text style={s.pointsSub}>Your WENIK balance</Text></View>
    <View style={s.grid}>{items.map(([title,sub],i)=><Pressable key={title} style={s.card} onPress={()=>title==='Partners'?setScreen('partners'):title==='WIN'?setScreen('wins'):title==='Gifts & rewards'?setScreen('rewards'):undefined}><View style={[s.dot,{backgroundColor:[colors.pink,colors.orange,colors.yellow,colors.purple][i]}]}/><Text style={s.cardTitle}>{title}</Text><Text style={s.cardSub}>{sub}</Text></Pressable>)}</View>
  </ScrollView></SafeAreaView>
}
export default function Index(){
  const [session,setSession]=useState<Session|null|undefined>(undefined);
  useEffect(()=>{supabase.auth.getSession().then(({data})=>setSession(data.session));const {data}=supabase.auth.onAuthStateChange((_e,next)=>setSession(next));return()=>data.subscription.unsubscribe()},[]);
  if(session===undefined)return <View style={s.loading}><ActivityIndicator size="large"/><Text style={s.loadingText}>WENIK</Text></View>;
  return session?<Home/>:<Auth/>;
}
const s=StyleSheet.create({
  safe:{flex:1,backgroundColor:colors.background},page:{padding:20,paddingBottom:40},loading:{flex:1,backgroundColor:colors.background,alignItems:'center',justifyContent:'center'},loadingText:{color:'#fff',fontWeight:'900',letterSpacing:3,marginTop:12},
  brand:{alignItems:'center',marginTop:12,marginBottom:24},logo:{color:colors.text,fontSize:32,fontWeight:'900',letterSpacing:3},winwin:{color:colors.pink,fontSize:12,fontWeight:'800',letterSpacing:4,marginTop:3},
  hero:{backgroundColor:colors.surface,borderRadius:28,padding:24,marginBottom:12},eyebrow:{color:colors.orange,fontSize:12,fontWeight:'800',letterSpacing:1.5},title:{color:colors.text,fontSize:30,fontWeight:'900',marginTop:8},copy:{color:colors.muted,fontSize:15,marginTop:8,lineHeight:22},
  points:{backgroundColor:colors.surface,borderRadius:22,padding:20,marginBottom:12},pointsLabel:{color:colors.pink,fontSize:12,fontWeight:'900',letterSpacing:1.5},pointsValue:{color:'#fff',fontSize:34,fontWeight:'900',marginTop:4},pointsSub:{color:colors.muted,fontSize:13},
  grid:{flexDirection:'row',flexWrap:'wrap',gap:12},card:{width:'48%',minHeight:150,backgroundColor:colors.surface,borderRadius:22,padding:18},dot:{width:12,height:12,borderRadius:6,marginBottom:22},cardTitle:{color:colors.text,fontSize:20,fontWeight:'900'},cardSub:{color:colors.muted,fontSize:13,marginTop:7,lineHeight:18}
});
