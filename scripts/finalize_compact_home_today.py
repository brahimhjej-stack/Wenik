from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Insert compact WENIK promo dashboard immediately after the Home welcome hero.
anchor='''<div class="hero"><div class="eyebrow">MORE TO DISCOVER</div><h2>Welcome to WENIK</h2><div class="muted">Offers, prizes and new opportunities in one place.</div></div>'''
assert anchor in s, 'home hero anchor missing'
block='''<div class="wenikMiniDash" aria-label="WENIK news">
  <div class="wenikMiniSlide isActive"><b>ADVERTISE ON WENIK</b><span>للإعلانات الاتصال على 76 468 506</span></div>
  <div class="wenikMiniSlide"><b>FREE ADS NOW</b><span>إعلاناتكم مجانية الآن على WENIK</span></div>
  <div class="wenikMiniSlide"><b>WIN EVERY DAY</b><span>كل يوم رابحين جدد وجوائز جديدة</span></div>
  <div class="wenikMiniSlide"><b>DISCOVER MORE</b><span>عروض جديدة من شركاء WENIK</span></div>
  <div class="wenikMiniDots" aria-hidden="true"><i class="on"></i><i></i><i></i><i></i></div>
</div>'''
if 'wenikMiniDash' not in s:
    s=s.replace(anchor,anchor+block,1)
# Rename/reorder visual headings: categories first, partners second inside discovery area.
s=s.replace('<div class="sectionTitle"><h3>PARTNERS</h3><span class="muted">Near you</span></div>','<div class="sectionTitle wenikCategoryLead"><h3>CATEGORIES</h3><span class="muted">Choose what you need</span></div>',1)
# Add Partners label immediately before home partner results if known.
needle='<div id="homePartnerResults"'
if needle in s and 'wenikPartnersLead' not in s:
    s=s.replace(needle,'<div class="sectionTitle wenikPartnersLead"><h3>PARTNERS</h3><span class="muted">Near you</span></div>'+needle,1)
# Compact styling + fast promo rotation.
style='''
/* WENIK COMPACT HOME + MINI DASH V1 */
@media(max-width:640px){
 #home>.hero{padding:11px 13px!important;min-height:0!important;margin-bottom:7px!important}
 #home>.hero h2{font-size:20px!important;margin:2px 0!important}
 #home>.hero .muted{font-size:11px!important}
 #home .sectionTitle{margin:10px 2px 5px!important}
 #home .wenikDiscovery{padding:9px!important}
}
.wenikMiniDash{position:relative;overflow:hidden;min-height:72px;margin:8px 0 5px;border-radius:18px;background:linear-gradient(120deg,#6f24ff 0%,#d923b9 42%,#ff6a20 76%,#ffc928 100%);box-shadow:0 8px 22px rgba(89,35,170,.16);color:#fff}
.wenikMiniSlide{position:absolute;inset:0;padding:13px 16px 18px;display:flex;flex-direction:column;justify-content:center;opacity:0;transform:translateX(10px);transition:opacity .22s ease,transform .22s ease;pointer-events:none}
.wenikMiniSlide.isActive{opacity:1;transform:none;pointer-events:auto}
.wenikMiniSlide b{font-size:13px;letter-spacing:.8px;line-height:1.1}.wenikMiniSlide span{font-size:12px;font-weight:700;margin-top:5px;direction:rtl;text-align:left}
.wenikMiniDots{position:absolute;left:16px;bottom:8px;display:flex;gap:4px}.wenikMiniDots i{width:5px;height:5px;border-radius:9px;background:rgba(255,255,255,.45)}.wenikMiniDots i.on{width:14px;background:#fff}
.wenikCategoryLead h3,.wenikPartnersLead h3{font-weight:900}
'''
if 'WENIK COMPACT HOME + MINI DASH V1' not in s:
    s=s.replace('</style>',style+'\n</style>',1)
js='''
// WENIK MINI DASH: compact, fast and swipe-friendly.
(()=>{const root=document.querySelector('.wenikMiniDash');if(!root)return;const slides=[...root.querySelectorAll('.wenikMiniSlide')],dots=[...root.querySelectorAll('.wenikMiniDots i')];let n=0,touchX=null;const show=i=>{n=(i+slides.length)%slides.length;slides.forEach((x,k)=>x.classList.toggle('isActive',k===n));dots.forEach((x,k)=>x.classList.toggle('on',k===n))};setInterval(()=>show(n+1),3000);root.addEventListener('touchstart',e=>touchX=e.touches[0].clientX,{passive:true});root.addEventListener('touchend',e=>{if(touchX==null)return;const d=e.changedTouches[0].clientX-touchX;if(Math.abs(d)>28)show(n+(d<0?1:-1));touchX=null},{passive:true})})();
'''
if 'WENIK MINI DASH: compact' not in s:
    s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('Finalized compact WENIK home mini-dashboard.')
