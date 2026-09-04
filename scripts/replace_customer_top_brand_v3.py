from pathlib import Path
p=Path('index.html'); s=p.read_text()
marker='/* WENIK WHITE BRAND HEADER V3 */'
if marker in s: raise SystemExit('already patched')
css='''\n<style>\n/* WENIK WHITE BRAND HEADER V3 */\n.wenikBrandPoster{position:relative;overflow:hidden;background:#fff;border-radius:0 0 24px 24px;padding:18px 16px 20px;text-align:center;box-shadow:0 10px 30px rgba(43,20,70,.07)}\n.wenikBrandPoster:before,.wenikBrandPoster:after{content:"";position:absolute;bottom:-30px;width:55%;height:78px;background:linear-gradient(105deg,#8f24ff,#ef159d,#ff6f21,#ffd21c);transform:skewY(-11deg);opacity:.98}.wenikBrandPoster:before{left:-20%;border-radius:0 90% 0 0}.wenikBrandPoster:after{right:-20%;transform:skewY(11deg);border-radius:90% 0 0 0}.wenikBrandMark{position:relative;z-index:2;font-size:74px;font-weight:1000;line-height:.8;letter-spacing:-12px;background:linear-gradient(135deg,#8f24ff 10%,#ef159d 48%,#ff6f21 75%,#ffd21c);-webkit-background-clip:text;background-clip:text;color:transparent}.wenikBrandName{position:relative;z-index:2;font-size:36px;font-weight:1000;letter-spacing:-1.5px;margin-top:10px}.wenikBrandName span{background:linear-gradient(90deg,#8f24ff,#ef159d,#ff6f21,#ffd21c);-webkit-background-clip:text;background-clip:text;color:transparent}.wenikBrandWin{position:relative;z-index:2;font-size:13px;font-weight:900;letter-spacing:6px;margin:2px 0 13px}.wenikBrandActions{position:relative;z-index:2;display:grid;grid-template-columns:repeat(4,1fr);gap:5px;max-width:520px;margin:0 auto 13px}.wenikBrandAction b{display:block;font-size:11px}.wenikBrandAction small{font-size:7px;color:#666}.wenikBrandIcon{font-size:22px;line-height:1.15}.wenikBrandUrl{position:relative;z-index:2;display:inline-block;border:1.5px solid #ff8b32;border-radius:999px;padding:6px 22px;background:#fff;font-size:11px;font-weight:900;letter-spacing:2px}\n@media(max-width:640px){.wenikBrandPoster{padding:14px 10px 18px}.wenikBrandMark{font-size:60px}.wenikBrandName{font-size:31px;margin-top:8px}.wenikBrandWin{font-size:11px;margin-bottom:10px}.wenikBrandActions{gap:2px;margin-bottom:10px}.wenikBrandAction b{font-size:9px}.wenikBrandAction small{font-size:6px}.wenikBrandIcon{font-size:19px}.wenikBrandUrl{padding:5px 18px;font-size:9px}}\n</style>\n'''
head=s.lower().rfind('</head>'); assert head>=0
s=s[:head]+css+s[head:]
# Replace the old dark/logo top visual if identifiable, otherwise inject before MORE TO DISCOVER hero.
poster='''<section class="wenikBrandPoster" aria-label="WENIK"><div class="wenikBrandMark">W</div><div class="wenikBrandName"><span>WENIK</span>.CO</div><div class="wenikBrandWin">— WIN - WIN —</div><div class="wenikBrandActions"><div class="wenikBrandAction"><div class="wenikBrandIcon">🎁</div><b>REWARDS</b><small>MORE IS YOURS</small></div><div class="wenikBrandAction"><div class="wenikBrandIcon">🤝</div><b>PARTNERS</b><small>TOGETHER WE GROW</small></div><div class="wenikBrandAction"><div class="wenikBrandIcon">▣</div><b>SCAN</b><small>EARN & WIN</small></div><div class="wenikBrandAction"><div class="wenikBrandIcon">📈</div><b>GROW</b><small>MORE TOGETHER</small></div></div><div class="wenikBrandUrl">◎ WWW.WENIK.CO</div></section>'''
# Target the home page before the known MORE TO DISCOVER hero; remove only the immediately preceding old top banner block when marked by known logo image area.
needle='MORE TO DISCOVER'
pos=s.find(needle); assert pos>=0
# find nearest opening element around hero and inject poster before it; CSS hides legacy top banner if present via first home media/banner selector added below.
start=s.rfind('<',0,pos)
# safer structural injection before nearest containing section/div with class hero by searching backwards
hero=s.rfind('<div',0,pos)
if hero<0: hero=s.rfind('<section',0,pos)
assert hero>=0
s=s[:hero]+poster+s[hero:]
# Hide legacy oversized banner at top of home without touching the new poster.
extra='''\n<style>/* WENIK LEGACY TOP HIDE V3 */#home .wenikBrandPoster~.wenikBrandPoster{display:none!important}</style>\n'''
s=s.replace('</head>',extra+'</head>',1)
p.write_text(s)
