import { supabase } from './supabase';

let pending: Promise<{data: any[] | null; error: any}> | null = null;
let loadedAt = 0;
let loading = false;
// Read every page rather than silently dropping partners after the API row cap.
export function loadPartnerDirectory({force = false}: {force?: boolean} = {}) {
  if (pending && (loading || !force && Date.now() - loadedAt < 60000)) return pending;
  loading = true;
  pending = (async () => {
    try {
      const rows: any[] = [];
      for (let start = 0; ; start += 500) {
        const {data, error} = await supabase.rpc('public_partner_directory_v2')
          .order('business_name').order('partner_id').range(start, start + 499);
        if (error) throw error;
        rows.push(...(data || []));
        if ((data || []).length < 500) {
          loadedAt = Date.now();
          return {data: rows, error: null};
        }
      }
    } catch (error) {
      pending = null;
      return {data: null, error};
    } finally {
      loading = false;
    }
  })();
  return pending;
}
