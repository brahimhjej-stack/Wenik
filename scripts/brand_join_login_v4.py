from pathlib import Path
p=Path('index.html'); s=p.read_text()
marker='/* WENIK JOIN LOGIN BRAND V4 */'
if marker in s: raise SystemExit('already patched')
css='''\n<style>\n/* WENIK JOIN LOGIN BRAND V4 */\n#authScreen .authBrandV4{background:#fff!important;border-radius:0 0 22px 22px!important;padding:14px 10px 17px!important;margin:0 0 10px!important;text-align:center!important;position:relative!important;overflow:hidden!important;box-shadow:0 8px 24px rgba(60,20,80,.08)!important}\n#authScreen .authBrandV4:after{content:"";position:absolute;left:-5%;right:-5%;bottom:-25px;height:55px;background:linear-gradient(90deg,#8f24ff,#ef159d,#ff6f21,#ffd21c);transform:skewY(-4deg);opacity:.95}\n#authScreen .authBrandV4 .abW{font-size:55px;font-weight:1000;line-height:.8;background:linear-gradient(135deg,#8f24ff,#ef159d 50%,#ff6f21 78%,#ffd21c);-webkit-background-clip:text;background-clip:text;color:transparent}\n#authScreen .authBrandV4 .abName{font-size:28px;font-weight:1000;line-height:1.1}.authBrandV4 .abName span{background:linear-gradient(90deg,#8f24ff,#ef159d,#ff6f21,#ffd21c);-webkit-background-clip:text;background-clip:text;color:transparent}.authBrandV4 .abWin{font-size:9px;font-weight:900;letter-spacing:4px;margin-top:3px;position:relative;z-index:2}\n#authScreen .brandBanner,#authScreen .authBanner,#authScreen .loginBrandBanner{display:none!important}\n</style>\n'''
head=s.lower().rfind('</head>'); assert head>=0
s=s[:head]+css+s[head:]
# Inject compact white identity at beginning of auth screen. Detect auth container from JOIN US text.
pos=s.find('JOIN US'); assert pos>=0
# locate closest authScreen opening tag before JOIN US
needle='id="authScreen"'; a=s.rfind(needle,0,pos); assert a>=0
open_end=s.find('>',a); assert open_end>=0
brand='''<div class="authBrandV4"><div class="abW">W</div><div class="abName"><span>WENIK</span>.CO</div><div class="abWin">— WIN - WIN —</div></div>'''
s=s[:open_end+1]+brand+s[open_end+1:]
p.write_text(s)
