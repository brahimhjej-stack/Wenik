"""Read-only load test against the isolated WENIK readiness project only."""
import argparse
import concurrent.futures
import json
import statistics
import time
import urllib.request

TEST_URL = 'https://ccvrfxyshagmtcwqqsoi.supabase.co/rest/v1/rpc/public_partner_directory_v2'
TEST_PUBLIC_KEY = 'sb_publishable_yTxPBxIUcssJbmNoYXvEoA_a8YenEsE'


def request_one(_):
    started = time.monotonic()
    request = urllib.request.Request(TEST_URL, data=b'{}', headers={
        'apikey': TEST_PUBLIC_KEY, 'Content-Type': 'application/json',
        'User-Agent': 'WENIK-Isolated-Load-Test/1.0',
    })
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            rows = json.load(response)
            return response.status, time.monotonic() - started, len(rows)
    except Exception as error:
        return type(error).__name__, time.monotonic() - started, 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--requests', type=int, default=1000)
    parser.add_argument('--concurrency', type=int, default=25)
    args = parser.parse_args()
    if not 1 <= args.requests <= 10000 or not 1 <= args.concurrency <= 100:
        parser.error('requests must be 1..10000 and concurrency 1..100')
    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        results = list(pool.map(request_one, range(args.requests)))
    times = sorted(result[1] for result in results)
    failures = [result for result in results if result[0] != 200]
    print(json.dumps({
        'requests': len(results), 'concurrency': args.concurrency,
        'success': len(results) - len(failures),
        'errors': sorted({str(result[0]) for result in failures}),
        'seconds': round(time.monotonic() - started, 2),
        'p50_ms': round(statistics.median(times) * 1000),
        'p95_ms': round(times[max(0, int(len(times) * .95) - 1)] * 1000),
        'returned_rows': sorted({result[2] for result in results}),
    }, indent=2))
    raise SystemExit(1 if failures else 0)
