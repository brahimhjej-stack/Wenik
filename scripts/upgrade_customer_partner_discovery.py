from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')
marker = '/* WENIK PARTNER DISCOVERY V1 */'

if marker in html:
    print('WENIK partner discovery already applied; no change needed.')
    raise SystemExit(0)

required = [
    'id="homeAds"',
    '<div class="muted">WENIK ID</div>',
    'id="partnerCategory"',
    'id="partnerArea"',
    'id="partnerSearch"',
    'id="partnerList"',
    'id="navRewards"',
]
for token in required:
    if token not in html:
        raise SystemExit(f'Required marker missing: {token}; refusing to modify index.html')

css = r'''
/* WENIK PARTNER DISCOVERY V1 */
.wenik-discovery-card{padding:14px 12px 16px;overflow:hidden}
.wenik-discovery-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px}
.wenik-discovery-title{font-size:19px;font-weight:950;letter-spacing:.2px}
.wenik-discovery-sub{font-size:12px;color:#bdb4cb;margin-top:3px}
.wenik-location-row{display:flex;gap:8px;align-items:center;margin:10px 0 12px}
.wenik-location-row select{flex:1;min-width:0;padding:10px 11px;border-radius:12px;background:#0b0a13;color:#fff;border:1px solid rgba(178,92,255,.30);font-weight:800}
.wenik-location-btn{width:auto!important;white-space:nowrap;padding:10px 12px!important;font-size:12px!important}
.wenik-category-strip{display:flex;gap:10px;overflow-x:auto;padding:2px 1px 10px;scroll-snap-type:x proximity}
.wenik-category-strip::-webkit-scrollbar{display:none}
.wenik-cat{min-width:76px;max-width:76px;border:0;background:transparent;color:#f8f5ff;padding:0;display:flex;flex-direction:column;align-items:center;gap:6px;scroll-snap-align:start}
.wenik-cat-circle{width:66px;height:66px;border-radius:50%;display:grid;place-items:center;font-size:25px;background:linear-gradient(145deg,rgba(143,36,255,.28),rgba(239,21,157,.20) 50%,rgba(255,111,33,.18));border:1px solid rgba(255,255,255,.12);box-shadow:0 8px 22px rgba(0,0,0,.26)}
.wenik-cat.active .wenik-cat-circle{outline:2px solid #ffd21c;box-shadow:0 0 0 4px rgba(255,210,28,.10),0 10px 28px rgba(143,36,255,.25)}
.wenik-cat-label{font-size:10.5px;line-height:1.15;text-align:center;color:#d9d3e3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:76px}
.wenik-partner-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:8px}
#partnerList.wenik-partner-grid{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:12px!important}
.wenik-partner-card{position:relative;overflow:hidden;border-radius:17px;background:linear-gradient(145deg,rgba(24,18,39,.98),rgba(10,9,18,.98));border:1px solid rgba(178,92,255,.22);box-shadow:0 12px 32px rgba(0,0,0,.30);cursor:pointer;min-width:0}
.wenik-partner-media{aspect-ratio:1.05/1;width:100%;background:linear-gradient(135deg,rgba(143,36,255,.28),rgba(239,21,157,.20),rgba(255,111,33,.20));display:grid;place-items:center;overflow:hidden}
.wenik-partner-media img{width:100%;height:100%;object-fit:cover;display:block}
.wenik-partner-placeholder{font-weight:950;font-size:20px;letter-spacing:.5px;color:#fff;text-align:center;padding:10px}
.wenik-off{position:absolute;top:9px;right:9px;z-index:2;padding:6px 8px;border-radius:10px;background:linear-gradient(100deg,#ef159d,#ff6f21,#ffd21c);color:#fff;font-weight:950;font-size:11px;box-shadow:0 8px 20px rgba(0,0,0,.28)}
.wenik-partner-body{padding:10px 10px 12px}
.wenik-partner-name{font-size:14px;font-weight:950;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wenik-partner-meta{font-size:11px;color:#bcb5c8;margin-top:5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wenik-partner-promo{font-size:11px;color:#ffd67a;font-weight:800;margin-top:7px;min-height:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wenik-view-all{margin-top:12px}
.wenik-empty{grid-column:1/-1;padding:24px 10px;text-align:center;color:#bcb5c8;border:1px dashed rgba(178,92,255,.25);border-radius:14px}
.wenik-partner-modal{position:fixed;inset:0;z-index:9999;background:rgba(3,2,7,.80);backdrop-filter:blur(8px);display:flex;align-items:flex-end;justify-content:center;padding:0}
.wenik-partner-modal.hidden{display:none!important}
.wenik-partner-sheet{width:min(720px,100%);max-height:91vh;overflow:auto;border-radius:24px 24px 0 0;background:linear-gradient(180deg,#171020,#090711);border:1px solid rgba(178,92,255,.28);box-shadow:0 -20px 70px rgba(0,0,0,.60);padding:14px 14px 28px;position:relative}
.wenik-modal-close{position:sticky;top:0;margin-left:auto;z-index:5;width:40px;height:40px;border-radius:50%;border:1px solid rgba(255,255,255,.15);background:rgba(9,7,17,.88);color:#fff;font-size:22px;display:grid;place-items:center}
.wenik-detail-hero{border-radius:18px;overflow:hidden;aspect-ratio:16/9;background:linear-gradient(135deg,rgba(143,36,255,.32),rgba(239,21,157,.22),rgba(255,111,33,.20));display:grid;place-items:center;margin-top:-30px}
.wenik-detail-hero img{width:100%;height:100%;object-fit:cover}
.wenik-detail-name{font-size:24px;font-weight:950;margin-top:14px}
.wenik-detail-meta{color:#bdb5c9;font-size:13px;margin-top:4px}
.wenik-detail-promo{margin-top:12px;border-radius:15px;padding:12px;background:linear-gradient(120deg,rgba(143,36,255,.28),rgba(239,21,157,.20),rgba(255,111,33,.16));border:1px solid rgba(255,210,28,.22)}
.wenik-detail-promo strong{display:block;color:#ffd66e;font-size:18px;margin-bottom:3px}
.wenik-detail-actions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:13px}
.wenik-detail-actions a{display:block;text-align:center;text-decoration:none;padding:11px 8px;border-radius:12px;background:rgba(143,36,255,.18);border:1px solid rgba(178,92,255,.26);color:#fff;font-weight:850;font-size:12px}
.wenik-detail-gallery{display:flex;gap:9px;overflow-x:auto;margin-top:12px}
.wenik-detail-gallery img{width:78%;aspect-ratio:16/10;object-fit:cover;border-radius:14px;border:1px solid rgba(255,255,255,.10)}
@media (max-width:390px){.wenik-partner-grid,#partnerList.wenik-partner-grid{gap:9px!important}.wenik-partner-name{font-size:13px}.wenik-location-btn{padding:10px 9px!important}.wenik-cat{min-width:70px;max-width:70px}.wenik-cat-circle{width:60px;height:60px}.wenik-cat-label{width:70px}}
'''

