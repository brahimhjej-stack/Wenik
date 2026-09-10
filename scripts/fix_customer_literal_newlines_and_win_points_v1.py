from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* WENIK CUSTOMER FINAL CLEANUP V1 */'
if marker in s:
    raise SystemExit('already applied')

block = r'''
<style id="wenikCustomerFinalCleanupV1">
/* WENIK CUSTOMER FINAL CLEANUP V1 */
.wenikWinPointsReadable,
.wenikWinPointsReadable *{
  color:#ffffff!important;
  opacity:1!important;
  -webkit-text-fill-color:#ffffff!important;
  text-shadow:0 2px 10px rgba(0,0,0,.28)!important;
}
.wenikWinPointsReadable{
  font-weight:950!important;
  letter-spacing:-1px!important;
}
</style>
<script id="wenikCustomerFinalCleanupRuntimeV1">
(function(){
  function cleanLiteralNewlines(){
    const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
    const remove=[];
    let n;
    while(n=walker.nextNode()){
      const v=n.nodeValue||'';
      if(v.trim()==='\\n\\n' || v.trim()==='\\n' || /^\\n(?:\\n)+$/.test(v.trim())) remove.push(n);
    }
    remove.forEach(n=>n.nodeValue='');
    document.querySelectorAll('body *').forEach(el=>{
      if(el.children.length===0){
        const t=(el.textContent||'').trim();
        if(t==='\\n\\n' || t==='\\n') el.remove();
      }
    });
  }
  function makeWinPointsReadable(){
    document.querySelectorAll('body *').forEach(el=>{
      const t=(el.textContent||'').replace(/\s+/g,' ').trim();
      if(/^\d[\d,]*\s*PTS$/i.test(t) && el.children.length<=3){
        el.classList.add('wenikWinPointsReadable');
      }
    });
  }
  function boot(){
    cleanLiteralNewlines();
    makeWinPointsReadable();
    setTimeout(cleanLiteralNewlines,400);
    setTimeout(makeWinPointsReadable,400);
    setTimeout(makeWinPointsReadable,1400);
    const mo=new MutationObserver(()=>{cleanLiteralNewlines();makeWinPointsReadable()});
    mo.observe(document.body,{childList:true,subtree:true,characterData:true});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
'''

if '</head>' not in s:
    raise SystemExit('head anchor missing')
s = s.replace('</head>', block + '\n</head>', 1)
p.write_text(s, encoding='utf-8')
print('Customer final cleanup V1 applied')
