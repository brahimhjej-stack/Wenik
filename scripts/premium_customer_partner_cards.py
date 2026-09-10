from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK CUSTOMER PARTNER CARDS PREMIUM V1 */'
if marker in s:
    raise SystemExit('already applied')
style=r'''
<style id="wenikCustomerPartnerCardsPremiumV1">
/* WENIK CUSTOMER PARTNER CARDS PREMIUM V1 */
.wenikPartnerGrid{gap:14px!important}
.wenikPartnerCard{
  border-radius:22px!important;
  overflow:hidden!important;
  background:#fff!important;
  border:1px solid rgba(49,25,68,.08)!important;
  box-shadow:0 12px 30px rgba(52,27,70,.10)!important;
  transition:transform .18s ease,box-shadow .18s ease!important;
}
.wenikPartnerCard:active{transform:scale(.985)!important}
.wenikPartnerMedia{
  position:relative!important;
  width:100%!important;
  aspect-ratio:4/3!important;
  background:linear-gradient(135deg,#f4ebff,#fff1e8,#fff8d9)!important;
  overflow:hidden!important;
}
.wenikPartnerMedia:after{
  content:"";position:absolute;left:0;right:0;bottom:0;height:34%;pointer-events:none;
  background:linear-gradient(180deg,transparent,rgba(20,12,30,.10));
}
.wenikPartnerMedia img{width:100%!important;height:100%!important;object-fit:cover!important;display:block!important}
.wenikPartnerPlaceholder{font-size:22px!important;font-weight:950!important;letter-spacing:-.4px!important;color:#7b2cff!important}
.wenikOff{
  top:11px!important;left:11px!important;right:auto!important;
  padding:7px 10px!important;border-radius:999px!important;
  font-size:11px!important;font-weight:950!important;line-height:1!important;
  background:rgba(255,255,255,.94)!important;color:#d95b16!important;
  border:1px solid rgba(255,255,255,.82)!important;
  box-shadow:0 6px 18px rgba(31,18,44,.16)!important;
  backdrop-filter:blur(8px)!important;
}
.wenikPartnerBody{padding:13px 14px 15px!important}
.wenikPartnerName{
  font-size:16px!important;font-weight:950!important;line-height:1.18!important;
  color:#21172d!important;letter-spacing:-.25px!important;
  white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;
}
.wenikPartnerMeta{
  margin-top:7px!important;font-size:12px!important;font-weight:650!important;
  color:#786f80!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;
}
.wenikPartnerPromo{
  display:inline-flex!important;align-items:center!important;max-width:100%!important;
  min-height:0!important;margin-top:9px!important;padding:6px 9px!important;border-radius:999px!important;
  background:linear-gradient(90deg,rgba(123,44,255,.08),rgba(255,111,33,.08))!important;
  color:#c95d1c!important;font-size:11px!important;font-weight:900!important;
  white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important;
}
@media(max-width:390px){
  .wenikPartnerGrid{gap:10px!important}
  .wenikPartnerCard{border-radius:19px!important}
  .wenikPartnerBody{padding:11px 11px 13px!important}
  .wenikPartnerName{font-size:14px!important}
  .wenikPartnerMeta{font-size:11px!important}
  .wenikPartnerPromo{font-size:10px!important;padding:5px 8px!important}
}
</style>
'''
if '</head>' not in s:
    raise SystemExit('head anchor missing')
s=s.replace('</head>',style+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Premium Customer partner card styling applied')
