#!/usr/bin/env python3
import requests

# List of proxy sources providing plain text IP:PORT per line
SOURCES = [
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all'
]


def scrape_proxies() -> None:
    """Scrape proxies from public sources and save to proxies_raw.txt."""
    proxies = set()
    for url in SOURCES:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                for line in resp.text.splitlines():
                    line = line.strip()
                    if line and ':' in line:
                        proxies.add(line)
        except Exception:
            pass
    with open('proxies_raw.txt', 'w') as f:
        for p in sorted(proxies):
            f.write(p + '\n')
    return None

