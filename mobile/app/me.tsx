import { useEffect,useMemo,useState } from 'react';
import { Pressable,SafeAreaView,ScrollView,StyleSheet,Text,TextInput,View } from 'react-native';
import { supabase } from '../lib/supabase';
export default function Me(){
 const [profile,setProfile]=useState<any>(null),[activity,setActivity]=useState<any[]>([]),[inbox,setInbox]=useState<any[]>([]),[q,setQ]=useState('');
 async function load(){const [p,a,i]=await Promise.all([supabase.rpc('customer_my_profile'),supabase.rpc('customer_my_activity',{p_limit:200}),supabase.rpc('customer_my_inbox',{p_limit:50})]);setProfile(Array.isArray(p.data)?p.data[0]:p.data);setActivity(a.data||[]);setInbox(i.data||[])}
 useEffect(()=>{load()},[]);
 const filtered=useMemo(()=>activity.filter(x=>{const h=String([x.partner_name,x.original_amount,x.final_amount].join(' ')).toLowerCase();return !q||h.includes(q.toLowerCase())}),[activity,q]);
 async function openMessage(x:any){if(!x.seen_at){await supabase.rpc('customer_open_message',{p_message_id:x.message_id});load()}}
 return <SafeAreaView style={s.safe}><ScrollView contentContainerStyle={s.page}>
  <Text style={s.title}>ME</Text><Text style={s.sub}>Your WENIK account and activity.</Text>
  <View style={s.profile}><Text style={s.name}>{[profile?.first_name,profile?.last_name].filter(Boolean).join(' ')||'WENIK Member'}</Text><Text style={s.meta}>{profile?.wenik_id||profile?.customer_wenik_id||''}</Text><Text style={s.points}>{Number(profile?.points_balance??profile?.points??0).toLocaleString()} POINTS</Text></View>
  <Text style={s.section}>PURCHASES</Text><TextInput style={s.search} placeholder="Search partner or amount" placeholderTextColor="#777783" value={q} onChangeText={setQ}/>
  {filtered.map((x,i)=><View key={x.transaction_id||i} style={s.card}><View style={s.row}><Text style={s.cardTitle}>{x.partner_name||'WENIK Partner'}</Text><Text style={s.amount}>${Number(x.original_amount||0).toFixed(2)}</Text></View><Text style={s.meta}>{x.transaction_at?new Date(x.transaction_at).toLocaleString():''}</Text><View style={[s.row,{marginTop:8}]}><Text style={s.meta}>Final paid</Text><Text style={s.cardTitle}>${Number(x.final_amount||0).toFixed(2)}</Text></View></View>)}
  {!filtered.length?<View style={s.card}><Text style={s.meta}>No purchases found.</Text></View>:null}
  <Text style={s.section}>NOTIFICATIONS</Text>
  {inbox.map((x,i)=><Pressable key={x.message_id||i} onPress={()=>openMessage(x)} style={[s.card,!x.seen_at&&s.unread]}><View style={s.row}><Text style={s.cardTitle}>{x.title||'WENIK'}</Text>{!x.seen_at?<Text style={s.badge}>NEW</Text>:null}</View><Text style={s.body}>{x.body||''}</Text></Pressable>)}
  {!inbox.length?<View style={s.card}><Text style={s.meta}>No notifications.</Text></View>:null}
  <Pressable style={s.logout} onPress={()=>supabase.auth.signOut()}><Text style={s.logoutText}>LOG OUT</Text></Pressable>
 </ScrollView></SafeAreaView>}
const s=StyleSheet.create({safe:{flex:1,backgroundColor:'#09090d'},page:{padding:20,paddingBottom:50},title:{color:'#fff',fontSize:30,fontWeight:'900'},sub:{color:'#aaaab5',marginTop:4},profile:{backgroundColor:'#17131f',borderRadius:24,padding:20,marginTop:18},name:{color:'#fff',fontSize:23,fontWeight:'900'},meta:{color:'#aaaab5',fontSize:12,marginTop:5},points:{color:'#ffd43b',fontSize:18,fontWeight:'900',marginTop:13},section:{color:'#ff7a00',fontSize:12,fontWeight:'900',letterSpacing:1.4,marginTop:25,marginBottom:9},search:{height:50,borderRadius:16,paddingHorizontal:15,backgroundColor:'#17131f',color:'#fff',marginBottom:10},card:{backgroundColor:'#17131f',borderRadius:19,padding:16,marginBottom:9,borderWidth:1,borderColor:'transparent'},unread:{borderColor:'#ef159d'},row:{flexDirection:'row',justifyContent:'space-between',alignItems:'center'},cardTitle:{color:'#fff',fontWeight:'900',flexShrink:1},amount:{color:'#ffd43b',fontWeight:'900'},body:{color:'#aaaab5',marginTop:8,lineHeight:19},badge:{color:'#fff',backgroundColor:'#ef159d',fontSize:9,fontWeight:'900',paddingHorizontal:8,paddingVertical:4,borderRadius:12},logout:{marginTop:24,borderWidth:1,borderColor:'#ef159d',borderRadius:17,padding:15,alignItems:'center'},logoutText:{color:'#ef159d',fontWeight:'900'}});
