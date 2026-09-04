from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')
marker = '/* WENIK HOME CATEGORIES FIRST V1 */'

old = '''        <div id="homePartnerGrid" class="wenikPartnerGrid"><div class="wenikEmpty">Loading partners…</div></div>\n        <div id="homePartnerCategories" class="wenikCategories" style="margin-top:14px"></div>'''
new = '''        <div id="homePartnerCategories" class="wenikCategories"></div>\n        <div id="homePartnerGrid" class="wenikPartnerGrid"><div class="wenikEmpty">Loading partners…</div></div>'''

if marker in html:
    print('Categories-first Home order already applied.')
    raise SystemExit(0)

if old not in html:
    if new in html:
        print('Home is already categories-first; no change needed.')
        raise SystemExit(0)
    raise SystemExit('Expected Home Partner/Categories block not found; refusing to modify index.html')

html = html.replace(old, new, 1)

style_anchor = '</style>'
if style_anchor not in html:
    raise SystemExit('Missing </style>; refusing to modify index.html')
html = html.replace(style_anchor, f'\n{marker}\n{style_anchor}', 1)

path.write_text(html, encoding='utf-8')
print('Restored Home order: Dashboard -> Categories -> Partners.')
