from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* WENIK PARTNER CARD COMPACT BODY V1 */'
if marker in s:
    raise SystemExit('already applied')
style=r'''
<style id="wenikPartnerCardCompactBodyV1">
/* WENIK PARTNER CARD COMPACT BODY V1 */
.wenikPartnerBody{
  min-height:96px!important;
  padding:10px 12px 9px!important;
  flex:0 0 auto!important;
}
.wenikPartnerName{
  margin:0!important;
  font-size:15px!important;
  line-height:1.12!important;
}
.wenikPartnerMeta{
  margin-top:4px!important;
  font-size:11px!important;
  line-height:1.18!important;
}
.wenikPartnerFooter{
  margin-top:8px!important;
  padding-top:0!important;
  gap:6px!important;
}
.wenikPartnerFooter .wenikOff,
.wenikPartnerFooter .wenikPartnerBadge{
  padding:6px 9px!important;
  font-size:10px!important;
  max-width:calc(100% - 54px)!important;
}
.wenikPartnerView{
  min-width:46px!important;
  height:27px!important;
  padding:0 9px!important;
  font-size:10px!important;
}
@media(max-width:390px){
  .wenikPartnerBody{min-height:90px!important;padding:9px 9px 8px!important}
  .wenikPartnerName{font-size:13.5px!important}
  .wenikPartnerMeta{margin-top:3px!important;font-size:10px!important}
  .wenikPartnerFooter{margin-top:7px!important;gap:5px!important}
  .wenikPartnerFooter .wenikOff,.wenikPartnerFooter .wenikPartnerBadge{padding:5px 7px!important;font-size:9px!important;max-width:calc(100% - 46px)!important}
  .wenikPartnerView{min-width:40px!important;height:25px!important;padding:0 7px!important;font-size:9px!important}
}
</style>
'''
if '</head>' not in s:
    raise SystemExit('head anchor missing')
s=s.replace('</head>',style+'\n</head>',1)
p.write_text(s,encoding='utf-8')
print('Compact Partner card body applied')
