export default async function handler(req,res){
  if(req.method!=='GET') return res.status(405).end();
  try{
    const r=await fetch('https://api.ipify.org?format=json',{headers:{'cache-control':'no-store'},signal:AbortSignal.timeout(8000)});
    if(!r.ok) return res.status(502).json({error:'Unable to resolve egress IP'});
    const data=await r.json();
    res.setHeader('Cache-Control','no-store');
    return res.status(200).json({ip:data.ip});
  }catch(e){
    return res.status(500).json({error:'IP diagnostic failed'});
  }
}
