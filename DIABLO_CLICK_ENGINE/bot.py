#!/usr/bin/env python3
import os
import time
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from scraper import scrape_proxies
from validator import validate_proxies
from banner import show_banner
from clicker import click_links


def check_resources() -> None:
    """Ensure required files and folders exist."""
    open(os.path.join(BASE_DIR, 'proxies_raw.txt'), 'a').close()
    open(os.path.join(BASE_DIR, 'proxies_valid.txt'), 'a').close()
    open(os.path.join(BASE_DIR, 'log.txt'), 'a').close()
    open(os.path.join(BASE_DIR, 'useragents.txt'), 'a').close()
    os.makedirs(os.path.join(BASE_DIR, 'links'), exist_ok=True)


def main():
    check_resources()
    start = time.time()
    scrape_proxies()
    # count scraped proxies
    with open(os.path.join(BASE_DIR, 'proxies_raw.txt')) as f:
        total = len([x for x in f if x.strip()])
    valid = validate_proxies()
    duration = time.time() - start
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text.strip()
    except Exception:
        ip = 'unknown'

    show_banner(valid, total, ip, duration)

    if valid == 0:
        print('\033[91mWARNING: semua proxy gagal, menggunakan koneksi langsung.\033[0m')

    # accept shortlink input one by one
    count = 1
    added = False
    while True:
        link = input(f'Kirim link {count}: ').strip()
        if link.upper() == 'DONE':
            break
        if link:
            domain = link.split('/')[2] if '://' in link else link.split('/')[0]
            path = os.path.join(BASE_DIR, 'links', f'{domain}.txt')
            with open(path, 'a') as f:
                f.write(link + '\n')
            count += 1
            added = True

    if added:
        click_links()
    else:
        print('\u274c Tidak ada shortlink ditemukan!')


if __name__ == '__main__':
    main()

