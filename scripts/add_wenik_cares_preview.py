from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
MARK='WENIK CARES PREVIEW V1'
if MARK in s:
    raise SystemExit('already applied')
css='''<style>/* WENIK CARES PREVIEW V1 */
#wenikCaresOverlay{position:fixed;inset:0;z-index:99999;background:linear-gradient(180deg,#120d22,#281333);display:flex;align-items:center;justify-content:center;padding:18px;font-family:inherit}
.wcCard{width:min(100%,430px);max-height:92vh;overflow:auto;background:#fff;border-radius:30px;padding:24px 20px 20px;box-shadow:0 24px 70px rgba(0,0,0,.38);text-align:center}.wcHeart{width:74px;height:74px;margin:0 auto 12px;border-radius:24px;display:grid;place-items:center;font-size:38px;background:linear-gradient(135deg,#7427ff,#e91cad 48%,#ff7a22,#ffb51b);color:#fff}.wcTag{font-size:12px;font-weight:900;letter-spacing:2px;color:#8b36d9}.wcCard h2{margin:7px 0 8px;font-size:28px;color:#17111f}.wcCard p{margin:0 auto 14px;line-height:1.65;color:#625a68;font-size:15px}.wcCase{background:#f8f5fb;border-radius:20px;padding:15px;text-align:left;margin:15px 0}.wcCase b{display:block;color:#25172f;margin-bottom:5px}.wcTrust{font-size:12px!important;color:#83798a!important}.wcDonate{width:100%;border:0;border-radius:18px;padding:15px;font-size:17px;font-weight:900;color:#fff;background:linear-gradient(90deg,#7427ff,#e91cad,#ff7a22);cursor:pointer}.wcLater{width:100%;border:0;background:transparent;padding:13px;color:#766c7c;font-weight:800;cursor:pointer}.wcDemo{display:inline-block;margin-top:8px;padding:5px 10px;border-radius:99px;background:#fff3d7;color:#9a6200;font-size:11px;font-weight:800}
</style>'''
html='''<div id="wenikCaresOverlay" role="dialog" aria-modal="true" aria-label="WENIK Cares" style="display:none"><div class="wcCard"><div class="wcHeart">♥</div><div class="wcTag">WENIK CARES</div><h2>سوا منعمل فرق</h2><p>كل فترة، WENIK بتسلّط الضوء على حالة إنسانية موثّقة وبتفتح الباب لعيلتنا تساعد بمحبة وشفافية.</p><div class="wcCase" dir="rtl"><b>الحالة الإنسانية الحالية</b><span>مساحة مخصّصة لقصة الحالة، الجهة الموثّقة، وهدف الحملة.</span></div><p class="wcTrust" dir="rtl">التبرع اختياري بالكامل • تفاصيل الجهة المستفيدة والإثباتات بتكون واضحة قبل الدفع</p><button class="wcDonate" type="button" onclick="alert('Preview فقط — ما في دفع أو تبرع فعلي حالياً')">تبرّع الآن ❤️</button><button class="wcLater" type="button" onclick="document.getElementById('wenikCaresOverlay').style.display='none'">يمكن لاحقاً</button><span class="wcDemo">PREVIEW — لا يوجد تحصيل أموال</span></div></div>'''
js='''<script>document.addEventListener('DOMContentLoaded',function(){try{if(!sessionStorage.getItem('wenik_cares_seen')){var x=document.getElementById('wenikCaresOverlay');if(x)x.style.display='flex';sessionStorage.setItem('wenik_cares_seen','1')}}catch(e){var x=document.getElementById('wenikCaresOverlay');if(x)x.style.display='flex'}});</script>'''
s=s.replace('</head>',css+'\n</head>',1)
s=s.replace('</body>',html+'\n'+js+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('applied',MARK)
# staging preview only
