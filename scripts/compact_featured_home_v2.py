from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='/* WENIK FEATURED COMPACT V2 */'
if marker in s:
    raise SystemExit('already patched')
css='''\n<style>\n/* WENIK FEATURED COMPACT V2 */\n@media(max-width:640px){\n  #home .carousel{height:180px!important;max-height:180px!important;overflow:hidden!important;border-radius:18px!important}\n  #home .carousel img{width:100%!important;height:180px!important;max-height:180px!important;object-fit:cover!important;object-position:center!important}\n  #home .carousel .slide,#home .carousel>div{max-height:180px!important}\n  #home .sectionTitle{margin-top:9px!important;margin-bottom:5px!important}\n  #home .wenikMiniDash{margin-bottom:7px!important}\n}\n</style>\n'''
pos=s.lower().rfind('</head>')
if pos<0: raise SystemExit('head not found')
s=s[:pos]+css+s[pos:]
p.write_text(s)