style_end = html.find('</style>')
if style_end == -1:
    raise SystemExit('No </style> tag found; refusing to modify index.html')
html = html[:style_end] + '\n' + css + '\n' + html[style_end:]

home_block = r'''

          <div class="card wenik-discovery-card" id="homePartnerDiscovery">
            <div class="wenik-discovery-head">
              <div>
                <div class="wenik-discovery-title">PARTNERS NEAR YOU</div>
                <div id="homePartnerLocationStatus" class="wenik-discovery-sub">Choose your area or use your location</div>
              </div>
            </div>
            <div class="wenik-location-row">
              <select id="homePartnerArea" aria-label="Partner area"><option value="">ALL AREAS</option></select>
              <button id="btnUseLocation" class="btn secondary wenik-location-btn" type="button">📍 MY LOCATION</button>
            </div>
            <div id="homePartnerCategories" class="wenik-category-strip"></div>
            <div id="homePartnerGrid" class="wenik-partner-grid"><div class="wenik-empty">Loading partners...</div></div>
            <button id="btnViewAllPartners" class="btn secondary wenik-view-all" type="button">VIEW ALL PARTNERS</button>
          </div>
'''

wenik_id_token = '<div class="muted">WENIK ID</div>'
wenik_id_pos = html.find(wenik_id_token)
card_pos = html.rfind('<div class="card">', 0, wenik_id_pos)
if card_pos == -1:
    raise SystemExit('Could not locate WENIK ID card; refusing to modify index.html')
