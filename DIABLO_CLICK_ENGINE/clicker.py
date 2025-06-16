#!/usr/bin/env python3
import os
import random
import time
import requests
from stealth import get_headers

LOG_FILE = 'log.txt'

def load_proxies() -> list:
    """Muat proxy valid dari file."""
    if not os.path.exists('proxies_valid.txt'):
        return []
    with open('proxies_valid.txt') as f:
        return [p.strip() for p in f if p.strip()]

def load_useragents() -> list:
    """Muat daftar user-agent dari file."""
    if not os.path.exists('useragents.txt'):
        return []
    with open('useragents.txt') as f:
        return [ua.strip() for ua in f if ua.strip()]

def click_links(links: list) -> None:
    """Kunjungi tiap link menggunakan proxy dan user-agent acak."""
    proxies = load_proxies()
    user_agents = load_useragents()

    if not user_agents:
        print('❌ File useragents.txt kosong!')
        return
    if not links:
        print('❌ Tidak ada link untuk diklik!')
        return

    with open(LOG_FILE, 'a') as log:
        for i, url in enumerate(links, 1):
            proxy = random.choice(proxies) if proxies else None
            ua = random.choice(user_agents)
            headers = get_headers(ua)
            proxy_dict = {'http': proxy, 'https': proxy} if proxy else None

            print(f"🔗 [{i}/{len(links)}] Mengunjungi: {url}")
            print(f"🌐 Proxy: {proxy or 'Koneksi langsung'}")
            print(f"🧠 User-Agent: {ua[:70]}...")

            try:
                r = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10, allow_redirects=True)
                print(f"✅ Status: {r.status_code} | Redirect: {r.url}\n")
                log.write(f"{time.asctime()} SUCCESS {url} via {proxy} status:{r.status_code}\n")
            except Exception as e:
                print(f"⛔ Gagal via proxy: {e}")
                log.write(f"{time.asctime()} ERROR {url} via {proxy} reason:{e}\n")
                # 🔁 Coba ulang pakai koneksi langsung
                try:
                    print("🔁 Mencoba ulang tanpa proxy...")
                    r = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
                    print(f"✅ Status (direct): {r.status_code} | Redirect: {r.url}\n")
                    log.write(f"{time.asctime()} SUCCESS {url} via DIRECT status:{r.status_code}\n")
                except Exception as e2:
                    print(f"⛔ Tetap gagal tanpa proxy: {e2}\n")
                    log.write(f"{time.asctime()} ERROR {url} via DIRECT reason:{e2}\n")