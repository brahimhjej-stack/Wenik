from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK PARTNER CARD LARGE IMAGE + TEXT OVERLAY V1 */'
if marker in s:
    raise SystemExit('already applied')
style=r'''
<style id="wenikPartnerLargeImageTextOverlayV1">
/* WENIK PARTNER CARD LARGE IMAGE + TEXT OVERLAY V1 */
.wenikPartnerCard{
  position:relative!important;
  overflow:hidden!important;
  min-height:0!important;
  background:#17131f!important;
}
.wenikPartnerMedia{
  position:relative!important;
  width:100%!important;
  aspect-ratio:5/4!important;
  min-height:0!important;
  overflow:hidden!important;
  background:linear-gradient(135deg,#f4ebff,#fff1e8,#fff8d9)!important;
}
.wenikPartnerMedia>img,
.wenikPartnerMedia img{
  width:100%!important;
  height:100%!important;
  max-width:none!important;
  display:block!important;
  object-fit:cover!important;
  object-position:center center!important;
}
.wenikPartnerMedia:after{
  content:""!important;
  position:absolute!important;
  inset:34% 0 0 0!important;
  z-index:2!important;
  pointer-events:none!important;
  background:linear-gradient(180deg,rgba(15,8,23,0) 0%,rgba(15,8,23,.18) 28%,rgba(15,8,23,.88) 100%)!important;
}
.wenikPartnerBody{
  position:absolute!important;
  left:0!important;right:0!important;bottom:0!important;
  z-index:12!important;
  padding:42px 13px 12px!important;
  background:transparent!important;
  pointer-events:none!important;
}
.wenikPartnerName{
  color:#fff!important;
  font-size:16px!important;
  font-weight:950!important;
  line-height:1.12!important;
  text-shadow:0 2px 8px rgba(0,0,0,.55)!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
.wenikPartnerMeta{
  margin-top:4px!important;
  color:rgba(255,255,255,.88)!important;
  font-size:11px!important;
  font-weight:750!important;
  text-shadow:0 2px 7px rgba(0,0,0,.5)!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
.wenikPartnerPromo{
  display:block!important;
  margin-top:5px!important;
  padding:0!important;
  min-height:0!important;
  border-radius:0!important;
  background:transparent!important;
  color:#fff!important;
  font-size:10px!important;
  font-weight:850!important;
  text-shadow:0 2px 7px rgba(0,0,0,.55)!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}
.wenikPartnerMedia .wenikOff{
  z-index:20!important;
}
@media(max-width:390px){
  .wenikPartnerMedia{aspect-ratio:5/4!important}
  .wenikPartnerBody{padding:38px 10px 10px!important}
  .wenikPartnerName{font-size:14px!important}
  .wenikPartnerMeta{font-size:10px!important}
  .wenikPartnerPromo{font-size:9px!important}
}
</style>
'''
if '</head>' not in s:
    raise SystemExit('head anchor missing')
s=s.replace('</head>',style+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Partner cards enlarged and text overlaid on image')
