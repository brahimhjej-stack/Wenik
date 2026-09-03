from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')
marker = '/* WENIK COLOR REFRESH — visual-only overrides, no functional changes */'

css = r'''
/* WENIK COLOR REFRESH — visual-only overrides, no functional changes */
:root{
  --bg:#06050d;
  --panel:rgba(15,12,27,.88);
  --line:rgba(178,92,255,.22);
  --muted:#b9b4c8;
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
    radial-gradient(circle at 10% -5%,rgba(143,36,255,.28) 0,transparent 30%),
    radial-gradient(circle at 92% 2%,rgba(255,111,33,.20) 0,transparent 27%),
    radial-gradient(circle at 55% 115%,rgba(239,21,157,.12) 0,transparent 30%),
    linear-gradient(180deg,#070610 0%,#090713 48%,#06050d 100%);
}
.top{
  background:linear-gradient(180deg,rgba(6,5,13,.99),rgba(8,6,17,.82),transparent);
}
.brandLogo{
  filter:drop-shadow(0 0 18px rgba(239,21,157,.18)) drop-shadow(0 0 26px rgba(255,174,0,.08));
}
.hero{
  position:relative;
  overflow:hidden;
  background:
    radial-gradient(circle at 0 0,rgba(143,36,255,.28),transparent 38%),
    radial-gradient(circle at 100% 100%,rgba(255,111,33,.18),transparent 40%),
    linear-gradient(145deg,rgba(30,14,60,.95),rgba(17,11,31,.94) 55%,rgba(34,14,24,.93));
  border:1px solid transparent;
  background-clip:padding-box;
  box-shadow:0 18px 55px rgba(0,0,0,.38),0 0 0 1px rgba(239,21,157,.08),0 0 34px rgba(143,36,255,.08);
}
.hero::before{
  content:"";
  position:absolute;inset:0 auto auto 0;width:100%;height:3px;
  background:linear-gradient(90deg,var(--purple),var(--pink),var(--orange),var(--yellow));
  opacity:.95;
}
.hero h2{
  background:linear-gradient(90deg,#fff 0%,#fff 44%,#ffd7ed 70%,#ffe6a6 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.card{
  background:linear-gradient(145deg,rgba(23,17,39,.94),rgba(12,11,23,.94));
  border:1px solid rgba(178,92,255,.20);
  box-shadow:0 14px 38px rgba(0,0,0,.26),inset 0 1px 0 rgba(255,255,255,.025);
}
.card:nth-of-type(4n+1){border-color:rgba(143,36,255,.28)}
.card:nth-of-type(4n+2){border-color:rgba(239,21,157,.24)}
.card:nth-of-type(4n+3){border-color:rgba(255,111,33,.24)}
.card:nth-of-type(4n+4){border-color:rgba(255,210,28,.20)}
.btn{
  background:linear-gradient(100deg,var(--purple) 0%,var(--pink) 38%,var(--orange) 72%,var(--yellow) 100%);
  color:#fff;
  text-shadow:0 1px 1px rgba(0,0,0,.18);
  box-shadow:0 10px 28px rgba(239,21,157,.18),0 0 0 1px rgba(255,255,255,.08) inset;
}
.btn.secondary{
  background:linear-gradient(145deg,rgba(43,24,68,.95),rgba(22,16,35,.96));
  color:#fff;
  border:1px solid rgba(143,36,255,.38);
  box-shadow:0 8px 20px rgba(92,33,214,.10);
}
.field{
  border:1px solid rgba(178,92,255,.22);
  background:linear-gradient(145deg,rgba(11,9,20,.98),rgba(18,11,26,.96));
}
.field:focus{
  border-color:var(--pink);
  box-shadow:0 0 0 3px rgba(239,21,157,.12),0 0 20px rgba(143,36,255,.08);
}
.nav{
  background:rgba(9,7,17,.90);
  border:1px solid rgba(178,92,255,.26);
  box-shadow:0 18px 55px rgba(0,0,0,.58),0 0 32px rgba(143,36,255,.09);
}
.nav button{color:#9e98ae}
.nav .active{
  color:#fff;
  background:linear-gradient(135deg,rgba(143,36,255,.48),rgba(239,21,157,.38) 45%,rgba(255,111,33,.34));
  box-shadow:0 7px 18px rgba(239,21,157,.13);
}
.badge{
  color:#fff;
  background:linear-gradient(100deg,rgba(143,36,255,.88),rgba(239,21,157,.88));
  box-shadow:0 4px 12px rgba(239,21,157,.18);
}
.dot{color:#fff;background:linear-gradient(90deg,var(--pink),var(--orange));}
.unread{
  border-color:rgba(239,21,157,.42);
  background:linear-gradient(145deg,rgba(75,25,91,.33),rgba(21,14,30,.92));
}
#qrImage{
  border:4px solid transparent;
  background:linear-gradient(#fff,#fff) padding-box,linear-gradient(135deg,var(--purple),var(--pink),var(--orange),var(--yellow)) border-box;
  box-shadow:0 18px 55px rgba(143,36,255,.17),0 0 32px rgba(255,111,33,.07);
}
.sectionTitle h2,.sectionTitle h3{
  background:linear-gradient(90deg,#fff 0%,#f7eaff 55%,#ffd797 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.partnerLogo{
  background:#171020;
  border:1px solid rgba(178,92,255,.25);
  box-shadow:0 6px 18px rgba(143,36,255,.10);
}
.chip{
  background:linear-gradient(145deg,rgba(40,21,61,.90),rgba(20,15,31,.92));
  border:1px solid rgba(239,21,157,.20);
  color:#f5edf9;
}
.price{
  background:linear-gradient(90deg,var(--pink),var(--orange),var(--yellow));
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.eyebrow{color:#ff9cdc;text-shadow:0 0 14px rgba(239,21,157,.20);}
.authTabs{gap:9px}
.authTab{
  border:1px solid rgba(178,92,255,.22);
  background:rgba(17,12,27,.95);
  color:#a8a1b6;
}
.authTab.active{
  color:#fff;
  background:linear-gradient(100deg,var(--purple),var(--pink),var(--orange));
  box-shadow:0 8px 22px rgba(239,21,157,.16);
}
.dots i{background:#4a4158}
.dots i.on{background:linear-gradient(90deg,var(--purple),var(--pink),var(--orange),var(--yellow))}
.slide .overlay{background:linear-gradient(transparent,rgba(5,4,11,.96));}
.focus{
  border-color:var(--pink);
  box-shadow:0 0 0 1px rgba(239,21,157,.65),0 16px 50px rgba(143,36,255,.16),0 0 30px rgba(255,111,33,.07);
}
.selected{
  outline:2px solid var(--yellow);
  box-shadow:0 0 0 4px rgba(255,210,28,.12),0 0 22px rgba(239,21,157,.12);
}
'''

if marker in html:
    print('WENIK color refresh already applied; no change needed.')
else:
    idx = html.find('</style>')
    if idx == -1:
        raise SystemExit('No </style> tag found; refusing to modify index.html')
    updated = html[:idx] + '\n' + css + '\n' + html[idx:]
    path.write_text(updated, encoding='utf-8')
    print('Applied WENIK customer color refresh to index.html')
