import { useEffect, useMemo, useState } from 'react';
import { ActivityIndicator, Image, Modal, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { supabase } from '../lib/supabase';

type Partner={partner_id:string;business_name:string;area?:string;category?:string;address?:string;logo_url?:string;benefit_title?:string;benefit_type?:string;benefit_value?:number;benefit_conditions?:string};
const categories=['All','Restaurants','Cafés','Sweets','Fashion','Shoes & Bags','Beauty','Hair Salons','Fitness','Perfumes','Optics','Jewelry','Electronics','Furniture','Hotels','Entertainment','Automotive','Education','Services','Swimming Pools'];
const norm=(v:any)=>String(v??'').trim().toLowerCase();
function discount(x:Partner){const v=Number(x.benefit_value);if(Number.isFinite(v)&&v>0&&v<=100)return Math.round(v)+'% OFF';return x.benefit_title?'WENIK OFFER':''}

export default function Partners(){
 const [rows,setRows]=useState<Partner[]>([]),[loading,setLoading]=useState(true),[q,setQ]=useState(''),[cat,setCat]=useState('All'),[selected,setSelected]=useState<Partner|null>(null),[hero,setHero]=useState('');
 useEffect(()=>{supabase.rpc('public_partner_directory_v2').then(({data})=>{setRows(data||[]);setLoading(false)})},[]);
 const list=useMemo(()=>rows.filter(x=>{
   const hay=norm([x.business_name,x.area,x.category,x.address,x.benefit_title].join(' '));
   return (!q||hay.includes(norm(q)))&&(cat==='All'||norm(x.category).includes(norm(cat.replace(/s$/,''))));
 }),[rows,q,cat]);
 async function open(x:Partner){setSelected(x);setHero(x.logo_url||'');const {data}=await supabase.rpc('public_partner_ads',{p_partner_id:x.partner_id});const img=(data||[]).find((a:any)=>a?.image_url)?.image_url;if(img)setHero(img)}
 return <SafeAreaView style={s.safe}><View style={s.head}><Text style={s.title}>PARTNERS</Text><Text style={s.sub}>Discover WENIK partners</Text></View>
  <TextInput style={s.search} placeholder="Search partners, area or category" placeholderTextColor="#777783" value={q} onChangeText={setQ}/>
  <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={s.chips}>{categories.map(x=><Pressable key={x} onPress={()=>setCat(x)} style={[s.chip,cat===x&&s.chipOn]}><Text style={[s.chipText,cat===x&&s.chipTextOn]}>{x}</Text></Pressable>)}</ScrollView>
  {loading?<ActivityIndicator style={{marginTop:40}}/>:<ScrollView contentContainerStyle={s.grid}>{list.map(x=><Pressable key={x.partner_id} style={s.card} onPress={()=>open(x)}>
    <View style={s.media}>{x.logo_url?<Image source={{uri:x.logo_url}} style={s.img}/>:<Text style={s.placeholder}>WENIK</Text>}{discount(x)?<Text style={s.off}>{discount(x)}</Text>:null}</View>
    <View style={s.body}><Text style={s.name} numberOfLines={1}>{x.business_name}</Text><Text style={s.meta} numberOfLines={1}>{[x.area,x.category].filter(Boolean).join(' · ')}</Text><Text style={s.promo} numberOfLines={1}>{x.benefit_title||'WENIK PARTNER'}</Text></View>
  </Pressable>)}</ScrollView>}
  <Modal visible={!!selected} transparent animationType="slide" onRequestClose={()=>setSelected(null)}><View style={s.modalBack}><View style={s.modal}>
    <Pressable onPress={()=>setSelected(null)}><Text style={s.close}>CLOSE ×</Text></Pressable>
    {hero?<Image source={{uri:hero}} style={s.hero}/>:<View style={[s.hero,s.heroFallback]}><Text style={s.placeholder}>WENIK</Text></View>}
    <Text style={s.detailName}>{selected?.business_name}</Text><Text style={s.detailMeta}>{[selected?.category,selected?.area,selected?.address].filter(Boolean).join(' • ')}</Text>
    {selected?.benefit_title?<View style={s.offer}><Text style={s.offerStrong}>{discount(selected)}</Text><Text style={s.offerText}>{selected.benefit_title}</Text>{selected.benefit_conditions?<Text style={s.detailMeta}>{selected.benefit_conditions}</Text>:null}</View>:null}
  </View></View></Modal>
 </SafeAreaView>
}
const s=StyleSheet.create({
 safe:{flex:1,backgroundColor:'#09090d'},head:{paddingHorizontal:20,paddingTop:16},title:{color:'#fff',fontSize:28,fontWeight:'900'},sub:{color:'#aaaab5',marginTop:3},
 search:{height:52,margin:16,marginBottom:8,borderRadius:17,paddingHorizontal:16,backgroundColor:'#17131f',color:'#fff',borderWidth:1,borderColor:'#292331'},
 chips:{paddingHorizontal:16,gap:8,paddingBottom:12},chip:{height:38,paddingHorizontal:14,borderRadius:19,backgroundColor:'#17131f',justifyContent:'center'},chipOn:{backgroundColor:'#ef159d'},chipText:{color:'#aaaab5',fontWeight:'800'},chipTextOn:{color:'#fff'},
 grid:{padding:16,paddingTop:0,flexDirection:'row',flexWrap:'wrap',gap:12},card:{width:'48%',backgroundColor:'#fff',borderRadius:22,overflow:'hidden'},media:{aspectRatio:1,backgroundColor:'#f4ebff',alignItems:'center',justifyContent:'center'},img:{width:'100%',height:'100%'},placeholder:{fontSize:20,fontWeight:'900',color:'#7c3cff'},off:{position:'absolute',top:9,left:9,backgroundColor:'#ff5a00',color:'#fff',fontSize:11,fontWeight:'900',paddingHorizontal:9,paddingVertical:6,borderRadius:20},
 body:{minHeight:112,padding:11},name:{color:'#16121b',fontSize:16,fontWeight:'900'},meta:{color:'#756e7b',fontSize:11,marginTop:4},promo:{color:'#ef159d',fontSize:10,fontWeight:'900',marginTop:7},
 modalBack:{flex:1,backgroundColor:'rgba(0,0,0,.72)',justifyContent:'flex-end'},modal:{backgroundColor:'#14141b',borderTopLeftRadius:30,borderTopRightRadius:30,padding:20,paddingBottom:38,maxHeight:'90%'},close:{alignSelf:'flex-end',color:'#aaaab5',fontWeight:'900',marginBottom:12},hero:{width:'100%',aspectRatio:1.6,borderRadius:22},heroFallback:{backgroundColor:'#f4ebff',alignItems:'center',justifyContent:'center'},detailName:{color:'#fff',fontSize:26,fontWeight:'900',marginTop:18},detailMeta:{color:'#aaaab5',fontSize:13,marginTop:6,lineHeight:19},offer:{backgroundColor:'#211727',padding:16,borderRadius:18,marginTop:16},offerStrong:{color:'#ff7a00',fontWeight:'900'},offerText:{color:'#fff',fontSize:16,fontWeight:'800',marginTop:5}
});
