#!/usr/bin/env python3
import os
import time
import json
import random
import requests

LOG_FILE = 'log.txt'
USAGE_FILE = 'proxy_usage.json'
PROXY_FILE = 'proxies_valid.txt'

def load_useragents():
    if not os.path.exists('useragents.txt'):
        return ['Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/89.0']
    with open('useragents.txt') as f:
        return [x.strip() for x in f if x.strip()]

def count_file_lines(path):
    try:
        with open(path) as f:
            return len([line for line in f if line.strip()])
    except:
        return 0

def save_proxy_usage(usage_dict):
    with open(USAGE_FILE, "w") as f:
        json.dump(usage_dict, f, indent=2)

def load_proxies_batch(size=1000, max_usage=1):
    if not os.path.exists(PROXY_FILE):
        return [], {}

    with open(PROXY_FILE) as f:
        proxies = [line.strip() for line in f if line.strip()]

    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE) as f:
            usage = json.load(f)
    else:
        usage = {}

    # Hanya ambil proxy yang belum dipakai lebih dari max_usage
    proxies = [p for p in proxies if usage.get(p, 0) < max_usage]
    proxies.sort(key=lambda p: usage.get(p, 0))
    return proxies[:size], usage

def check_and_reload_proxies_if_needed(threshold=100):
    proxies_left = count_file_lines(PROXY_FILE)
    if proxies_left < threshold:
        print("🔄 Proxy kurang dari 100! Auto scrape + validasi...")
        from scraper import scrape_proxies
        from validator import validate_all
        scrape_proxies()
        validate_all()

def click_links(links: list):
    user_agents = load_useragents()
    proxies, usage = load_proxies_batch()
    
    for i, url in enumerate(links, 1):
        if not proxies:
            check_and_reload_proxies_if_needed()
            proxies, usage = load_proxies_batch()

        proxy = proxies.pop(0)
        usage[proxy] = usage.get(proxy, 0) + 1
        user_agent = random.choice(user_agents)

        print(f"\n🔗 [{i}/{len(links)}] Mengunjungi: {url}")
        print(f"🌐 Proxy: {proxy}")
        print(f"🧠 User-Agent: {user_agent[:70]}...")

        headers = {
            "User-Agent": user_agent,
            "Referer": "https://google.com",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
            "DNT": "1"
        }

        try:
            proxies_dict = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }

            resp = requests.get(url, headers=headers, proxies=proxies_dict,
                                timeout=10, allow_redirects=True)

            final_url = resp.url
            print(f"✅ Redirect selesai ke: {final_url}")
            with open(LOG_FILE, 'a') as log:
                log.write(f"{time.asctime()} OK {url} -> {final_url} via {proxy}\n")

        except Exception as e:
            print(f"⛔ ERROR: {e}")
            with open(LOG_FILE, 'a') as log:
                log.write(f"{time.asctime()} ERROR {url} via {proxy} reason:{e}\n")

        save_proxy_usage(usage)
        time.sleep(3)  # delay antarklik