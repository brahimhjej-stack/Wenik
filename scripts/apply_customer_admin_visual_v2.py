from pathlib import Path

# Customer: compact featured area
p=Path('index.html'); s=p.read_text()
if '/* WENIK FEATURED COMPACT V2 */' not in s:
    css='''\n<style>\n/* WENIK FEATURED COMPACT V2 */\n@media(max-width:640px){#home .carousel{height:180px!important;max-height:180px!important;overflow:hidden!important;border-radius:18px!important}#home .carousel img{width:100%!important;height:180px!important;max-height:180px!important;object-fit:cover!important;object-position:center!important}#home .carousel .slide,#home .carousel>div{max-height:180px!important}#home .sectionTitle{margin-top:9px!important;margin-bottom:5px!important}#home .wenikMiniDash{margin-bottom:7px!important}}\n</style>\n'''
    pos=s.lower().rfind('</head>'); assert pos>=0
    s=s[:pos]+css+s[pos:]; p.write_text(s)

# Admin + Super Admin: same bright WENIK spirit, no permission/logic changes
p=Path('admin.html'); a=p.read_text()
if '/* WENIK ADMIN SPIRIT V2 */' not in a:
    css='''\n<style>\n/* WENIK ADMIN SPIRIT V2 */\nbody:before{content:"";position:fixed;z-index:-1;inset:0 0 auto 0;height:150px;background:linear-gradient(115deg,rgba(143,36,255,.11),rgba(239,21,157,.09),rgba(255,111,33,.09),rgba(255,210,28,.08));pointer-events:none}\n.wrap:before{content:"WENIK.CO  ·  WIN - WIN";display:block;text-align:center;font-size:11px;font-weight:1000;letter-spacing:2.2px;color:#8f24ff;padding:4px 0 7px}\n#app>.hero{background:linear-gradient(115deg,#fff 0%,#fbf3ff 45%,#fff6ef 78%,#fffbea 100%)}\n#app>.hero:after{content:"MORE TO DISCOVER";display:block;margin-top:8px;font-size:10px;font-weight:1000;letter-spacing:1.6px;color:#a329b8}\n.card{border-radius:20px}.metric{border-top:3px solid transparent;border-image:linear-gradient(90deg,#8f24ff,#ef159d,#ff6f21,#ffd21c) 1}.tabs{scrollbar-width:none}.tabs::-webkit-scrollbar{display:none}\n@media(max-width:520px){.brand{text-align:center;font-size:27px}.sub{text-align:center}.hero,.card{padding:15px;border-radius:18px}.metric{padding:12px}.metric b{font-size:21px}.tab{padding:9px 11px;font-size:12px}}\n</style>\n'''
    pos=a.lower().rfind('</head>'); assert pos>=0
    a=a[:pos]+css+a[pos:]; p.write_text(a)
