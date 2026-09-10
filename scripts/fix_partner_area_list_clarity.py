from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

old = ".wenikAreaSearchMenu{position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:50;max-height:260px;overflow:auto;background:#16161d;border:1px solid rgba(255,255,255,.15);border-radius:14px;box-shadow:0 12px 30px rgba(0,0,0,.35);padding:6px}.wenikAreaSearchMenu.hidden{display:none}.wenikAreaOption{display:block;width:100%;border:0;background:transparent;color:#fff;text-align:left;padding:11px 12px;border-radius:10px;font:inherit;cursor:pointer}.wenikAreaOption:hover,.wenikAreaOption:focus{background:rgba(255,255,255,.09);outline:none}"
new = ".wenikAreaSearchMenu{position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:999;max-height:340px;overflow-y:auto;background:#fff;border:1px solid #e5e1ee;border-radius:16px;box-shadow:0 16px 38px rgba(23,12,44,.24);padding:6px;color:#17131f;-webkit-overflow-scrolling:touch}.wenikAreaSearchMenu.hidden{display:none}.wenikAreaOption{display:block;width:100%;min-height:52px;border:0;border-bottom:1px solid #eeeaf3;background:#fff;color:#17131f;text-align:left;padding:13px 16px;border-radius:0;font:inherit;font-size:17px;font-weight:650;line-height:1.25;cursor:pointer}.wenikAreaOption:first-child{background:#f1e8ff;color:#4d188f;border-radius:11px 11px 4px 4px}.wenikAreaOption:last-child{border-bottom:0;border-radius:0 0 11px 11px}.wenikAreaOption:hover,.wenikAreaOption:focus{background:#f5efff;color:#42147f;outline:none}"

if old in html:
    html = html.replace(old, new, 1)
elif new in html:
    print('Clear area list UI already applied.')
    raise SystemExit(0)
else:
    raise SystemExit('Expected WENIK V5 area menu styles not found; refusing unsafe patch')

path.write_text(html, encoding='utf-8')
print('WENIK clear white area list UI applied successfully.')
