from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''</script>\n\n\n// WENIK MINI DASH: compact, fast and swipe-friendly.\n(()=>{const root=document.querySelector('.wenikMiniDash');if(!root)return;const slides=[...root.querySelectorAll('.wenikMiniSlide')],dots=[...root.querySelectorAll('.wenikMiniDots i')];let n=0,touchX=null;const show=i=>{n=(i+slides.length)%slides.length;slides.forEach((x,k)=>x.classList.toggle('isActive',k===n));dots.forEach((x,k)=>x.classList.toggle('on',k===n))};setInterval(()=>show(n+1),3000);root.addEventListener('touchstart',e=>touchX=e.touches[0].clientX,{passive:true});root.addEventListener('touchend',e=>{if(touchX==null)return;const d=e.changedTouches[0].clientX-touchX;if(Math.abs(d)>28)show(n+(d<0?1:-1));touchX=null},{passive:true})})();\n\n</body>'''
new='''</script>\n\n<script>\n// WENIK MINI DASH: compact, fast and swipe-friendly.\n(()=>{const root=document.querySelector('.wenikMiniDash');if(!root)return;const slides=[...root.querySelectorAll('.wenikMiniSlide')],dots=[...root.querySelectorAll('.wenikMiniDots i')];let n=0,touchX=null;const show=i=>{n=(i+slides.length)%slides.length;slides.forEach((x,k)=>x.classList.toggle('isActive',k===n));dots.forEach((x,k)=>x.classList.toggle('on',k===n))};setInterval(()=>show(n+1),3000);root.addEventListener('touchstart',e=>touchX=e.touches[0].clientX,{passive:true});root.addEventListener('touchend',e=>{if(touchX==null)return;const d=e.changedTouches[0].clientX-touchX;if(Math.abs(d)>28)show(n+(d<0?1:-1));touchX=null},{passive:true})})();\n</script>\n\n</body>'''
assert old in s, 'unsafe raw mini dash script block not found'
s=s.replace(old,new,1)
assert '<script>\n// WENIK MINI DASH: compact, fast and swipe-friendly.' in s
p.write_text(s,encoding='utf-8')
print('Fixed mini dashboard script wrapper.')
