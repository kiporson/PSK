#!/usr/bin/env python3 import requests

✅ Validator Proxy untuk DIABLO_CLICK_ENGINE (Stabil & Responsif)

def validate_proxies() -> int: """Cek proxies dari proxies_raw.txt dan simpan yang aktif.""" try: with open('proxies_raw.txt') as f: raw_proxies = [p.strip() for p in f if p.strip()] except FileNotFoundError: print("❌ File proxies_raw.txt tidak ditemukan.") return 0

good = []
max_test = 100  # Batasi pengujian maksimal 100 proxy
print(f"🔍 Memulai validasi maksimal {min(len(raw_proxies), max_test)} proxy...\n")

for i, proxy in enumerate(raw_proxies):
    if i >= max_test:
        break
    proxies = {'http': proxy, 'https': proxy}
    try:
        print(f"🌐 Menguji: {proxy}")
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=3)
        if r.status_code == 200:
            print(f"✅ Aktif: {proxy}")
            good.append(proxy)
        else:
            print(f"⛔ Gagal ({r.status_code}): {proxy}")
    except Exception:
        print(f"⛔ Timeout/Error: {proxy}")
        continue

with open('proxies_valid.txt', 'w') as f:
    for p in good:
        f.write(p + '\n')

print(f"\n✅ Validasi selesai. Total proxy aktif: {len(good)}\n")
return len(good)

if name == "main": validate_proxies()

