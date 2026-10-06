"""Read-only production availability check; creates no accounts or transactions."""
import concurrent.futures
import json
import sys
import time
import urllib.request

PUBLIC_KEY = 'sb_publishable_Q8pOXn-3YAUo_6OX6c2bKg_mLKH8O0k'

def check(name, url, payload=None):
    started = time.monotonic()
    headers = {'User-Agent': 'WENIK-Availability-Check/1.0'}
    if payload is not None:
        headers.update({'apikey': PUBLIC_KEY, 'Content-Type': 'application/json'})
    request = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode('utf-8')
            valid = isinstance(json.loads(body), list) if payload is not None else 'WELCOME TO WENIK' in body and 'meContactUs' in body
            return {'check': name, 'ok': response.status == 200 and valid, 'status': response.status, 'elapsed_ms': round((time.monotonic()-started)*1000)}
    except Exception as error:
        return {'check': name, 'ok': False, 'error': type(error).__name__}

if __name__ == '__main__':
    targets = [('website', 'https://wenik.co/', None), ('partner_api', 'https://zkrnzwnbdoaqanqzznlw.supabase.co/rest/v1/rpc/public_partner_directory_v2', b'{}')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda args: check(*args), targets))
    print(json.dumps({'results': results}, indent=2))
    sys.exit(0 if all(result['ok'] for result in results) else 1)
