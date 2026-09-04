from pathlib import Path
p=Path('index.html')
h=p.read_text(encoding='utf-8')
marker='/* WENIK INTERNAL BACK NAV V1 */'
if marker in h:
    print('back nav already applied'); raise SystemExit(0)
required=['id="shell"','id="nav"','id="wenikPartnerModal"','id="wenikPartnerClose"','window.tab=','openWenikPartner']
for t in required:
    if t not in h:
        raise SystemExit(f'missing {t}; refusing to patch')
js=r'''
<script>
/* WENIK INTERNAL BACK NAV V1 */
(() => {
  const views=['home','win','iza','qr','partners','me'];
  const byId=id=>document.getElementById(id);
  let applyingHistory=false, originalTab=null, originalOpenPartner=null;
  const visibleView=()=>views.find(id=>{const el=byId(id);return el&&!el.classList.contains('hidden')})||'home';
  const navButton=id=>[...(byId('nav')?.querySelectorAll('button')||[])].find(b=>(b.getAttribute('onclick')||'').includes("tab('"+id+"'"));
  const shellReady=()=>byId('shell')&&!byId('shell').classList.contains('hidden');
  const ensureRoot=()=>{
    if(!shellReady()) return;
    const v=visibleView();
    if(!history.state?.wenikInternal){history.replaceState({wenikInternal:true,view:v},'',location.href)}
  };
  const pushView=id=>{
    if(applyingHistory||!shellReady()) return;
    const st=history.state||{};
    if(st.wenikInternal&&st.view===id&&!st.partner) return;
    history.pushState({wenikInternal:true,view:id},'',location.href);
  };
  const closeModalOnly=()=>byId('wenikPartnerModal')?.classList.add('hidden');
  const install=()=>{
    ensureRoot();
    if(typeof window.tab==='function'&&!window.tab.__wenikBackWrapped){
      originalTab=window.tab;
      const wrapped=function(id,b){if(!applyingHistory)pushView(id);return originalTab(id,b)};
      wrapped.__wenikBackWrapped=true;
      window.tab=wrapped;
    }
    if(typeof window.openWenikPartner==='function'&&!window.openWenikPartner.__wenikBackWrapped){
      originalOpenPartner=window.openWenikPartner;
      const wrappedPartner=async function(id){
        if(!applyingHistory&&shellReady())history.pushState({wenikInternal:true,view:visibleView(),partner:id},'',location.href);
        return originalOpenPartner(id);
      };
      wrappedPartner.__wenikBackWrapped=true;
      window.openWenikPartner=wrappedPartner;
    }
    const close=byId('wenikPartnerClose');
    if(close&&!close.dataset.wenikBackBound){
      close.dataset.wenikBackBound='1';
      close.addEventListener('click',e=>{
        if(history.state?.wenikInternal&&history.state?.partner){e.preventDefault();e.stopImmediatePropagation();history.back()}
      },true);
    }
    const modal=byId('wenikPartnerModal');
    if(modal&&!modal.dataset.wenikBackBound){
      modal.dataset.wenikBackBound='1';
      modal.addEventListener('click',e=>{
        if(e.target===modal&&history.state?.wenikInternal&&history.state?.partner){e.preventDefault();e.stopImmediatePropagation();history.back()}
      },true);
    }
  };
  window.addEventListener('popstate',async e=>{
    const st=e.state;
    if(!st?.wenikInternal) return;
    applyingHistory=true;
    try{
      if(st.partner){
        if(originalTab) originalTab(st.view||'partners',navButton(st.view||'partners'));
        if(originalOpenPartner) await originalOpenPartner(st.partner);
      }else{
        closeModalOnly();
        if(originalTab) originalTab(st.view||'home',navButton(st.view||'home'));
      }
    }finally{applyingHistory=false}
  });
  window.addEventListener('load',()=>{setTimeout(install,0);setTimeout(install,700);setTimeout(install,1800)});
  const shell=byId('shell');
  if(shell)new MutationObserver(()=>{if(shellReady()){ensureRoot();install()}}).observe(shell,{attributes:true,attributeFilter:['class']});
})();
</script>
'''
pos=h.rfind('</body>')
if pos<0: raise SystemExit('no body close')
h=h[:pos]+js+'\n'+h[pos:]
p.write_text(h,encoding='utf-8')
print('internal back navigation applied')
