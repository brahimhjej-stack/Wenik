from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
start='<!-- WENIK VISIBLE CUSTOMER LOGIN BRIDGE 20260912 START -->'
end='<!-- WENIK VISIBLE CUSTOMER LOGIN BRIDGE 20260912 END -->'
block=r'''<!-- WENIK VISIBLE CUSTOMER LOGIN BRIDGE 20260912 START -->
<script>
document.addEventListener('click',function(e){
  const clicked=e.target.closest('button#login');
  if(!clicked)return;
  const buttons=[...document.querySelectorAll('button#login')];
  if(buttons.length<2)return;
  const bound=buttons[0];
  if(clicked===bound)return;
  const visibleForm=clicked.closest('#loginForm');
  const boundForm=bound.closest('#loginForm');
  if(!visibleForm||!boundForm)return;
  e.preventDefault();
  e.stopImmediatePropagation();
  const vp=visibleForm.querySelector('#loginPhone');
  const vw=visibleForm.querySelector('#loginPassword');
  const bp=boundForm.querySelector('#loginPhone');
  const bw=boundForm.querySelector('#loginPassword');
  if(bp&&vp)bp.value=vp.value;
  if(bw&&vw)bw.value=vw.value;
  bound.click();
},true);
</script>
<!-- WENIK VISIBLE CUSTOMER LOGIN BRIDGE 20260912 END -->'''
if start in s and end in s:
    a=s.index(start);b=s.index(end,a)+len(end);s=s[:a]+block+s[b:]
else:
    s=s.replace('</body>',block+'\n</body>')
p.write_text(s,encoding='utf-8')
