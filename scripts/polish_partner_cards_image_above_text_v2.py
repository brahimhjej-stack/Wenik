from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK PARTNER CARD IMAGE ABOVE TEXT PREMIUM V2 */'
if marker in s:
    raise SystemExit('already applied')
style=r'''
<style id="wenikPartnerImageAboveTextPremiumV2">
/* WENIK PARTNER CARD IMAGE ABOVE TEXT PREMIUM V2 */
.wenikPartnerGrid{
  gap:12px!important;
  align-items:stretch!important;
}
.wenikPartnerCard{
  position:relative!important;
  display:flex!important;
  flex-direction:column!important;
  height:100%!important;
  min-height:0!important;
  overflow:hidden!important;
  border-radius:22px!important;
  background:#fff!important;
  border:1px solid rgba(40,22,58,.08)!important;
  box-shadow:0 10px 28px rgba(45,24,63,.11)!important;
  transition:transform .18s ease,box-shadow .18s ease!important;
}
.wenikPartnerCard:active{transform:scale(.985)!important}
.wenikPartnerMedia{
  position:relative!important;
  width:100%!important;
  aspect-ratio:16/10!important;
  min-height:0!important;
  flex:0 0 auto!important;
  overflow:hidden!important;
  background:linear-gradient(135deg,#f4ebff,#fff1e8,#fff8d9)!important;
}
.wenikPartnerMedia>img,.wenikPartnerMedia img{
  width:100%!important;
  height:100%!important;
  max-width:none!important;
  display:block!important;
  object-fit:cover!important;
  object-position:center!important;
}
.wenikPartnerMedia:after{display:none!important}
.wenikPartnerPlaceholder{
  display:flex!important;
  align-items:center!important;
  justify-content:center!important;
  width:100%!important;
  height:100%!important;
  font-size:22px!important;
  font-weight:950!important;
  letter-spacing:-.4px!important;
  color:#7b2cff!important;
}
.wenikPartnerMedia .wenikOff,
.wenikPartnerCard>.wenikOff{
  position:absolute!important;
  top:10px!important;
  left:10px!important;
  right:auto!important;
  bottom:auto!important;
  z-index:30!important;
  width:auto!important;
  max-width:calc(100% - 20px)!important;
  margin:0!important;
  padding:7px 11px!important;
  border-radius:999px!important;
  background:linear-gradient(135deg,#ff7518,#ff5a00)!important;
  color:#fff!important;
  border:1px solid rgba(255,255,255,.65)!important;
  box-shadow:0 5px 14px rgba(31,17,18,.22)!important;
  font-size:11px!important;
  font-weight:950!important;
  line-height:1!important;
  letter-spacing:.1px!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
.wenikPartnerBody{
  position:relative!important;
  inset:auto!important;
  left:auto!important;
  right:auto!important;
  bottom:auto!important;
  z-index:auto!important;
  flex:1 1 auto!important;
  display:flex!important;
  flex-direction:column!important;
  min-height:112px!important;
  padding:12px 13px 13px!important;
  background:#fff!important;
  color:#21172d!important;
  pointer-events:auto!important;
}
.wenikPartnerName{
  color:#21172d!important;
  font-size:16px!important;
  font-weight:950!important;
  line-height:1.16!important;
  letter-spacing:-.2px!important;
  text-shadow:none!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
.wenikPartnerMeta{
  margin-top:6px!important;
  color:#7f7788!important;
  font-size:12px!important;
  font-weight:700!important;
  line-height:1.2!important;
  text-shadow:none!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
.wenikPartnerPromo{
  display:inline-flex!important;
  align-items:center!important;
  align-self:flex-start!important;
  max-width:100%!important;
  margin-top:auto!important;
  padding:6px 9px!important;
  min-height:0!important;
  border-radius:999px!important;
  background:linear-gradient(90deg,rgba(123,44,255,.08),rgba(255,111,33,.10))!important;
  color:#ce5c18!important;
  font-size:10.5px!important;
  font-weight:900!important;
  line-height:1.05!important;
  text-shadow:none!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
@media(max-width:390px){
  .wenikPartnerGrid{gap:10px!important}
  .wenikPartnerCard{border-radius:19px!important}
  .wenikPartnerMedia{aspect-ratio:16/10!important}
  .wenikPartnerBody{padding:10px 10px 11px!important;min-height:104px!important}
  .wenikPartnerName{font-size:14px!important}
  .wenikPartnerMeta{font-size:10.5px!important;margin-top:5px!important}
  .wenikPartnerPromo{font-size:9.5px!important;padding:5px 7px!important}
  .wenikPartnerMedia .wenikOff,.wenikPartnerCard>.wenikOff{top:8px!important;left:8px!important;padding:6px 8px!important;font-size:10px!important}
}
</style>
'''
if '</head>' not in s:
    raise SystemExit('head anchor missing')
s=s.replace('</head>',style+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Premium Partner image-above-text cards applied')
