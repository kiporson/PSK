#!/usr/bin/env python3
import requests

# ✅ Validate proxies scraped to ensure they are usable
def validate_proxies() -> int:
    """Check proxies from proxies_raw.txt and save working ones."""
    try:
        with open('proxies_raw.txt') as f:
            raw_proxies = [p.strip() for p in f if p.strip()]
    except FileNotFoundError:
        print("❌ File proxies_raw.txt tidak ditemukan.")
        return 0

    good = []
    max_test = 200  # Batasi jumlah proxy yang dites agar tidak lama
    print(f"🔍 Validasi maksimal {min(len(raw_proxies), max_test)} proxy...\n")

    for i, proxy in enumerate(raw_proxies):
        if i >= max_test:
            break
        proxies = {'http': proxy, 'https': proxy}
        try:
            print(f"🌐 Testing: {proxy}")
            r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=3)
            if r.status_code == 200:
                print(f"✅ OK: {proxy}")
                good.append(proxy)
        except Exception:
            print(f"⛔ Gagal: {proxy}")
            continue

    with open('proxies_valid.txt', 'w') as f:
        for p in good:
            f.write(p + '\n')

    print(f"\n✅ Selesai. Total proxy valid: {len(good)}\n")
    return len(good)