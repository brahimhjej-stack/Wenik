from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
start='<!-- WENIK CUSTOMER LOGIN BUTTON FIX 20260912 START -->'
end='<!-- WENIK CUSTOMER LOGIN BUTTON FIX 20260912 END -->'
if start in s and end in s:
    a=s.index(start)
    b=s.index(end,a)+len(end)
    s=s[:a]+s[b:]
    p.write_text(s,encoding='utf-8')
else:
    raise SystemExit('customer login override block not found')
