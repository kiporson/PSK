#!/usr/bin/env python3
import requests

# Validate proxies scraped to ensure they are usable

def validate_proxies() -> int:
    """Check proxies from proxies_raw.txt and save working ones."""
    try:
        with open('proxies_raw.txt') as f:
            raw_proxies = [p.strip() for p in f if p.strip()]
    except FileNotFoundError:
        return 0
    good = []
    for proxy in raw_proxies:
        proxies = {'http': proxy, 'https': proxy}
        try:
            r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
            if r.status_code == 200:
                good.append(proxy)
        except Exception:
            pass
    with open('proxies_valid.txt', 'w') as f:
        for p in good:
            f.write(p + '\n')
    return len(good)

