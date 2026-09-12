from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
start='<!-- WENIK CUSTOMER LOGIN SELF-CONTAINED 20260912 START -->'
end='<!-- WENIK CUSTOMER LOGIN SELF-CONTAINED 20260912 END -->'
if s.count(start)!=1 or s.count(end)!=1:
    raise SystemExit('Expected exactly one temporary customer login override block')
a=s.index(start)
b=s.index(end,a)+len(end)
new=s[:a]+s[b:]
if new==s:
    raise SystemExit('No change')
p.write_text(new,encoding='utf-8')
print('Removed only temporary customer login override; original login and enter flow preserved.')
