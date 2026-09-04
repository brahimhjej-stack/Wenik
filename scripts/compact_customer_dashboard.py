from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
anchor='</style>'
assert anchor in s
css=r'''

/* WENIK CUSTOMER COMPACT DASHBOARD V1 */
@media(max-width:640px){
  .app{padding:10px 10px 92px}
  .top{padding:5px 0 7px}
  .brandLogo{width:76px;max-width:24vw}
  #shell .hero{padding:14px 15px;border-radius:19px}
  #shell .hero h2{font-size:23px;line-height:1.05;margin:4px 0 3px;letter-spacing:-.6px}
  #shell .hero .eyebrow{font-size:10px;letter-spacing:1.5px}
  #shell .hero .muted{font-size:12px;line-height:1.35}
  #shell .card{padding:12px;border-radius:17px;margin-top:8px}
  #shell .sectionTitle{margin:13px 2px 6px}
  #shell .sectionTitle h3{font-size:14px;margin:0}
  #shell .sectionTitle .muted{font-size:11px}
  #shell .btn,#shell .field{padding:10px 11px;margin-top:7px;border-radius:12px;font-size:13px}
  #home .carousel{margin-top:6px}
  #home .wenikDiscovery{padding:11px}
  #homeViewAllPartners{margin-top:8px!important}
  .wenikWinGiftGrid,.wenikPartnerGrid{gap:8px}
  .wenikWinGift{padding:11px!important}
  #qr .card{padding:12px}
  #qrImage{max-width:220px!important;margin:auto;display:block}
}
'''
assert 'WENIK CUSTOMER COMPACT DASHBOARD V1' not in s
s=s.replace(anchor,css+'\n'+anchor,1)
p.write_text(s,encoding='utf-8')
print('Applied compact customer dashboard styles.')
