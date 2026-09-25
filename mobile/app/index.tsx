import { useEffect,useState } from 'react';
import { ActivityIndicator,Pressable,SafeAreaView,ScrollView,StyleSheet,Text,View } from 'react-native';
import type { Session } from '@supabase/supabase-js';
import Partners from './partners'; import Rewards from './rewards'; import Wins from './wins'; import Iza from './iza'; import CustomerQr from './qr'; import Me from './me';
import Auth from '../components/Auth'; import { supabase } from '../lib/supabase';
const C={bg:'#09090d',surface:'#14141b',text:'#fff',muted:'#aaaab5',pink:'#ef159d',orange:'#ff7a00',yellow:'#ffd43b',purple:'#7c3cff'};
type Screen='home'|'partners'|'rewards'|'wins'|'iza'|'qr'|'me';
const nav:[Screen,string,string][]=[['home','⌂','HOME'],['partners','⌕','PARTNERS'],['qr','▣','QR'],['wins','★','WIN'],['me','●','ME']];
function BottomNav({screen,setScreen,unread}:{screen:Screen,setScreen:(x:Screen)=>void,unread:number}){return <View style={s.nav}>{nav.map(([id,icon,label])=><Pressable key={id} style={s.navItem} onPress={()=>setScreen(id)}><View><Text style={[s.navIcon,screen===id&&s.navOn]}>{icon}</Text>{id==='me'&&unread>0?<Text style={s.unread}>{unread>99?'99+':unread}</Text>:null}</View><Text style={[s.navLabel,screen===id&&s.navOn]}>{label}</Text></Pressable>)}</View>}
function Home(){
 const [screen,setScreen]=useState<Screen>('home'),[profile,setProfile]=useState<any>(null),[unread,setUnread]=useState(0);
 async function refresh(){const [p,u]=await Promise.all([supabase.rpc('customer_my_profile'),supabase.rpc('customer_unread_message_count')]);if(!p.error)setProfile(Array.isArray(p.data)?p.data[0]:p.data);setUnread(Number(u.data||0))}
 useEffect(()=>{refresh()},[screen]);
 const points=profile?.points_balance??profile?.points??0,name=profile?.first_name||'';
 let body;
 if(screen==='partners')body=<Partners/>;else if(screen==='rewards')body=<Rewards/>;else if(screen==='wins')body=<Wins/>;else if(screen==='iza')body=<Iza/>;else if(screen==='qr')body=<CustomerQr/>;else if(screen==='me')body=<Me/>;else body=<SafeAreaView style={s.safe}><ScrollView contentContainerStyle={s.page}>
  <View style={s.brand}><Text style={s.logo}>WENIK</Text><Text style={s.winwin}>WIN WIN</Text></View>
  <View style={s.hero}><Text style={s.eyebrow}>{name?'WELCOME '+String(name).toUpperCase():'WELCOME TO WENIK'}</Text><Text style={s.title}>Everything starts here.</Text><Text style={s.copy}>Discover partners, collect points and unlock rewards.</Text></View>
  <Pressable style={s.points} onPress={()=>setScreen('rewards')}><Text style={s.pointsLabel}>MY POINTS</Text><Text style={s.pointsValue}>{Number(points||0).toLocaleString()}</Text><Text style={s.pointsSub}>Tap to explore rewards</Text></Pressable>
  <View style={s.grid}>
   <Pressable style={s.card} onPress={()=>setScreen('rewards')}><View style={[s.dot,{backgroundColor:C.pink}]}/><Text style={s.cardTitle}>REWARDS</Text><Text style={s.cardSub}>Gifts you can redeem</Text></Pressable>
   <Pressable style={s.card} onPress={()=>setScreen('iza')}><View style={[s.dot,{backgroundColor:C.orange}]}/><Text style={s.cardTitle}>IZA</Text><Text style={s.cardSub}>Vote & participate</Text></Pressable>
   <Pressable style={s.card} onPress={()=>setScreen('partners')}><View style={[s.dot,{backgroundColor:C.purple}]}/><Text style={s.cardTitle}>PARTNERS</Text><Text style={s.cardSub}>Discover benefits</Text></Pressable>
   <Pressable style={s.card} onPress={()=>setScreen('wins')}><View style={[s.dot,{backgroundColor:C.yellow}]}/><Text style={s.cardTitle}>WIN</Text><Text style={s.cardSub}>Wins & winners</Text></Pressable>
  </View>
 </ScrollView></SafeAreaView>;
 return <View style={s.shell}>{body}<BottomNav screen={screen} setScreen={setScreen} unread={unread}/></View>
}
export default function Index(){const [session,setSession]=useState<Session|null|undefined>(undefined);useEffect(()=>{supabase.auth.getSession().then(({data})=>setSession(data.session));const {data}=supabase.auth.onAuthStateChange((_e,n)=>setSession(n));return()=>data.subscription.unsubscribe()},[]);if(session===undefined)return <View style={s.loading}><ActivityIndicator size="large"/><Text style={s.loadingText}>WENIK</Text></View>;return session?<Home/>:<Auth/>}
const s=StyleSheet.create({
 shell:{flex:1,backgroundColor:C.bg},safe:{flex:1,backgroundColor:C.bg},page:{padding:20,paddingBottom:110},loading:{flex:1,backgroundColor:C.bg,alignItems:'center',justifyContent:'center'},loadingText:{color:'#fff',fontWeight:'900',letterSpacing:3,marginTop:12},
 brand:{alignItems:'center',marginTop:12,marginBottom:24},logo:{color:C.text,fontSize:32,fontWeight:'900',letterSpacing:3},winwin:{color:C.pink,fontSize:12,fontWeight:'800',letterSpacing:4,marginTop:3},
 hero:{backgroundColor:C.surface,borderRadius:28,padding:24,marginBottom:12},eyebrow:{color:C.orange,fontSize:12,fontWeight:'800',letterSpacing:1.5},title:{color:C.text,fontSize:30,fontWeight:'900',marginTop:8},copy:{color:C.muted,fontSize:15,marginTop:8,lineHeight:22},
 points:{backgroundColor:C.surface,borderRadius:22,padding:20,marginBottom:12},pointsLabel:{color:C.pink,fontSize:12,fontWeight:'900',letterSpacing:1.5},pointsValue:{color:'#fff',fontSize:34,fontWeight:'900',marginTop:4},pointsSub:{color:C.muted,fontSize:13},
 grid:{flexDirection:'row',flexWrap:'wrap',gap:12},card:{width:'48%',minHeight:142,backgroundColor:C.surface,borderRadius:22,padding:18},dot:{width:12,height:12,borderRadius:6,marginBottom:22},cardTitle:{color:C.text,fontSize:18,fontWeight:'900'},cardSub:{color:C.muted,fontSize:13,marginTop:7,lineHeight:18},
 nav:{height:78,backgroundColor:'#111117',borderTopWidth:1,borderTopColor:'#24242d',flexDirection:'row',paddingBottom:8,paddingTop:7},navItem:{flex:1,alignItems:'center',justifyContent:'center'},navIcon:{color:'#777783',fontSize:20,fontWeight:'900'},navLabel:{color:'#777783',fontSize:9,fontWeight:'900',marginTop:3},navOn:{color:C.pink},unread:{position:'absolute',right:-12,top:-6,backgroundColor:C.pink,color:'#fff',fontSize:8,fontWeight:'900',minWidth:17,height:17,borderRadius:9,textAlign:'center',lineHeight:17,paddingHorizontal:3}
});
