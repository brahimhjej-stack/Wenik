from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK CUSTOMER HOME COMPACT ROTATING DASHBOARD V1 */'
if marker in s:
    raise SystemExit('already applied')
block=r'''
<style id="wenikCustomerHomeCompactDashboardV1">
/* WENIK CUSTOMER HOME COMPACT ROTATING DASHBOARD V1 */
.wenikHomeDash{margin:12px 20px 16px;position:relative;overflow:hidden;border-radius:22px;background:#fff;border:1px solid rgba(94,48,126,.08);box-shadow:0 10px 28px rgba(45,24,62,.09)}
.wenikHomeDashTrack{display:flex;width:100%;transition:transform .42s cubic-bezier(.22,.61,.36,1);will-change:transform}
.wenikHomeDashSlide{flex:0 0 100%;min-width:100%;box-sizing:border-box;padding:15px 17px 13px;display:grid;grid-template-columns:44px 1fr auto;gap:12px;align-items:center;min-height:88px}
.wenikHomeDashIcon{width:44px;height:44px;border-radius:15px;display:flex;align-items:center;justify-content:center;font-size:22px;background:linear-gradient(135deg,#f2e4ff,#ffe8ed,#fff0d6)}
.wenikHomeDashKicker{font-size:10px;letter-spacing:1.4px;font-weight:900;color:#8a8190;text-transform:uppercase;margin-bottom:3px}
.wenikHomeDashTitle{font-size:17px;line-height:1.08;font-weight:950;color:#24162f;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wenikHomeDashSub{margin-top:4px;font-size:11px;line-height:1.2;font-weight:650;color:#7e7584;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wenikHomeDashValue{font-size:22px;font-weight:950;color:#842cff;letter-spacing:-.5px;white-space:nowrap;text-align:right}
.wenikHomeDashValue small{font-size:10px;color:#8d8490;display:block;letter-spacing:.2px;margin-top:2px}
.wenikHomeDashDots{display:flex;gap:5px;justify-content:center;padding:0 0 9px}
.wenikHomeDashDot{width:6px;height:6px;border:0;padding:0;border-radius:99px;background:#ddd5e2;transition:width .25s,background .25s}
.wenikHomeDashDot.on{width:20px;background:linear-gradient(90deg,#832cff,#ef45bd,#ff9c22)}
@media(max-width:390px){.wenikHomeDash{margin:10px 20px 13px}.wenikHomeDashSlide{min-height:80px;padding:12px 14px;grid-template-columns:40px 1fr auto;gap:9px}.wenikHomeDashIcon{width:40px;height:40px;border-radius:13px;font-size:20px}.wenikHomeDashTitle{font-size:15px}.wenikHomeDashSub{font-size:10px}.wenikHomeDashValue{font-size:19px}}
</style>
<script id="wenikCustomerHomeCompactDashboardRuntimeV1">
(function(){
 const MARK='wenikHomeDashV1';
 function txt(el){return (el&&el.textContent||'').replace(/\s+/g,' ').trim()}
 function findByText(needle){
   const all=document.querySelectorAll('h1,h2,h3,h4,div,section,p,span');
   for(const el of all){if(txt(el)===needle)return el}
   for(const el of all){if(txt(el).includes(needle))return el}
   return null;
 }
 function findHomeAnchor(){
   const f=findByText('FEATURED');
   if(!f)return null;
   let n=f;
   for(let i=0;i<4&&n.parentElement;i++){
     if(n.parentElement.children.length>1){n=n.parentElement;break}
     n=n.parentElement;
   }
   return n;
 }
 function readPoints(){
   const sels=['#pointsBalance','#customerPoints','#points','#myPoints','[data-points]','[data-points-balance]','.pointsBalance','.customerPoints'];
   for(const sel of sels){const e=document.querySelector(sel);if(e){const raw=(e.dataset.points||e.dataset.pointsBalance||txt(e));const m=String(raw).match(/\d[\d,]*/);if(m)return m[0]}}
   try{
     for(let i=0;i<localStorage.length;i++){
       const k=localStorage.key(i)||''; if(!/point/i.test(k))continue;
       const v=localStorage.getItem(k)||''; const m=v.match(/\d[\d,]*/); if(m)return m[0];
     }
   }catch(e){}
   return '—';
 }
 function compactHero(){
   const t=findByText('Everything starts here.'); if(!t)return;
   let box=t.parentElement;
   for(let i=0;i<4&&box&&box.parentElement;i++){
     const r=box.getBoundingClientRect();
     if(r.height>130&&r.height<420&&r.width>250)break;
     box=box.parentElement;
   }
   if(box){box.style.setProperty('padding','18px 28px','important');box.style.setProperty('min-height','0','important');box.style.setProperty('margin-bottom','8px','important');}
   t.style.setProperty('font-size','26px','important');
   t.style.setProperty('line-height','1.05','important');
 }
 function make(){
   if(document.querySelector('.'+MARK))return true;
   const anchor=findHomeAnchor(); if(!anchor)return false;
   const wrap=document.createElement('section');wrap.className='wenikHomeDash '+MARK;wrap.setAttribute('aria-label','WENIK quick dashboard');
   const slides=[
    ['⭐','MY POINTS','Your WENIK balance','Points ready for rewards','points'],
    ['🎁','MY REWARDS','Rewards & gifts','See what you can redeem','REWARDS'],
    ['🏪','PARTNERS','Discover benefits','Find WENIK partners near you','EXPLORE'],
    ['🏆','WIN','Your next win','Check prizes, draws & winners','WIN'],
    ['⚡','IZA','Vote in one tap','I’m in / I’m out','IZA']
   ];
   const track=document.createElement('div');track.className='wenikHomeDashTrack';
   slides.forEach((x,i)=>{const sl=document.createElement('div');sl.className='wenikHomeDashSlide';sl.innerHTML='<div class="wenikHomeDashIcon">'+x[0]+'</div><div><div class="wenikHomeDashKicker">'+x[1]+'</div><div class="wenikHomeDashTitle">'+x[2]+'</div><div class="wenikHomeDashSub">'+x[3]+'</div></div><div class="wenikHomeDashValue" '+(x[4]==='points'?'data-wenik-points-value':'')+'>'+(x[4]==='points'?readPoints():x[4])+(x[4]==='points'?'<small>POINTS</small>':'')+'</div>';track.appendChild(sl)});
   const dots=document.createElement('div');dots.className='wenikHomeDashDots';
   slides.forEach((_,i)=>{const b=document.createElement('button');b.className='wenikHomeDashDot'+(i===0?' on':'');b.type='button';b.setAttribute('aria-label','Dashboard '+(i+1));dots.appendChild(b)});
   wrap.append(track,dots);
   anchor.parentElement.insertBefore(wrap,anchor);
   let idx=0,timer=null,startX=null;
   const ds=[...dots.children];
   function go(n){idx=(n+slides.length)%slides.length;track.style.transform='translateX(-'+(idx*100)+'%)';ds.forEach((d,j)=>d.classList.toggle('on',j===idx))}
   function reset(){if(timer)clearInterval(timer);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)timer=setInterval(()=>go(idx+1),5000)}
   ds.forEach((d,i)=>d.addEventListener('click',()=>{go(i);reset()}));
   wrap.addEventListener('touchstart',e=>{startX=e.touches[0].clientX},{passive:true});
   wrap.addEventListener('touchend',e=>{if(startX==null)return;const dx=e.changedTouches[0].clientX-startX;if(Math.abs(dx)>38)go(idx+(dx<0?1:-1));startX=null;reset()},{passive:true});
   setInterval(()=>{const e=wrap.querySelector('[data-wenik-points-value]');if(e){const v=readPoints();e.innerHTML=v+'<small>POINTS</small>'}},3000);
   reset();compactHero();return true;
 }
 function boot(){if(make())return;let n=0;const t=setInterval(()=>{n++;if(make()||n>20)clearInterval(t)},300)}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
'''
if '</head>' not in s: raise SystemExit('head anchor missing')
s=s.replace('</head>',block+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Compact rotating Customer Home dashboard applied')
