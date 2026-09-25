import { useEffect, useState } from 'react';
import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import { supabase } from '../lib/supabase';
export default function Wins(){
 const [mine,setMine]=useState<any[]>([]),[recent,setRecent]=useState<any[]>([]);
 useEffect(()=>{Promise.all([supabase.rpc('customer_my_wins'),supabase.rpc('public_recent_winners',{p_limit:20})]).then(([a,b])=>{setMine(a.data||[]);setRecent(b.data||[])})},[]);
 return <SafeAreaView style={s.safe}><ScrollView contentContainerStyle={s.page}><Text style={s.title}>WIN</Text><Text style={s.sub}>Your wins and recent WENIK winners.</Text>
 <Text style={s.section}>MY WINS</Text>{mine.length?mine.map((x,i)=><View key={x.id||i} style={s.card}><Text style={s.eye}>YOUR WIN</Text><Text style={s.win}>🎉 {x.prize_name||'Prize'}</Text><Text style={s.muted}>Congratulations! You won with WENIK.</Text></View>):<View style={s.card}><Text style={s.muted}>No wins yet.</Text></View>}
 <Text style={s.section}>RECENT WINNERS</Text>{recent.length?recent.map((x,i)=><View key={x.id||i} style={s.card}><View style={s.row}><Text style={s.name}>{x.public_display_name||'Winner'}</Text><Text style={s.badge}>WINNER</Text></View></View>):<View style={s.card}><Text style={s.muted}>No announced winners.</Text></View>}
 </ScrollView></SafeAreaView>}
const s=StyleSheet.create({safe:{flex:1,backgroundColor:'#09090d'},page:{padding:20,paddingBottom:40},title:{color:'#fff',fontSize:30,fontWeight:'900'},sub:{color:'#aaaab5',marginTop:4},section:{color:'#ff7a00',fontSize:12,fontWeight:'900',letterSpacing:1.4,marginTop:24,marginBottom:9},card:{backgroundColor:'#17131f',padding:17,borderRadius:20,marginBottom:10},eye:{color:'#ef159d',fontSize:10,fontWeight:'900'},win:{color:'#fff',fontSize:19,fontWeight:'900',marginTop:5},muted:{color:'#aaaab5',marginTop:5},row:{flexDirection:'row',justifyContent:'space-between',alignItems:'center'},name:{color:'#fff',fontWeight:'900'},badge:{color:'#ffd43b',fontSize:10,fontWeight:'900'}});
