from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK CUSTOMER PARTNER CARD BADGE + EQUAL HEIGHT V1 */'
if marker in s:
    raise SystemExit('already applied')
style=r'''
<style id="wenikCustomerPartnerCardBadgeEqualHeightV1">
/* WENIK CUSTOMER PARTNER CARD BADGE + EQUAL HEIGHT V1 */
.wenikPartnerGrid{align-items:stretch!important}
.wenikPartnerCard{
  position:relative!important;
  display:flex!important;
  flex-direction:column!important;
  min-width:0!important;
  height:100%!important;
  overflow:hidden!important;
}
.wenikPartnerMedia{
  position:relative!important;
  flex:0 0 auto!important;
  width:100%!important;
  aspect-ratio:4/3!important;
  overflow:hidden!important;
}
.wenikPartnerMedia img{
  width:100%!important;
  height:100%!important;
  display:block!important;
  object-fit:cover!important;
  object-position:center!important;
}
.wenikOff{
  position:absolute!important;
  top:10px!important;
  left:10px!important;
  right:auto!important;
  bottom:auto!important;
  z-index:20!important;
  width:auto!important;
  max-width:calc(100% - 20px)!important;
  margin:0!important;
  padding:7px 10px!important;
  border-radius:999px!important;
  line-height:1!important;
  font-size:11px!important;
  font-weight:950!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
  background:rgba(255,255,255,.95)!important;
  color:#d95b16!important;
  border:1px solid rgba(255,255,255,.9)!important;
  box-shadow:0 5px 15px rgba(24,14,34,.18)!important;
  backdrop-filter:blur(8px)!important;
  -webkit-backdrop-filter:blur(8px)!important;
}
.wenikPartnerBody{
  flex:1 1 auto!important;
  display:flex!important;
  flex-direction:column!important;
  min-height:112px!important;
}
.wenikPartnerPromo{margin-top:auto!important;align-self:flex-start!important}
@media(max-width:390px){
  .wenikOff{top:8px!important;left:8px!important;padding:6px 8px!important;font-size:10px!important}
  .wenikPartnerBody{min-height:104px!important}
}
</style>
'''
if '</head>' not in s:
    raise SystemExit('head anchor missing')
s=s.replace('</head>',style+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Customer Partner card badge and equal height fix applied')
