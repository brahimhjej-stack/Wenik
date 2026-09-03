from pathlib import Path

# Trigger-safe visual updater for WENIK Partner.
path = Path('partner.html')
html = path.read_text(encoding='utf-8')
marker = '/* WENIK PARTNER COLOR REFRESH — visual-only */'
css = r'''
/* WENIK PARTNER COLOR REFRESH — visual-only */
:root{
  --purple:#8f24ff;
  --pink:#ef159d;
  --orange:#ff6f21;
  --yellow:#ffd21c;
}
body{
  background:
    radial-gradient(circle at 10% -5%,rgba(143,36,255,.28) 0,transparent 30%),
    radial-gradient(circle at 92% 2%,rgba(255,111,33,.20) 0,transparent 27%),
    radial-gradient(circle at 55% 115%,rgba(239,21,157,.12) 0,transparent 30%),
    linear-gradient(180deg,#070610 0%,#090713 48%,#06050d 100%);
}
.logo{filter:drop-shadow(0 0 18px rgba(239,21,157,.18)) drop-shadow(0 0 26px rgba(255,174,0,.08))}
.hero{
  position:relative;overflow:hidden;
  background:
    radial-gradient(circle at 0 0,rgba(143,36,255,.30),transparent 38%),
    radial-gradient(circle at 100% 100%,rgba(255,111,33,.20),transparent 40%),
    linear-gradient(145deg,rgba(30,14,60,.96),rgba(17,11,31,.95) 55%,rgba(34,14,24,.94));
  border-color:rgba(178,92,255,.28);
  box-shadow:0 18px 55px rgba(0,0,0,.38),0 0 0 1px rgba(239,21,157,.08),0 0 34px rgba(143,36,255,.09);
}
.hero::before{content:"";position:absolute;inset:0 auto auto 0;width:100%;height:3px;background:linear-gradient(90deg,var(--purple),var(--pink),var(--orange),var(--yellow))}
.card{background:linear-gradient(145deg,rgba(23,17,39,.95),rgba(12,11,23,.95));border-color:rgba(178,92,255,.22);box-shadow:0 14px 38px rgba(0,0,0,.28)}
.eyebrow{color:#ff9cdc;text-shadow:0 0 14px rgba(239,21,157,.20)}
h1,h2{background:linear-gradient(90deg,#fff 0%,#f8ecff 60%,#ffe4a3 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.field{border-color:rgba(178,92,255,.24);background:linear-gradient(145deg,rgba(11,9,20,.98),rgba(18,11,26,.96))}
.field:focus{outline:none;border-color:var(--pink);box-shadow:0 0 0 3px rgba(239,21,157,.12),0 0 20px rgba(143,36,255,.08)}
.btn{background:linear-gradient(100deg,var(--purple) 0%,var(--pink) 38%,var(--orange) 72%,var(--yellow) 100%);color:#fff;text-shadow:0 1px 1px rgba(0,0,0,.18);box-shadow:0 10px 28px rgba(239,21,157,.18),0 0 0 1px rgba(255,255,255,.08) inset}
.btn.secondary{background:linear-gradient(145deg,rgba(43,24,68,.95),rgba(22,16,35,.96));color:#fff;border-color:rgba(143,36,255,.38);box-shadow:0 8px 20px rgba(92,33,214,.10)}
video{border:2px solid transparent;background:linear-gradient(#000,#000) padding-box,linear-gradient(135deg,var(--purple),var(--pink),var(--orange),var(--yellow)) border-box;box-shadow:0 16px 38px rgba(143,36,255,.12)}
.success{color:#79f1c6}.error{color:#ff93a8}
'''
if marker in html:
    print('Partner colors already applied; no change.')
else:
    idx = html.find('</style>')
    if idx == -1:
        raise SystemExit('No </style> tag found; refusing to modify partner.html')
    updated = html[:idx] + '\n' + css + '\n' + html[idx:]
    path.write_text(updated, encoding='utf-8')
    print('Applied WENIK partner color refresh')
