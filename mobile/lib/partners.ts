import { supabase } from './supabase';

let pending: Promise<{data: any[] | null; error: any}> | null = null;
let loadedAt = 0;
// Read every page rather than silently dropping partners after the API row cap.
export function loadPartnerDirectory() {
  if (pending && Date.now() - loadedAt < 60000) return pending;
  loadedAt = Date.now();
  pending = (async () => {
    try {
      const rows: any[] = [];
      for (let start = 0; ; start += 500) {
        const {data, error} = await supabase.rpc('public_partner_directory_v2')
          .order('business_name').order('partner_id').range(start, start + 499);
        if (error) throw error;
        rows.push(...(data || []));
        if ((data || []).length < 500) return {data: rows, error: null};
      }
    } catch (error) {
      pending = null;
      return {data: null, error};
    }
  })();
  return pending;
}