html = html[:card_pos] + home_block + '\n          ' + html[card_pos:]

html = html.replace('<div id="partnerList"></div>', '<div id="partnerList" class="wenik-partner-grid"></div>', 1)

modal = r'''
  <div id="wenikPartnerModal" class="wenik-partner-modal hidden" role="dialog" aria-modal="true" aria-label="Partner details">
    <div class="wenik-partner-sheet">
      <button id="wenikPartnerClose" class="wenik-modal-close" type="button" aria-label="Close">×</button>
      <div id="wenikPartnerDetail"></div>
    </div>
  </div>
'''
body_end = html.rfind('</body>')
if body_end == -1:
    raise SystemExit('No </body> tag found; refusing to modify index.html')
html = html[:body_end] + modal + '\n' + html[body_end:]

js = r'''
<script>
/* WENIK PARTNER DISCOVERY V1 — additive customer UX; QR/WIN/IZA untouched */
(() => {
  const $ = (id) => document.getElementById(id);
  const esc = (v='') => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm = (v='') => String(v ?? '').trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9\u0600-\u06ff]+/g,' ');
  let directory = [];
  let homeCategory = '';
  let homeArea = localStorage.getItem('wenik_partner_area') || '';
  let loaded = false;

  const categoryIcon = (cat='') => {
    const c = norm(cat);
    if (/restaurant|food|مطعم|اكل|أكل/.test(c)) return '🍽️';
    if (/cafe|coffee|قهو|كاف/.test(c)) return '☕';
    if (/fashion|cloth|wear|ملابس|البسة|ألبسة/.test(c)) return '👕';
    if (/beauty|salon|spa|صالون|تجميل/.test(c)) return '✨';
    if (/jewel|ذهب|مجوهر/.test(c)) return '💎';
    if (/elect|phone|tech|كهرب|هاتف/.test(c)) return '📱';
    if (/hotel|resort|فندق|منتجع/.test(c)) return '🏨';
    if (/kids|play|entertain|اطفال|أطفال|ترفيه/.test(c)) return '🎈';
    if (/service|خدمات/.test(c)) return '🛠️';
    return '⭐';
  };

  const discountLabel = (p) => {
    const type = norm(p.benefit_type || '');
    const value = Number(p.benefit_value);
    if (Number.isFinite(value) && value > 0) {
      if (/percent|percentage|discount|خصم/.test(type)) return `${Math.round(value)}% OFF`;
      if (/cash|amount|fixed/.test(type)) return `$${value % 1 ? value.toFixed(2) : Math.round(value)} OFF`;
    }
    return p.benefit_title ? 'WENIK OFFER' : '';
  };

  const promoText = (p) => p.benefit_title || (discountLabel(p) ? `${discountLabel(p)} WITH WENIK` : 'WENIK PARTNER');

  const cardHtml = (p) => {
    const badge = discountLabel(p);
    const logo = p.logo_url ? `<img src="${esc(p.logo_url)}" alt="${esc(p.business_name)}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=&quot;wenik-partner-placeholder&quot;>WENIK</div>'">` : `<div class="wenik-partner-placeholder">WENIK</div>`;
    return `<article class="wenik-partner-card" tabindex="0" data-wenik-partner="${esc(p.partner_id)}">
      ${badge ? `<div class="wenik-off">${esc(badge)}</div>` : ''}
      <div class="wenik-partner-media">${logo}</div>
      <div class="wenik-partner-body">
        <div class="wenik-partner-name">${esc(p.business_name)}</div>
        <div class="wenik-partner-meta">${esc([p.category,p.area].filter(Boolean).join(' • '))}</div>
        <div class="wenik-partner-promo">${esc(promoText(p))}</div>
      </div>
    </article>`;
  };

  const matches = (p, category, area, search='') => {
    if (category && norm(p.category) !== norm(category)) return false;
    if (area && norm(p.area) !== norm(area)) return false;
    if (search) {
      const hay = norm([p.business_name,p.category,p.area,p.benefit_title,p.benefit_conditions].filter(Boolean).join(' '));
      if (!hay.includes(norm(search))) return false;
    }
    return true;
  };

  const bindCards = (root) => {
    if (!root) return;
    root.querySelectorAll('[data-wenik-partner]').forEach(el => {
      const open = () => openPartner(el.dataset.wenikPartner);
      el.addEventListener('click', open);
      el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    });
  };

  const renderHome = () => {
    const grid = $('homePartnerGrid');
    if (!grid) return;
    const rows = directory.filter(p => matches(p, homeCategory, homeArea)).slice(0, 6);
    grid.innerHTML = rows.length ? rows.map(cardHtml).join('') : '<div class="wenik-empty">No partners found in this area yet.</div>';
    bindCards(grid);
  };

  const renderCategories = () => {
    const root = $('homePartnerCategories');
    if (!root) return;
    const cats = [...new Set(directory.map(p => p.category).filter(Boolean))].sort((a,b) => a.localeCompare(b));
    const all = `<button class="wenik-cat ${homeCategory ? '' : 'active'}" data-cat="" type="button"><span class="wenik-cat-circle">✨</span><span class="wenik-cat-label">ALL</span></button>`;
    root.innerHTML = all + cats.map(cat => `<button class="wenik-cat ${norm(cat)===norm(homeCategory)?'active':''}" data-cat="${esc(cat)}" type="button"><span class="wenik-cat-circle">${categoryIcon(cat)}</span><span class="wenik-cat-label">${esc(cat)}</span></button>`).join('');
    root.querySelectorAll('[data-cat]').forEach(btn => btn.addEventListener('click', () => {
      homeCategory = btn.dataset.cat || '';
      renderCategories();
      renderHome();
    }));
  };

  const populateArea = () => {
    const select = $('homePartnerArea');
    if (!select) return;
    const areas = [...new Set(directory.map(p => p.area).filter(Boolean))].sort((a,b) => a.localeCompare(b));
    select.innerHTML = '<option value="">ALL AREAS</option>' + areas.map(a => `<option value="${esc(a)}">${esc(a)}</option>`).join('');
    if (homeArea && areas.some(a => norm(a) === norm(homeArea))) {
      homeArea = areas.find(a => norm(a) === norm(homeArea));
      select.value = homeArea;
      $('homePartnerLocationStatus').textContent = `Showing ${homeArea}`;
    } else {
      homeArea = '';
      select.value = '';
    }
    select.addEventListener('change', () => {
      homeArea = select.value || '';
      if (homeArea) localStorage.setItem('wenik_partner_area', homeArea); else localStorage.removeItem('wenik_partner_area');
      $('homePartnerLocationStatus').textContent = homeArea ? `Showing ${homeArea}` : 'Showing all areas';
      renderHome();
    });
  };

  const CITY_POINTS = [
    {aliases:['nabatieh','nabatiyeh','النبطية'],lat:33.3772,lng:35.4838},
    {aliases:['sour','tyre','صور'],lat:33.2705,lng:35.2038},
    {aliases:['saida','sidon','صيدا'],lat:33.5571,lng:35.3729},
    {aliases:['beirut','بيروت'],lat:33.8938,lng:35.5018},
    {aliases:['baalbek','بعلبك'],lat:34.0047,lng:36.2110},
    {aliases:['zahle','zahle','زحلة'],lat:33.8463,lng:35.9020},
    {aliases:['tripoli','طرابلس'],lat:34.4367,lng:35.8497},
    {aliases:['jounieh','جونية'],lat:33.9808,lng:35.6178},
    {aliases:['aley','عاليه'],lat:33.8104,lng:35.5970},
    {aliases:['chouf','shouf','الشوف'],lat:33.6968,lng:35.5795}
  ];
  const hav = (lat1,lon1,lat2,lon2) => {
    const R=6371, dLat=(lat2-lat1)*Math.PI/180, dLon=(lon2-lon1)*Math.PI/180;
    const a=Math.sin(dLat/2)**2+Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLon/2)**2;
    return 2*R*Math.asin(Math.sqrt(a));
  };
  const detectArea = (lat,lng) => {
    const available = [...new Set(directory.map(p => p.area).filter(Boolean))];
    const candidates = CITY_POINTS.map(c => {
      const area = available.find(a => c.aliases.some(alias => norm(a).includes(norm(alias)) || norm(alias).includes(norm(a))));
      return area ? {...c,area,d: hav(lat,lng,c.lat,c.lng)} : null;
    }).filter(Boolean).sort((a,b)=>a.d-b.d);
    return candidates[0]?.d <= 35 ? candidates[0].area : '';
  };

  const useLocation = (silent=false) => {
    const status = $('homePartnerLocationStatus');
    if (!navigator.geolocation) { if(status) status.textContent='Location is not supported on this device'; return; }
    if(status) status.textContent='Getting your location...';
    navigator.geolocation.getCurrentPosition(pos => {
      const detected = detectArea(pos.coords.latitude, pos.coords.longitude);
      if (detected) {
        homeArea = detected;
        localStorage.setItem('wenik_partner_area', detected);
        const select = $('homePartnerArea'); if (select) select.value = detected;
        if(status) status.textContent = `Near you: ${detected}`;
        renderHome();
      } else if(status) {
        status.textContent='Location enabled — choose your area';
      }
    }, () => { if(status && !silent) status.textContent='Location not available — choose your area'; }, {enableHighAccuracy:false,timeout:7000,maximumAge:600000});
  };

  const renderPartnerTab = () => {
    const root = $('partnerList');
    if (!root || !directory.length) return;
    const category = $('partnerCategory')?.value || '';
    const area = $('partnerArea')?.value || '';
    const search = $('partnerSearch')?.value || '';
    const rows = directory.filter(p => matches(p, category, area, search));
    root.classList.add('wenik-partner-grid');
    root.innerHTML = rows.length ? rows.map(cardHtml).join('') : '<div class="wenik-empty">No partners found.</div>';
    bindCards(root);
  };

  const safeUrl = (u='') => /^https?:\/\//i.test(String(u)) ? String(u) : '';
  const openPartner = async (id) => {
    const p = directory.find(x => String(x.partner_id) === String(id));
    if (!p) return;
    const modal = $('wenikPartnerModal'), detail = $('wenikPartnerDetail');
    if (!modal || !detail) return;
    modal.classList.remove('hidden');
    document.body.style.overflow='hidden';
    let ads=[];
    try { const r = await sb.rpc('public_partner_ads',{p_partner_id:p.partner_id}); if (!r.error && Array.isArray(r.data)) ads=r.data; } catch(_) {}
    const hero = ads[0]?.image_url || p.logo_url || '';
    const socials = p.social_links && typeof p.social_links === 'object' ? p.social_links : {};
    const menu = safeUrl(p.menu_url || socials.menu_url || socials.menu);
    const maps = safeUrl(p.location_url || socials.location_url || socials.location || socials.maps);
    const insta = safeUrl(socials.instagram_url || socials.instagram);
    const fb = safeUrl(socials.facebook_url || socials.facebook);
    const web = safeUrl(socials.website_url || socials.website);
    const phone = String(p.phone || '').trim();
    const actions = [
      phone ? `<a href="tel:${esc(phone.replace(/[^+\d]/g,''))}">📞 CALL</a>` : '',
      maps ? `<a href="${esc(maps)}" target="_blank" rel="noopener">📍 LOCATION</a>` : '',
      menu ? `<a href="${esc(menu)}" target="_blank" rel="noopener">🍽️ MENU</a>` : '',
      insta ? `<a href="${esc(insta)}" target="_blank" rel="noopener">INSTAGRAM</a>` : '',
      fb ? `<a href="${esc(fb)}" target="_blank" rel="noopener">FACEBOOK</a>` : '',
      web ? `<a href="${esc(web)}" target="_blank" rel="noopener">WEBSITE</a>` : ''
    ].filter(Boolean).join('');
    const gallery = ads.length ? `<div class="wenik-detail-gallery">${ads.map(a=>`<img src="${esc(a.image_url)}" alt="${esc(a.title || p.business_name)}" loading="lazy">`).join('')}</div>` : '';
    const badge = discountLabel(p);
    detail.innerHTML = `
      <div class="wenik-detail-hero">${hero ? `<img src="${esc(hero)}" alt="${esc(p.business_name)}">` : '<div class="wenik-partner-placeholder">WENIK</div>'}</div>
      <div class="wenik-detail-name">${esc(p.business_name)}</div>
      <div class="wenik-detail-meta">${esc([p.category,p.area,p.address].filter(Boolean).join(' • '))}</div>
      ${(p.benefit_title || badge) ? `<div class="wenik-detail-promo"><strong>${esc(badge || 'WENIK OFFER')}</strong><div>${esc(p.benefit_title || '')}</div>${p.benefit_conditions ? `<div class="wenik-detail-meta" style="margin-top:5px">${esc(p.benefit_conditions)}</div>`:''}</div>` : ''}
      ${gallery}
      ${actions ? `<div class="wenik-detail-actions">${actions}</div>` : ''}`;
  };

  const closePartner = () => {
    $('wenikPartnerModal')?.classList.add('hidden');
    document.body.style.overflow='';
  };

  async function init() {
    if (loaded) return;
    if (typeof sb === 'undefined' || !$('homePartnerGrid')) return;
    loaded = true;
    try {
      const {data,error} = await sb.rpc('public_partner_directory_v2');
      if (error) throw error;
      directory = Array.isArray(data) ? data : [];
      populateArea();
      renderCategories();
      renderHome();
      setTimeout(renderPartnerTab, 250);
      if (!homeArea) {
        const tryAuto = () => {
          const app=$('app');
          if (app && !app.classList.contains('hidden')) useLocation(true);
          else setTimeout(tryAuto, 900);
        };
        setTimeout(tryAuto, 900);
      }
    } catch (e) {
      const grid=$('homePartnerGrid'); if(grid) grid.innerHTML='<div class="wenik-empty">Partners will appear here.</div>';
      console.warn('WENIK partner discovery:', e);
    }
  }

  $('btnUseLocation')?.addEventListener('click', () => useLocation(false));
  $('btnViewAllPartners')?.addEventListener('click', () => { $('navRewards')?.click(); setTimeout(renderPartnerTab,100); });
  $('wenikPartnerClose')?.addEventListener('click', closePartner);
  $('wenikPartnerModal')?.addEventListener('click', e => { if(e.target === $('wenikPartnerModal')) closePartner(); });
  document.addEventListener('keydown', e => { if(e.key==='Escape') closePartner(); });
  $('navRewards')?.addEventListener('click', () => setTimeout(renderPartnerTab,120));
  ['partnerCategory','partnerArea','partnerSearch'].forEach(id => {
    const el=$(id); if(el) el.addEventListener(id==='partnerSearch'?'input':'change', () => setTimeout(renderPartnerTab,50));
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true}); else init();
})();
</script>
'''

body_end = html.rfind('</body>')
html = html[:body_end] + js + '\n' + html[body_end:]

path.write_text(html, encoding='utf-8')
print('Applied WENIK Customer Home partner discovery upgrade to index.html')
