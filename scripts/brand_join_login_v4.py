from pathlib import Path
p=Path('index.html'); s=p.read_text()
marker='/* WENIK JOIN LOGIN BRAND V4 */'
if marker in s: raise SystemExit('already patched')
css='''\n<style>\n/* WENIK JOIN LOGIN BRAND V4 */\n#auth{padding-top:0!important;overflow:hidden!important}\n#auth .authBrandV4{background:#fff!important;border-radius:0 0 22px 22px!important;padding:14px 10px 18px!important;margin:0 -1px 16px!important;text-align:center!important;position:relative!important;overflow:hidden!important;box-shadow:0 8px 24px rgba(60,20,80,.08)!important}\n#auth .authBrandV4:before,#auth .authBrandV4:after{content:"";position:absolute;bottom:-25px;width:58%;height:52px;background:linear-gradient(90deg,#8f24ff,#ef159d,#ff6f21,#ffd21c);opacity:.96}\n#auth .authBrandV4:before{left:-18%;transform:skewY(-10deg);border-radius:0 80% 0 0}\n#auth .authBrandV4:after{right:-18%;transform:skewY(10deg);border-radius:80% 0 0 0}\n#auth .authBrandV4 .abW{position:relative;z-index:2;font-size:56px;font-weight:1000;line-height:.82;background:linear-gradient(135deg,#8f24ff,#ef159d 50%,#ff6f21 78%,#ffd21c);-webkit-background-clip:text;background-clip:text;color:transparent}\n#auth .authBrandV4 .abName{position:relative;z-index:2;font-size:28px;font-weight:1000;line-height:1.1;margin-top:6px;color:#111}\n#auth .authBrandV4 .abName span{background:linear-gradient(90deg,#8f24ff,#ef159d,#ff6f21,#ffd21c);-webkit-background-clip:text;background-clip:text;color:transparent}\n#auth .authBrandV4 .abWin{position:relative;z-index:2;font-size:9px;font-weight:900;letter-spacing:4px;margin-top:4px;color:#111}\n#auth>.eyebrow{margin-top:14px}\n</style>\n'''
head=s.lower().rfind('</head>'); assert head>=0
s=s[:head]+css+s[head:]
needle='<section id="auth" class="hero">'; pos=s.find(needle); assert pos>=0
open_end=s.find('>',pos); assert open_end>=0
brand='''<div class="authBrandV4" aria-label="WENIK"><div class="abW">W</div><div class="abName"><span>WENIK</span>.CO</div><div class="abWin">— WIN - WIN —</div></div>'''
s=s[:open_end+1]+brand+s[open_end+1:]
p.write_text(s)
