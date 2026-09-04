from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""      const logo=x.partner_logo_url?'<img class=\"wenikWinGiftLogo\" src=\"'+esc(x.partner_logo_url)+'\" alt=\"'+esc(x.partner_name||'WENIK Partner')+'\" loading=\"lazy\">':'<div class=\"wenikWinGiftLogoFallback\">W</div>';\n      const value=x.stated_value!=null&&Number(x.stated_value)>0?'$'+Number(x.stated_value).toLocaleString():'';\n"""
new="""      const logoUrl=safeUrl(x.partner_logo_url);\n      const logo=logoUrl?'<img class=\"wenikWinGiftLogo\" src=\"'+esc(logoUrl)+'\" alt=\"'+esc(x.partner_name||'WENIK Partner')+'\" loading=\"lazy\">':'<div class=\"wenikWinGiftLogoFallback\">W</div>';\n      const value=''; // Gift title/description/conditions carry the exact benefit until typed gift values exist. Never infer USD or %.\n"""
assert old in s, 'WIN card legacy rendering anchor missing'
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Hardened customer WIN cards')
