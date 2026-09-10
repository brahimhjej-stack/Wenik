from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* WENIK CUSTOMER HOME MOBILE APP FINISH V2 */'
if marker in s:
    raise SystemExit('already applied')

if '/* WENIK CUSTOMER HOME COMPACT ROTATING DASHBOARD V1 */' not in s:
    raise SystemExit('V1 dashboard marker missing')

old = "   return '—';"
if old in s:
    s = s.replace(old, "   return '0';", 1)
elif "   return '0';" not in s:
    raise SystemExit('points fallback anchor missing')

block = r'''
<style id="wenikCustomerHomeMobileFinishV2">
/* WENIK CUSTOMER HOME MOBILE APP FINISH V2 */
html{-webkit-text-size-adjust:100%}
body{-webkit-tap-highlight-color:transparent}
button,a,[role="button"]{touch-action:manipulation}
.wenikHomeDash{margin:10px 18px 14px;border-radius:20px}
.wenikHomeDashSlide{min-height:82px;padding:12px 15px}
.wenikHomeDashSlide img{width:56px;height:56px;object-fit:cover;object-position:center;border-radius:14px;display:block;flex:0 0 56px}
.wenikHomeDashMedia{width:56px;height:56px;border-radius:14px;overflow:hidden;flex:0 0 56px;background:#f4eef8}
.wenikHomeDashMedia img{width:100%;height:100%;object-fit:cover;object-position:center;display:block}
.wenikHomeDashValue[data-wenik-points-value]{min-width:52px}
@media(max-width:390px){
  .wenikHomeDash{margin:9px 16px 12px;border-radius:18px}
  .wenikHomeDashSlide{min-height:76px;padding:11px 13px}
  .wenikHomeDashSlide img,.wenikHomeDashMedia{width:50px;height:50px;flex-basis:50px;border-radius:13px}
}
</style>
<script id="wenikCustomerHomeMobileFinishRuntimeV2">
(function(){
  function normalizePoints(){
    const el=document.querySelector('[data-wenik-points-value]');
    if(!el)return;
    const raw=(el.textContent||'').trim();
    if(!/\d/.test(raw)) el.innerHTML='0<small>POINTS</small>';
  }
  function boot(){normalizePoints();setTimeout(normalizePoints,500);setTimeout(normalizePoints,1500)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
'''

if '</head>' not in s:
    raise SystemExit('head anchor missing')
s = s.replace('</head>', block + '\n</head>', 1)
p.write_text(s, encoding='utf-8')
print('Customer Home mobile finish V2 applied')
