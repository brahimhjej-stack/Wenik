// Match the web gallery: draw gifts and points rewards share one catalog.
export function mergeGiftCatalogs(...catalogs) {
  const merged = new Map();
  for (const raw of catalogs.flat()) {
    const gift = {
      ...raw,
      gift_title: raw.gift_title || raw.title || raw.name || raw.gift_name || raw.prize_name || 'WENIK Gift',
      partner_name: raw.partner_name || raw.business_name || raw.partner || '',
      gift_image_url: raw.image_url || raw.gift_image_url || raw.photo_url || raw.partner_logo_url || raw.image || '',
      remaining_quantity: raw.remaining_quantity ?? raw.remaining ?? raw.remaining_gifts ?? raw.stock_remaining ?? null,
    };
    const key = `${gift.gift_title}|${gift.partner_name}`.toLowerCase();
    const old = merged.get(key);
    merged.set(key, old ? {...old, ...gift, gift_image_url: gift.gift_image_url || old.gift_image_url, remaining_quantity: gift.remaining_quantity ?? old.remaining_quantity} : gift);
  }
  return [...merged.values()].filter(g => g.remaining_quantity === null || Number(g.remaining_quantity) > 0);
}
