import { AppState, Platform } from 'react-native';
import 'react-native-url-polyfill/auto';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createClient, processLock } from '@supabase/supabase-js';

// Public client configuration. Supabase publishable keys are designed to be
// embedded in web/mobile clients; authorization is still enforced by Auth + RLS.
const url = process.env.EXPO_PUBLIC_SUPABASE_URL || 'https://zkrnzwnbdoaqanqzznlw.supabase.co';
const key = process.env.EXPO_PUBLIC_SUPABASE_PUBLISHABLE_KEY || 'sb_publishable_Q8pOXn-3YAUo_6OX6c2bKg_mLKH8O0k';

export const supabase = createClient(url, key, {
  auth: {
    ...(Platform.OS !== 'web' ? { storage: AsyncStorage } : {}),
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
    lock: processLock,
  },
});

if (Platform.OS !== 'web') {
  AppState.addEventListener('change', state => {
    if (state === 'active') supabase.auth.startAutoRefresh();
    else supabase.auth.stopAutoRefresh();
  });
}
