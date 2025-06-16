#!/usr/bin/env python3
import os
import random
import time
import requests
from stealth import get_headers

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, 'log.txt')


def load_proxies() -> list:
    """Load validated proxies from file."""
    if not os.path.exists(os.path.join(BASE_DIR, 'proxies_valid.txt')):
        return []
    with open(os.path.join(BASE_DIR, 'proxies_valid.txt')) as f:
        return [p.strip() for p in f if p.strip()]


def load_useragents() -> list:
    """Load user-agents from file."""
    with open(os.path.join(BASE_DIR, 'useragents.txt')) as f:
        return [ua.strip() for ua in f if ua.strip()]


def load_links() -> list:
    """Gather all shortlinks from files inside the links directory."""
    urls = []
    if not os.path.isdir(os.path.join(BASE_DIR, 'links')):
        return urls
    for fname in os.listdir(os.path.join(BASE_DIR, 'links')):
        path = os.path.join(BASE_DIR, 'links', fname)
        if os.path.isfile(path):
            with open(path) as f:
                for line in f:
                    link = line.strip()
                    if link:
                        urls.append(link)
    return urls


def click_links(links: list | None = None) -> None:
    """Request each link using random proxy and user-agent."""
    if links is None:
        links = load_links()
    proxies = load_proxies()
    user_agents = load_useragents()
    if not user_agents:
        print('User-agent list empty.')
        return
    if not proxies:
        print('Tidak ada proxy valid, menggunakan koneksi langsung.')
    if not links:
        print('\u274c Tidak ada shortlink ditemukan!')
        return
    with open(LOG_FILE, 'a') as log:
        for url in links:
            proxy = random.choice(proxies) if proxies else None
            ua = random.choice(user_agents)
            headers = get_headers(ua)
            proxy_dict = {'http': proxy, 'https': proxy} if proxy else None
            try:
                r = requests.get(
                    url,
                    headers=headers,
                    proxies=proxy_dict,
                    timeout=10,
                    allow_redirects=True,
                )
                log.write(
                    f"{time.asctime()} SUCCESS {url} via {proxy} status:{r.status_code}\n"
                )
            except Exception as e:
                log.write(
                    f"{time.asctime()} ERROR {url} via {proxy} reason:{e}\n"
                )


