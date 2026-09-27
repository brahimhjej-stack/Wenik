import { useEffect,useState } from 'react';
import { ActivityIndicator,Pressable,SafeAreaView,ScrollView,StyleSheet,Text,View,Platform } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import type { Session } from '@supabase/supabase-js';
import Partners from './partners'; import Rewards from './rewards'; import Wins from './wins'; import Iza from './iza'; import CustomerQr from './qr'; import Me from './me';
import Auth from '../components/Auth'; import { supabase } from '../lib/supabase';

const C={bg:'#f8f7fb',panel:'#fff',line:'rgba(92,55,110,.12)',text:'#18141d',muted:'#77717e',purple:'#8f24ff',pink:'#ef159d',orange:'#ff6f21',yellow:'#ffd21c'};
type Screen='home'|'partners'|'rewards'|'wins'|'iza'|'qr'|'me';
const nav:[Screen,string][]=[['home','HOME'],['wins','WIN'],['iza','IZA'],['qr','QR'],['partners','PARTNERS'],['me','ME']];

function BottomNav({screen,setScreen,unread}:{screen:Screen,setScreen:(x:Screen)=>void,unread:number}){
 return <SafeAreaView style={s.navSafe}><View style={s.nav}>{nav.map(([id,label])=>{
  const on=screen===id;
  return <Pressable key={id} style={[s.navItem,on&&s.navActive]} onPress={()=>setScreen(id)}>
   <View><Text style={[s.navLabel,on&&s.navOn]}>{label}</Text>{id==='me'&&unread>0?<Text style={s.unread}>{unread>99?'99+':unread}</Text>:null}</View>
  </Pressable>})}</View></SafeAreaView>
}

function Brand(){
 return <View style={s.brand}><LinearGradient colors={[C.purple,C.pink,C.orange,C.yellow]} start={{x:0,y:0}} end={{x:1,y:1}} style={s.brandMark}><Text style={s.brandW}>W.</Text></LinearGradient><View><Text style={s.logo}>WENIK</Text><Text style={s.winwin}>WIN WIN</Text></View></View>
}

function Hero(){
 return <LinearGradient colors={['#b978f3','#f58bc5','#ffad86']} start={{x:0,y:0}} end={{x:1,y:1}} style={s.hero}>
  <LinearGradient colors={[C.purple,C.pink,C.orange,C.yellow]} start={{x:0,y:0}} end={{x:1,y:0}} style={s.heroLine}/>
  <Text style={s.eyebrow}>YOUR WENIK</Text>
  <Text style={s.title}>Everything starts here.</Text>
  <Text style={s.copy}>Discover partners, unlock benefits and keep your next win close.</Text>
 </LinearGradient>
}

function Home(){
 const [screen,setScreen]=useState<Screen>('home'),[profile,setProfile]=useState<any>(null),[unread,setUnread]=useState(0);
 async function refresh(){const [p,u]=await Promise.all([supabase.rpc('customer_my_profile'),supabase.rpc('customer_my_inbox',{p_limit:50})]);if(!p.error)setProfile(Array.isArray(p.data)?p.data[0]:p.data);if(!u.error)setUnread((u.data||[]).filter((x:any)=>!x.seen_at).length)}
 useEffect(()=>{refresh()},[screen]);
 const profilePoints=profile?.points_balance??profile?.points;
 const [livePoints,setLivePoints]=useState<number|null>(null);
 useEffect(()=>{let active=true;supabase.rpc('wenik_customer_points_balance').then(({data,error})=>{if(active&&!error)setLivePoints(Number(data??0))});return()=>{active=false}},[screen]);
 const points=livePoints??profilePoints??0;
 let body;
 if(screen==='partners')body=<Partners/>;else if(screen==='rewards')body=<Rewards/>;else if(screen==='wins')body=<Wins/>;else if(screen==='iza')body=<Iza/>;else if(screen==='qr')body=<CustomerQr/>;else if(screen==='me')body=<Me/>;else body=<SafeAreaView style={s.safe}><ScrollView contentContainerStyle={s.page} showsVerticalScrollIndicator={false}>
   <Brand/><Hero/>
   <View style={s.sectionHead}><Text style={s.sectionTitle}>MY WENIK</Text></View>
   <LinearGradient colors={['#ffffff','#fffafd']} style={s.pointsCard}>
    <View><Text style={s.pointsLabel}>MY POINTS</Text><Text style={s.pointsValue}>{Number(points||0).toLocaleString()}</Text></View>
    <Pressable onPress={()=>setScreen('rewards')}><LinearGradient colors={[C.purple,C.pink,C.orange]} start={{x:0,y:0}} end={{x:1,y:0}} style={s.action}><Text style={s.actionText}>REWARDS</Text></LinearGradient></Pressable>
   </LinearGradient>
   <View style={s.sectionHead}><Text style={s.sectionTitle}>DISCOVER</Text></View>
   <View style={s.grid}>
    <Pressable style={s.tile} onPress={()=>setScreen('partners')}><Text style={s.tileKicker}>WENIK</Text><Text style={s.tileTitle}>PARTNERS</Text><Text style={s.tileSub}>Discover benefits</Text></Pressable>
    <Pressable style={s.tile} onPress={()=>setScreen('wins')}><Text style={[s.tileKicker,{color:C.yellow}]}>YOUR</Text><Text style={s.tileTitle}>WIN</Text><Text style={s.tileSub}>Wins & winners</Text></Pressable>
    <Pressable style={s.tile} onPress={()=>setScreen('iza')}><Text style={[s.tileKicker,{color:C.orange}]}>IZA | إذا</Text><Text style={s.tileTitle}>I'M IN?</Text><Text style={s.tileSub}>Vote & participate</Text></Pressable>
    <Pressable style={s.tile} onPress={()=>setScreen('qr')}><Text style={[s.tileKicker,{color:C.pink}]}>YOUR ACCESS</Text><Text style={s.tileTitle}>MY QR</Text><Text style={s.tileSub}>Scan at a partner</Text></Pressable>
   </View>
 </ScrollView></SafeAreaView>;
 return <View style={s.shell}>{body}<BottomNav screen={screen} setScreen={setScreen} unread={unread}/></View>
}

