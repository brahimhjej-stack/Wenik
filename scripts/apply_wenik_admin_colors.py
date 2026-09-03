from pathlib import Path

path = Path('admin.html')
html = path.read_text(encoding='utf-8')
marker = '/* WENIK ADMIN COLOR REFRESH — visual-only */'
css = r'''
/* WENIK ADMIN COLOR REFRESH — visual-only */
:root{
  --purple:#8f24ff;
  --violet:#5b21d6;
  --pink:#ef159d;
  --coral:#ff3f64;
  --orange:#ff6f21;
  --amber:#ffae00;
  --yellow:#ffd21c;
}
body{
  background:
    radial-gradient(circle at 8% -8%,rgba(143,36,255,.30),transparent 31%),
    radial-gradient(circle at 94% 4%,rgba(255,111,33,.21),transparent 28%),
    radial-gradient(circle at 48% 112%,rgba(239,21,157,.13),transparent 32%),
    linear-gradient(180deg,#070610 0%,#090713 52%,#06050d 100%);
}
.logo{filter:drop-shadow(0 0 20px rgba(239,21,157,.20)) drop-shadow(0 0 28px rgba(255,174,0,.08))}
.hero{
  position:relative;overflow:hidden;
  background:
    radial-gradient(circle at 0 0,rgba(143,36,255,.32),transparent 40%),
    radial-gradient(circle at 100% 100%,rgba(255,111,33,.21),transparent 42%),
    linear-gradient(145deg,rgba(31,14,63,.96),rgba(16,11,30,.96) 55%,rgba(34,14,24,.95));
  border-color:rgba(178,92,255,.30);
  box-shadow:0 20px 58px rgba(0,0,0,.42),0 0 0 1px rgba(239,21,157,.08),0 0 36px rgba(143,36,255,.10);
}
.hero::before{content:"";position:absolute;inset:0 auto auto 0;width:100%;height:3px;background:linear-gradient(90deg,var(--purple),var(--pink),var(--orange),var(--yellow))}
.card,.metric{background:linear-gradient(145deg,rgba(23,17,39,.96),rgba(12,11,23,.96));border-color:rgba(178,92,255,.22);box-shadow:0 14px 38px rgba(0,0,0,.27),inset 0 1px 0 rgba(255,255,255,.025)}
.metric:nth-child(4n+1){border-color:rgba(143,36,255,.34)}
.metric:nth-child(4n+2){border-color:rgba(239,21,157,.30)}
.metric:nth-child(4n+3){border-color:rgba(255,111,33,.30)}
.metric:nth-child(4n+4){border-color:rgba(255,210,28,.25)}
.metric b{background:linear-gradient(90deg,#fff,#ffd5ed 58%,#ffe29b);-webkit-background-clip:text;background-clip:text;color:transparent}
.eyebrow{color:#ff9cdc;text-shadow:0 0 14px rgba(239,21,157,.22)}
h1,h2,h3{background:linear-gradient(90deg,#fff 0%,#f7eaff 55%,#ffe09d 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.field{border-color:rgba(178,92,255,.25);background:linear-gradient(145deg,rgba(11,9,20,.98),rgba(18,11,26,.97))}
.field:focus{outline:none;border-color:var(--pink);box-shadow:0 0 0 3px rgba(239,21,157,.12),0 0 22px rgba(143,36,255,.09)}
.btn{background:linear-gradient(100deg,var(--purple) 0%,var(--pink) 38%,var(--orange) 72%,var(--yellow) 100%);color:#fff;text-shadow:0 1px 1px rgba(0,0,0,.18);box-shadow:0 10px 30px rgba(239,21,157,.19),0 0 0 1px rgba(255,255,255,.08) inset}
.btn.secondary{background:linear-gradient(145deg,rgba(43,24,68,.95),rgba(22,16,35,.96));color:#fff;border-color:rgba(143,36,255,.38);box-shadow:0 8px 20px rgba(92,33,214,.10)}
.partner{border-left:3px solid var(--purple)}
.partner:nth-child(3n+2){border-left-color:var(--pink)}
.partner:nth-child(3n+3){border-left-color:var(--orange)}
.row b{color:#fff}
.error{color:#ff93a8}
'''
if marker in html:
    print('Admin colors already applied; no change.')
else:
    idx = html.find('</style>')
    if idx == -1:
        raise SystemExit('No </style> tag found; refusing to modify admin.html')
    updated = html[:idx] + '\n' + css + '\n' + html[idx:]
    path.write_text(updated, encoding='utf-8')
    print('Applied WENIK admin color refresh')
