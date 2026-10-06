import { useState } from 'react';
import { Alert, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { supabase } from '../lib/supabase';
import { LinearGradient } from 'expo-linear-gradient';

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
  const [terms,setTerms]=useState(false),[privacy,setPrivacy]=useState(false),[marketing,setMarketing]=useState(false);
  const [flow,setFlow]=useState<'auth'|'joinOtp'|'resetOtp'|'newPassword'>('auth');
  const [otp,setOtp]=useState(''),[flowPhone,setFlowPhone]=useState(''),[newPassword,setNewPassword]=useState(''),[confirmPassword,setConfirmPassword]=useState(''),[showPassword,setShowPassword]=useState(false),[showNewPassword,setShowNewPassword]=useState(false);

  async function submit(){if(loading)return;try{
    if(mode==='join'&&(!first.trim()||!last.trim())) return Alert.alert('WENIK','First and last name are required.');
    if(mode==='join'&&(!terms||!privacy)) return Alert.alert('WENIK','Terms and Privacy are required.');
    if(!phone.trim()||!password) return Alert.alert('WENIK','Mobile and password are required.');
    if(password.length<6) return Alert.alert('WENIK','Password must be at least 6 characters.');
    setLoading(true);
    const p=normalizePhone(phone);
    const result=mode==='login'
      ? await supabase.auth.signInWithPassword({phone:p,password})
      : await supabase.auth.signUp({phone:p,password,options:{data:{first_name:first.trim(),last_name:last.trim(),terms_accepted:true,privacy_accepted:true,marketing_consent:marketing}}});
    setLoading(false);
    if(result.error) return Alert.alert('WENIK',result.error.message);
    if(mode==='join'&&!result.data.session){setFlowPhone(p);setOtp('');setFlow('joinOtp');}
  }catch(e){Alert.alert('WENIK',e instanceof Error?e.message:'Please check your connection and try again.')}finally{setLoading(false)}}

  async function verifyJoinOtp(){if(loading)return;try{if(otp.replace(/\D/g,'').length!==6)return Alert.alert('WENIK','Enter the 6-digit code.');setLoading(true);const {data,error}=await supabase.auth.verifyOtp({phone:flowPhone,token:otp.replace(/\D/g,''),type:'sms'});setLoading(false);if(error)return Alert.alert('WENIK',error.message);if(!data?.session)return Alert.alert('WENIK','Verification succeeded. Please try Login.');}catch(e){Alert.alert('WENIK',e instanceof Error?e.message:'Please check your connection and try again.')}finally{setLoading(false)}}
  async function forgot(){if(loading)return;try{if(!phone.trim())return Alert.alert('WENIK','Enter your mobile number first.');const p=normalizePhone(phone);setLoading(true);const {error}=await supabase.auth.signInWithOtp({phone:p,options:{shouldCreateUser:false}});setLoading(false);if(error)return Alert.alert('WENIK',error.message);setFlowPhone(p);setOtp('');setFlow('resetOtp');}catch(e){Alert.alert('WENIK',e instanceof Error?e.message:'Please check your connection and try again.')}finally{setLoading(false)}}
  async function verifyReset(){if(loading)return;try{if(otp.replace(/\D/g,'').length!==6)return Alert.alert('WENIK','Enter the 6-digit code.');setLoading(true);const {data,error}=await supabase.auth.verifyOtp({phone:flowPhone,token:otp.replace(/\D/g,''),type:'sms'});setLoading(false);if(error||!data?.session)return Alert.alert('WENIK',error?.message||'Could not verify code.');setFlow('newPassword');}catch(e){Alert.alert('WENIK',e instanceof Error?e.message:'Please check your connection and try again.')}finally{setLoading(false)}}
  async function savePassword(){if(loading)return;try{if(newPassword.length<6)return Alert.alert('WENIK','Password must be at least 6 characters.');if(newPassword!==confirmPassword)return Alert.alert('WENIK','Passwords do not match.');setLoading(true);const {error}=await supabase.auth.updateUser({password:newPassword});setLoading(false);if(error)return Alert.alert('WENIK',error.message);Alert.alert('WENIK','Password changed ✓');}catch(e){Alert.alert('WENIK',e instanceof Error?e.message:'Please check your connection and try again.')}finally{setLoading(false)}}
  if(flow!=='auth')return <ScrollView style={s.scroll} contentContainerStyle={s.wrap}><View style={s.brand}><LinearGradient colors={['#8f24ff','#ef159d','#ff6f21','#ffd21c']} style={s.brandW}><Text style={s.brandWText}>W.</Text></LinearGradient><View><Text style={s.logo}>WENIK</Text><Text style={s.win}>WIN WIN</Text></View></View><Text style={s.title}>{flow==='joinOtp'?'VERIFY PHONE':'RESET PASSWORD'}</Text>{flow!=='newPassword'?<><Text style={s.help}>We sent a 6-digit code to your mobile.</Text><TextInput style={s.input} placeholder="6-digit code" placeholderTextColor="#777783" keyboardType="number-pad" maxLength={6} value={otp} onChangeText={x=>setOtp(x.replace(/\D/g,'').slice(0,6))}/><Pressable disabled={loading} style={s.btn} onPress={flow==='joinOtp'?verifyJoinOtp:verifyReset}><Text style={s.btnText}>{loading?'PLEASE WAIT…':'VERIFY CODE'}</Text></Pressable></>:<><Text style={s.help}>Choose your new password.</Text><View style={s.passwordWrap}><TextInput style={s.passwordInput} placeholder="New password" placeholderTextColor="#777783" secureTextEntry={!showNewPassword} value={newPassword} onChangeText={setNewPassword}/><Pressable onPress={()=>setShowNewPassword(v=>!v)}><Text style={s.eyeBtn}>{showNewPassword?'HIDE':'SHOW'}</Text></Pressable></View><TextInput style={s.input} placeholder="Confirm new password" placeholderTextColor="#777783" secureTextEntry={!showNewPassword} value={confirmPassword} onChangeText={setConfirmPassword}/><Pressable disabled={loading} style={s.btn} onPress={savePassword}><Text style={s.btnText}>{loading?'PLEASE WAIT…':'SAVE NEW PASSWORD'}</Text></Pressable></>}<Pressable style={s.secondary} onPress={()=>setFlow('auth')}><Text style={s.secondaryText}>BACK</Text></Pressable></ScrollView>;

  return <ScrollView style={s.scroll} contentContainerStyle={s.wrap}>
    <View style={s.brand}><LinearGradient colors={['#8f24ff','#ef159d','#ff6f21','#ffd21c']} style={s.brandW}><Text style={s.brandWText}>W.</Text></LinearGradient><View><Text style={s.logo}>WENIK</Text><Text style={s.win}>WIN WIN</Text></View></View>
    <View style={s.tabs}>
      <Pressable onPress={()=>setMode('join')} style={[s.tab,mode==='join'&&s.tabOn]}><Text style={[s.tabText,mode==='join'&&s.tabTextOn]}>JOIN US</Text></Pressable>
      <Pressable onPress={()=>setMode('login')} style={[s.tab,mode==='login'&&s.tabOn]}><Text style={[s.tabText,mode==='login'&&s.tabTextOn]}>LOGIN</Text></Pressable>
    </View>
    <Text style={s.title}>{mode==='login'?'Welcome back':'Join WENIK'}</Text><Text style={s.authSub}>{mode==='login'?'Access your points, rewards and WENIK activity.':'Create your WENIK account and start discovering benefits.'}</Text>
    {mode==='join'&&<View style={s.nameRow}>
      <TextInput style={[s.input,s.half]} placeholder="First name" placeholderTextColor="#777783" value={first} onChangeText={setFirst}/>
      <TextInput style={[s.input,s.half]} placeholder="Last name" placeholderTextColor="#777783" value={last} onChangeText={setLast}/>
    </View>}
    <TextInput style={s.input} placeholder="Mobile" placeholderTextColor="#777783" keyboardType="phone-pad" value={phone} onChangeText={setPhone}/>
    <View style={s.passwordWrap}><TextInput style={s.passwordInput} placeholder={mode==='join'?'Create password':'Password'} placeholderTextColor="#777783" secureTextEntry={!showPassword} value={password} onChangeText={setPassword}/><Pressable onPress={()=>setShowPassword(v=>!v)}><Text style={s.eyeBtn}>{showPassword?'HIDE':'SHOW'}</Text></Pressable></View>
    {mode==='join'?<View style={s.checks}><Pressable onPress={()=>setTerms(!terms)}><Text style={s.checkText}>{terms?'☑':'☐'} I accept Terms</Text></Pressable><Pressable onPress={()=>setPrivacy(!privacy)}><Text style={s.checkText}>{privacy?'☑':'☐'} I accept Privacy</Text></Pressable><Pressable onPress={()=>setMarketing(!marketing)}><Text style={s.checkText}>{marketing?'☑':'☐'} Marketing updates (optional)</Text></Pressable></View>:null}
    <Pressable style={[s.btn,loading&&{opacity:.6}]} disabled={loading} onPress={submit}><Text style={s.btnText}>{loading?'PLEASE WAIT…':mode==='login'?'LOGIN':'CREATE ACCOUNT'}</Text></Pressable>
    {mode==='login'?<Pressable style={s.secondary} onPress={forgot}><Text style={s.secondaryText}>FORGOT PASSWORD?</Text></Pressable>:null}
  </ScrollView>
}
const s=StyleSheet.create({
  scroll:{flex:1,backgroundColor:'#f8f7fb'},
  wrap:{flexGrow:1,justifyContent:'center',padding:24,backgroundColor:'#f8f7fb'},
  brand:{flexDirection:'row',alignItems:'center',justifyContent:'center',gap:10,marginBottom:28},brandW:{width:52,height:52,borderRadius:26,alignItems:'center',justifyContent:'center'},brandWText:{color:'#fff',fontSize:22,fontWeight:'900'},logo:{color:'#18141d',fontSize:29,fontWeight:'900',letterSpacing:3},win:{color:'#ef159d',fontSize:10,fontWeight:'900',letterSpacing:4},
  tabs:{flexDirection:'row',backgroundColor:'#fff',borderRadius:18,padding:4,marginBottom:24},
  tab:{flex:1,padding:12,borderRadius:14,alignItems:'center'},tabOn:{backgroundColor:'#f5eaff',borderWidth:1,borderColor:'rgba(143,36,255,.18)'},
  tabText:{color:'#777783',fontWeight:'900'},tabTextOn:{color:'#8f24ff'},
  title:{color:'#18141d',fontSize:27,fontWeight:'900',marginBottom:5},authSub:{color:'#77717e',fontSize:12,lineHeight:18,marginBottom:18},
  nameRow:{flexDirection:'row',gap:10},half:{flex:1},
  input:{backgroundColor:'#fff',color:'#18141d',borderRadius:18,paddingHorizontal:18,height:56,marginBottom:12,borderWidth:1,borderColor:'rgba(92,55,110,.12)'},passwordWrap:{height:56,backgroundColor:'#fff',borderRadius:18,paddingLeft:18,paddingRight:14,marginBottom:12,borderWidth:1,borderColor:'rgba(92,55,110,.12)',flexDirection:'row',alignItems:'center'},passwordInput:{flex:1,color:'#18141d',height:'100%'},eyeBtn:{color:'#8f24ff',fontSize:9,fontWeight:'900',letterSpacing:.7,padding:8},
  btn:{height:56,borderRadius:18,backgroundColor:'#ef159d',borderWidth:1,borderColor:'rgba(255,255,255,.08)',alignItems:'center',justifyContent:'center',marginTop:8},
  btnText:{color:'#fff',fontWeight:'900',letterSpacing:1},
  checks:{gap:10,marginVertical:6},checkText:{color:'#77717e',fontWeight:'700'},secondary:{height:48,alignItems:'center',justifyContent:'center',marginTop:8},secondaryText:{color:'#8f24ff',fontWeight:'900'},help:{color:'#77717e',marginBottom:16,lineHeight:20}
});
