from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""    const{error}=await sb.auth.signInWithPassword({phone:ph(raw),password});
    if(error){if(msg)msg.textContent=error.message;return;}
    enter();
"""
new="""    const normalized=ph(raw);
    let{error}=await sb.auth.signInWithPassword({phone:normalized,password});
    if(error&&normalized.startsWith('+'))({error}=await sb.auth.signInWithPassword({phone:normalized.slice(1),password}));
    if(error){if(msg)msg.textContent=error.message;return;}
    enter();
"""
if s.count(old)!=1:
    raise SystemExit('Expected exactly one customer login auth block')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Patched only customer login phone normalization fallback.')