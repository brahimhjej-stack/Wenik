from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
lines = s.splitlines()
idx = [i for i, line in enumerate(lines) if line.startswith('function wenikPartnerCard(x){')]
if len(idx) != 1:
    raise SystemExit(f'Expected exactly one wenikPartnerCard function line, found {len(idx)}')

i = idx[0]
old = lines[i]
if 'openWenikPartner' not in old:
    raise SystemExit('Target line does not contain openWenikPartner')

new = '''function wenikPartnerCard(x){const d=partnerDiscount(x),cat=displayPartnerCategory(x.category),img=x.logo_url?'<img style="position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:cover!important;object-position:center!important" src="'+esc(x.logo_url)+'" alt="'+esc(x.business_name)+'" loading="lazy" decoding="async">':'<div class="wenikPartnerPlaceholder">WENIK</div>';return'<article class="wenikPartnerCard" data-wenik-partner-id="'+esc(x.partner_id)+'" style="display:flex!important;flex-direction:column!important;height:auto!important;min-height:0!important;overflow:hidden!important" tabindex="0" onclick="openWenikPartner(this.dataset.wenikPartnerId)" onkeydown="if(event.key===&quot;Enter&quot;||event.key===&quot; &quot;){event.preventDefault();openWenikPartner(this.dataset.wenikPartnerId)}"><div class="wenikPartnerMedia" style="position:relative!important;display:block!important;width:100%!important;height:auto!important;aspect-ratio:1/1!important;overflow:hidden!important;flex:0 0 auto!important">'+img+(d?'<div class="wenikOff">'+esc(d)+'</div>':'')+'</div><div class="wenikPartnerBody" style="position:relative!important;display:block!important;width:100%!important;height:auto!important;min-height:118px!important;flex:0 0 auto!important;visibility:visible!important;opacity:1!important;background:#fff!important"><div class="wenikPartnerName" style="display:block!important;visibility:visible!important;opacity:1!important">'+esc(x.business_name)+'</div><div class="wenikPartnerMeta" style="display:block!important;visibility:visible!important;opacity:1!important">'+esc([x.area,cat].filter(Boolean).join(' · '))+'</div><div class="wenikPartnerPromo">'+esc(x.benefit_title||'WENIK PARTNER')+'</div></div></article>'}'''

lines[i] = new
out = '\n'.join(lines) + ('\n' if s.endswith('\n') else '')
if out == s:
    raise SystemExit('No change')
p.write_text(out, encoding='utf-8')
print('Fixed malformed inline quoting in wenikPartnerCard only; customer module can parse and bind LOGIN.')
# trigger workflow after workflow file exists
