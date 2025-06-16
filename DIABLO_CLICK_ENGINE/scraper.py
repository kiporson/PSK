#!/usr/bin/env python3
import requests
import time
import re
from typing import List

# Daftar sumber proxy HTTP publik
SOURCES: List[str] = [
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all',
    'https://www.proxy-list.download/api/v1/get?type=http',
    'https://www.proxyscan.io/download?type=http',
    'https://spys.me/proxy.txt',
]

# Regex untuk mendeteksi format IP:PORT
PROXY_REGEX = re.compile(r'^\d{1,3}(\.\d{1,3}){3}:\d{2,5}$')

def scrape_proxies() -> None:
    """Scrape proxies dari berbagai sumber publik dan simpan ke proxies_raw.txt"""
    proxies = set()
    print("🌐 Mengambil proxy dari sumber publik...")

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36"
    }

    for i, url in enumerate(SOURCES, start=1):
        print(f"🔗 [{i}/{len(SOURCES)}] Fetching: {url}")
        try:
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()

            for line in response.text.splitlines():
                proxy = line.strip()
                if PROXY_REGEX.match(proxy):
                    proxies.add(proxy)
            print(f"✅ Total sementara: {len(proxies)} proxy valid.")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Gagal ambil dari {url}: {e}")

        time.sleep(1.0)  # Jeda ringan agar tidak terblokir

    with open('proxies_raw.txt', 'w') as f:
        for proxy in sorted(proxies):
            f.write(proxy + '\n')

    print(f"\n💾 Total proxy terkumpul: {len(proxies)}")