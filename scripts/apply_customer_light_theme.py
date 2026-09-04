from pathlib import Path
p=Path('index.html')
h=p.read_text(encoding='utf-8')
marker='/* WENIK CUSTOMER LIGHT THEME V1 */'
if marker in h:
    print('already applied'); raise SystemExit(0)
if '/* WENIK PARTNER DISCOVERY V1 */' not in h:
    raise SystemExit('partner discovery missing')
css=r'''
/* WENIK CUSTOMER LIGHT THEME V1 */
:root{--lp:#7b2cff;--lo:#ff6f21;--ly:#ffd21c;--li:#21172d;--lm:#756b7d;--ll:#ece5f2}
html,body{background:#fbfafc!important;color:var(--li)!important}
body:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:-1;background:linear-gradient(125deg,rgba(123,44,255,.045),transparent 30%),linear-gradient(305deg,rgba(255,111,33,.045),transparent 32%)}
.card{background:#fff!important;color:var(--li)!important;border:1px solid var(--ll)!important;box-shadow:0 8px 24px rgba(52,27,70,.065)!important}
.muted,.wenikDiscoverySub,.wenikPartnerMeta,.wenikDetailMeta{color:var(--lm)!important}
.sectionTitle h3,.wenikDiscoveryTitle,.wenikPartnerName,.wenikDetailName{color:var(--li)!important}
.field,input,select,textarea{background:#fff!important;color:var(--li)!important;border:1px solid #ded4e7!important;box-shadow:none!important}
.btn{background:linear-gradient(100deg,var(--lp),#b02fff)!important;color:#fff!important;border:0!important}.btn.secondary{background:#fff!important;color:var(--lp)!important;border:1px solid rgba(123,44,255,.24)!important;box-shadow:none!important}
.wenikDiscovery{position:relative;background:#fff!important}.wenikDiscovery:before{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:linear-gradient(90deg,var(--lp) 0 38%,var(--lo) 38% 72%,var(--ly) 72%)}
.wenikCat{color:var(--li)!important}.wenikCatCircle{background:#fff!important;border:1px solid #eadff1!important;box-shadow:0 7px 18px rgba(52,27,70,.07)!important}.wenikCat.active .wenikCatCircle{outline:2px solid var(--lp)!important;box-shadow:0 0 0 4px rgba(123,44,255,.07)!important}.wenikCatLabel{color:#665d6d!important}
.wenikPartnerCard{background:#fff!important;border:1px solid var(--ll)!important;box-shadow:0 8px 22px rgba(52,27,70,.08)!important}.wenikPartnerMedia{background:linear-gradient(135deg,#f6efff,#fff5ec,#fffbea)!important}.wenikPartnerPlaceholder{color:var(--lp)!important}.wenikPartnerPromo{color:#d85b16!important}.wenikOff{background:linear-gradient(100deg,var(--lp),var(--lo),#f0b800)!important;color:#fff!important}
.wenikEmpty{color:var(--lm)!important;border-color:#e4d9eb!important;background:#fff!important}.wenikPartnerModal{background:rgba(35,22,44,.42)!important}.wenikPartnerSheet{background:#fff!important;color:var(--li)!important;border-color:#e6ddeb!important}.wenikModalClose{background:#fff!important;color:var(--li)!important;border-color:#e3dbe8!important}.wenikDetailHero{background:linear-gradient(135deg,#f5edff,#fff3ea,#fff9dc)!important}.wenikDetailPromo{background:linear-gradient(120deg,rgba(123,44,255,.07),rgba(255,111,33,.07),rgba(255,210,28,.10))!important;border-color:#eadff0!important}.wenikDetailPromo strong{color:#d85b16!important}.wenikDetailActions a{background:#faf7fc!important;border-color:#e3d7eb!important;color:#6f25d9!important}
.nav{background:rgba(255,255,255,.97)!important;border-color:#e8e0ed!important;box-shadow:0 -8px 25px rgba(52,27,70,.08)!important}.nav button{color:#756b7d!important}.nav button.active{color:var(--lp)!important}
'''
i=h.find('</style>')
if i<0: raise SystemExit('style missing')
h=h[:i]+'\n'+css+'\n'+h[i:]
p.write_text(h,encoding='utf-8')
print('light theme applied')
