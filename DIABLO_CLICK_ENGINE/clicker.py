#!/usr/bin/env python3
import os
import random
import time
import requests
from stealth import get_headers

LOG_FILE = 'log.txt'


def load_proxies() -> list:
    """Load validated proxies from file."""
    if not os.path.exists('proxies_valid.txt'):
        return []
    with open('proxies_valid.txt') as f:
        return [p.strip() for p in f if p.strip()]


def load_useragents() -> list:
    """Load user-agents from file."""
    with open('useragents.txt') as f:
        return [ua.strip() for ua in f if ua.strip()]


def click_links(links: list) -> None:
    """Request each link using random proxy and user-agent."""
    proxies = load_proxies()
    user_agents = load_useragents()
    if not user_agents:
        print('User-agent list empty.')
        return
    if not proxies:
        print('Tidak ada proxy valid, menggunakan koneksi langsung.')
    with open(LOG_FILE, 'a') as log:
        for url in links:
            proxy = random.choice(proxies) if proxies else None
            ua = random.choice(user_agents)
            headers = get_headers(ua)
            proxy_dict = {'http': proxy, 'https': proxy} if proxy else None
            try:
                r = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10, allow_redirects=True)
                log.write(f"{time.asctime()} SUCCESS {url} via {proxy} status:{r.status_code}\n")
            except Exception as e:
                log.write(f"{time.asctime()} ERROR {url} via {proxy} reason:{e}\n")


