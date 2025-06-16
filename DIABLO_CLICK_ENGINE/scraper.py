#!/usr/bin/env python3
import requests
import time

# Daftar sumber proxy HTTP publik
SOURCES = [
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all',
    'https://www.proxy-list.download/api/v1/get?type=http',
    'https://www.proxyscan.io/download?type=http',
    'https://spys.me/proxy.txt',
]

def scrape_proxies() -> None:
    """Scrape proxies dari berbagai sumber publik dan simpan ke proxies_raw.txt"""
    proxies = set()
    print("🌐 Mengambil proxy dari sumber publik...")

    for i, url in enumerate(SOURCES, start=1):
        print(f"🔗 [{i}/{len(SOURCES)}] Fetching: {url}")
        try:
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36"
            })
            if response.status_code == 200:
                for line in response.text.splitlines():
                    line = line.strip()
                    if ':' in line and len(line.split(':')) == 2:
                        proxies.add(line)
                print(f"✅ Berhasil ambil {len(proxies)} proxy sejauh ini.")
            else:
                print(f"⛔ Gagal (kode HTTP {response.status_code})")
        except Exception as e:
            print(f"⚠️ Gagal ambil dari {url}: {e}")
        time.sleep(1.5)  # Delay ringan biar gak dianggap spam

    with open('proxies_raw.txt', 'w') as f:
        for p in sorted(proxies):
            f.write(p + '\n')

    print(f"\n💾 Total proxy terkumpul: {len(proxies)}")