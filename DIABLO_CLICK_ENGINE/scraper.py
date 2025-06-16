#!/usr/bin/env python3
import os
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# List of proxy sources providing plain text IP:PORT per line
SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"
]


def scrape_proxies() -> None:
    """Scrape proxies from public sources and save to proxies_raw.txt."""
    proxies = set()
    headers = {"User-Agent": "Mozilla/5.0"}
    for url in SOURCES:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.ok:
                for line in resp.text.splitlines():
                    line = line.strip()
                    if line and ':' in line:
                        proxies.add(line)
        except Exception:
            continue
    with open(os.path.join(BASE_DIR, "proxies_raw.txt"), "w") as f:
        for p in sorted(proxies):
            f.write(p + "\n")

