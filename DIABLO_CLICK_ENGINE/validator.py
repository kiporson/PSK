#!/usr/bin/env python3
import requests
import concurrent.futures
import time

MAX_WORKERS = 50  # Thread paralel
TIMEOUT = 5       # Timeout per request

def load_proxies():
    try:
        with open('proxies_raw.txt') as f:
            return list(set(line.strip() for line in f if line.strip()))
    except FileNotFoundError:
        print("❌ File proxies_raw.txt tidak ditemukan.")
        return []

def test_proxy(proxy):
    proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    try:
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=TIMEOUT)
        if r.status_code == 200:
            return proxy
    except:
        return None

def validate_proxies():
    proxies = load_proxies()
    if not proxies:
        return 0

    print(f"🔍 Memulai validasi turbo ({len(proxies)} proxy) dengan {MAX_WORKERS} thread...\n")
    start = time.time()
    valid = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(test_proxy, p): p for p in proxies}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(f"\033[92m✅ Aktif: {result}\033[0m")
                valid.append(result)
            else:
                print(f"\033[91m⛔ Gagal: {futures[future]}\033[0m")

    with open('proxies_valid.txt', 'w') as f:
        for proxy in valid:
            f.write(proxy + '\n')

    print(f"\n✅ Validasi selesai. Total proxy aktif: {len(valid)} / {len(proxies)}")
    print(f"⏱️ Durasi: {time.time() - start:.2f} detik\n")
    return len(valid)

if __name__ == "__main__":
    validate_proxies()