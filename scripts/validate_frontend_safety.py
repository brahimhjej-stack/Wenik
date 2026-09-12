from html.parser import HTMLParser
from pathlib import Path
from collections import Counter
import re
import sys

html_path = Path('index.html')
if not html_path.exists():
    raise SystemExit('index.html missing')

html = html_path.read_text(encoding='utf-8')

required_ids = {
    'joinTab','loginTab','joinForm','loginForm','loginPhone','loginPassword','login','msg',
    'shell','home','partners','me','qr'
}
ids = re.findall(r'\bid=["\']([^"\']+)["\']', html)
counts = Counter(ids)
missing = sorted(required_ids - set(ids))
duplicates = sorted(k for k,v in counts.items() if v > 1 and k in required_ids)
if missing:
    raise SystemExit('Missing critical IDs: ' + ', '.join(missing))
if duplicates:
    raise SystemExit('Duplicate critical IDs: ' + ', '.join(duplicates))

class ScriptCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script = False
        self.attrs = {}
        self.buf = []
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'script':
            self.in_script = True
            self.attrs = dict(attrs)
            self.buf = []
    def handle_data(self, data):
        if self.in_script:
            self.buf.append(data)
    def handle_endtag(self, tag):
        if tag.lower() == 'script' and self.in_script:
            self.scripts.append((self.attrs, ''.join(self.buf)))
            self.in_script = False
            self.attrs = {}
            self.buf = []

p = ScriptCollector()
p.feed(html)

out = Path('.safety-js')
out.mkdir(exist_ok=True)
written = 0
for i, (attrs, code) in enumerate(p.scripts):
    if attrs.get('src') or not code.strip():
        continue
    t = (attrs.get('type') or '').lower()
    if t in ('application/ld+json','application/json'):
        continue
    ext = '.mjs' if t == 'module' else '.js'
    (out / f'script_{i}{ext}').write_text(code, encoding='utf-8')
    written += 1

if written == 0:
    raise SystemExit('No inline JavaScript extracted')

print(f'HTML safety checks passed. Extracted {written} inline scripts for JS syntax validation.')
