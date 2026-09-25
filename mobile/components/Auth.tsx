import { useState } from 'react';
import { Alert, Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { supabase } from '../lib/supabase';

const normalizePhone=(value:string)=>{
  const raw=value.trim().replace(/[\s()-]/g,'');
  if(raw.startsWith('+')) return raw;
  if(raw.startsWith('961')) return '+'+raw;
  if(raw.startsWith('0')) return '+961'+raw.slice(1);
  return '+961'+raw;
};

export default function Auth() {
  const [mode,setMode]=useState<'join'|'login'>('login');
  const [first,setFirst]=useState('');
  const [last,setLast]=useState('');
  const [phone,setPhone]=useState('');
  const [password,setPassword]=useState('');
  const [loading,setLoading]=useState(false);

  async function submit(){
    if(!phone.trim()||!password) return Alert.alert('WENIK','Mobile and password are required.');
    if(password.length<6) return Alert.alert('WENIK','Password must be at least 6 characters.');
    setLoading(true);
    const p=normalizePhone(phone);
    const result=mode==='login'
      ? await supabase.auth.signInWithPassword({phone:p,password})
      : await supabase.auth.signUp({phone:p,password,options:{data:{first_name:first.trim(),last_name:last.trim()}}});
    setLoading(false);
    if(result.error) return Alert.alert('WENIK',result.error.message);
    if(mode==='join'&&!result.data.session) Alert.alert('WENIK','We sent a verification code to your mobile.');
  }

  return <View style={s.wrap}>
    <Text style={s.logo}>WENIK</Text><Text style={s.win}>WIN WIN</Text>
    <View style={s.tabs}>
      <Pressable onPress={()=>setMode('join')} style={[s.tab,mode==='join'&&s.tabOn]}><Text style={[s.tabText,mode==='join'&&s.tabTextOn]}>JOIN US</Text></Pressable>
      <Pressable onPress={()=>setMode('login')} style={[s.tab,mode==='login'&&s.tabOn]}><Text style={[s.tabText,mode==='login'&&s.tabTextOn]}>LOGIN</Text></Pressable>
    </View>
    <Text style={s.title}>{mode==='login'?'Welcome back':'Join WENIK'}</Text>
    {mode==='join'&&<View style={s.nameRow}>
      <TextInput style={[s.input,s.half]} placeholder="First name" placeholderTextColor="#777783" value={first} onChangeText={setFirst}/>
      <TextInput style={[s.input,s.half]} placeholder="Last name" placeholderTextColor="#777783" value={last} onChangeText={setLast}/>
    </View>}
    <TextInput style={s.input} placeholder="Mobile" placeholderTextColor="#777783" keyboardType="phone-pad" value={phone} onChangeText={setPhone}/>
    <TextInput style={s.input} placeholder={mode==='join'?'Create password':'Password'} placeholderTextColor="#777783" secureTextEntry value={password} onChangeText={setPassword}/>
    <Pressable style={[s.btn,loading&&{opacity:.6}]} disabled={loading} onPress={submit}><Text style={s.btnText}>{loading?'PLEASE WAIT…':mode==='login'?'LOGIN':'CREATE ACCOUNT'}</Text></Pressable>
  </View>
}
const s=StyleSheet.create({
  wrap:{flex:1,justifyContent:'center',padding:24,backgroundColor:'#09090d'},
  logo:{textAlign:'center',color:'#fff',fontSize:34,fontWeight:'900',letterSpacing:3},
  win:{textAlign:'center',color:'#ef159d',fontSize:12,fontWeight:'900',letterSpacing:4,marginBottom:34},
  tabs:{flexDirection:'row',backgroundColor:'#14141b',borderRadius:18,padding:4,marginBottom:24},
  tab:{flex:1,padding:12,borderRadius:14,alignItems:'center'},tabOn:{backgroundColor:'#24242d'},
  tabText:{color:'#777783',fontWeight:'900'},tabTextOn:{color:'#fff'},
  title:{color:'#fff',fontSize:27,fontWeight:'900',marginBottom:18},
  nameRow:{flexDirection:'row',gap:10},half:{flex:1},
  input:{backgroundColor:'#14141b',color:'#fff',borderRadius:18,paddingHorizontal:18,height:56,marginBottom:12,borderWidth:1,borderColor:'#24242d'},
  btn:{height:56,borderRadius:18,backgroundColor:'#ef159d',alignItems:'center',justifyContent:'center',marginTop:8},
  btnText:{color:'#fff',fontWeight:'900',letterSpacing:1}
});
