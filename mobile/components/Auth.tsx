import { useState } from 'react';
import { Alert, Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { supabase } from '../lib/supabase';

export default function Auth() {
  const [email,setEmail]=useState('');
  const [password,setPassword]=useState('');
  const [loading,setLoading]=useState(false);

  async function login(){
    setLoading(true);
    const {error}=await supabase.auth.signInWithPassword({email:email.trim(),password});
    setLoading(false);
    if(error) Alert.alert('WENIK',error.message);
  }

  return <View style={s.wrap}>
    <Text style={s.logo}>WENIK</Text><Text style={s.win}>WIN WIN</Text>
    <Text style={s.title}>Welcome back</Text>
    <TextInput style={s.input} placeholder="Email" placeholderTextColor="#777783" autoCapitalize="none" keyboardType="email-address" value={email} onChangeText={setEmail}/>
    <TextInput style={s.input} placeholder="Password" placeholderTextColor="#777783" secureTextEntry value={password} onChangeText={setPassword}/>
    <Pressable style={[s.btn,loading&&{opacity:.6}]} disabled={loading} onPress={login}><Text style={s.btnText}>{loading?'SIGNING IN…':'SIGN IN'}</Text></Pressable>
  </View>
}
const s=StyleSheet.create({
  wrap:{flex:1,justifyContent:'center',padding:24,backgroundColor:'#09090d'},
  logo:{textAlign:'center',color:'#fff',fontSize:34,fontWeight:'900',letterSpacing:3},
  win:{textAlign:'center',color:'#ef159d',fontSize:12,fontWeight:'900',letterSpacing:4,marginBottom:42},
  title:{color:'#fff',fontSize:27,fontWeight:'900',marginBottom:18},
  input:{backgroundColor:'#14141b',color:'#fff',borderRadius:18,paddingHorizontal:18,height:56,marginBottom:12,borderWidth:1,borderColor:'#24242d'},
  btn:{height:56,borderRadius:18,backgroundColor:'#ef159d',alignItems:'center',justifyContent:'center',marginTop:8},
  btnText:{color:'#fff',fontWeight:'900',letterSpacing:1}
});