export default function Index(){
 const [session,setSession]=useState<Session|null|undefined>(undefined);
 useEffect(()=>{supabase.auth.getSession().then(({data})=>setSession(data.session));const {data}=supabase.auth.onAuthStateChange((_e,n)=>setSession(n));return()=>data.subscription.unsubscribe()},[]);
 if(session===undefined)return <View style={s.loading}><ActivityIndicator size="large"/><Text style={s.loadingText}>WENIK</Text></View>;
 return session?<Home/>:<Auth/>
}

const s=StyleSheet.create({
 shell:{flex:1,backgroundColor:C.bg},safe:{flex:1,backgroundColor:C.bg},page:{paddingHorizontal:14,paddingTop:8,paddingBottom:120},
 loading:{flex:1,backgroundColor:C.bg,alignItems:'center',justifyContent:'center'},loadingText:{color:'#fff',fontWeight:'900',letterSpacing:3,marginTop:12},
 brand:{flexDirection:'row',alignItems:'center',justifyContent:'center',gap:11,marginTop:4,marginBottom:18},brandMark:{width:48,height:48,borderRadius:24,alignItems:'center',justifyContent:'center'},brandW:{fontSize:22,fontWeight:'900',color:'#fff',letterSpacing:-1},logo:{color:'#18141d',fontSize:27,fontWeight:'900',letterSpacing:2.8,lineHeight:30},winwin:{color:C.pink,fontSize:10,fontWeight:'900',letterSpacing:4,marginTop:1},
 hero:{borderRadius:26,padding:22,overflow:'hidden',borderWidth:1,borderColor:'rgba(255,255,255,.08)'},heroLine:{position:'absolute',top:0,left:0,right:0,height:3},
 eyebrow:{fontSize:11,letterSpacing:2,color:'#fff',fontWeight:'800'},title:{color:'#fff',fontSize:30,fontWeight:'900',letterSpacing:-1,marginTop:6},copy:{color:'rgba(255,255,255,.92)',fontSize:13,lineHeight:20,marginTop:5},
 sectionHead:{marginTop:24,marginHorizontal:2,marginBottom:8},sectionTitle:{color:'#18141d',fontSize:18,fontWeight:'900',letterSpacing:.2},
 pointsCard:{borderRadius:22,padding:18,borderWidth:1,borderColor:C.line,flexDirection:'row',alignItems:'center',justifyContent:'space-between'},
 pointsLabel:{color:'#8d8490',fontSize:11,fontWeight:'900',letterSpacing:1.7},pointsValue:{color:'#18141d',fontSize:34,fontWeight:'900',marginTop:2},
 action:{borderRadius:14,paddingVertical:11,paddingHorizontal:15},actionText:{color:'#fff',fontSize:11,fontWeight:'900',letterSpacing:.7},
 grid:{flexDirection:'row',flexWrap:'wrap',gap:10},tile:{width:'48.5%',minHeight:128,backgroundColor:'#fff',borderWidth:1,borderColor:C.line,borderRadius:22,padding:17,justifyContent:'flex-end'},
 tileKicker:{color:C.purple,fontSize:10,fontWeight:'900',letterSpacing:1.6,marginBottom:8},tileTitle:{color:'#18141d',fontSize:18,fontWeight:'900'},tileSub:{color:C.muted,fontSize:12,marginTop:5,lineHeight:17},
 navSafe:{backgroundColor:'transparent',paddingBottom:Platform.OS==='android'?18:2},nav:{marginHorizontal:9,marginBottom:4,backgroundColor:'rgba(255,255,255,.96)',borderWidth:1,borderColor:'rgba(90,65,100,.10)',borderRadius:22,padding:7,flexDirection:'row',minHeight:62},
 navItem:{flex:1,alignItems:'center',justifyContent:'center',borderRadius:14,paddingVertical:9,paddingHorizontal:1},navActive:{backgroundColor:'rgba(239,21,157,.10)'},navLabel:{color:'#746d79',fontSize:8,fontWeight:'900'},navOn:{color:'#6f35e8'},
 unread:{position:'absolute',right:-9,top:-10,backgroundColor:C.pink,color:'#fff',fontSize:7,fontWeight:'900',minWidth:16,height:16,borderRadius:8,textAlign:'center',lineHeight:16,paddingHorizontal:2}
});
