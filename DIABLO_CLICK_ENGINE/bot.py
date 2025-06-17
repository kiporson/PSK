#!/usr/bin/env python3
import os
import time
import requests
from scraper import scrape_proxies
from validator import validate_all
from banner import show_banner
from clicker import click_links

def check_resources():
    for filename in ['proxies_raw.txt', 'proxies_valid.txt', 'log.txt', 'useragents.txt']:
        open(filename, 'a').close()
    os.makedirs('links', exist_ok=True)

def remove_duplicate_proxies():
    seen = set()
    proxies = []
    with open("proxies_valid.txt") as f:
        for line in f:
            proxy = line.strip()
            if proxy and proxy not in seen:
                seen.add(proxy)
                proxies.append(proxy)
    with open("proxies_valid.txt", "w") as f:
        for proxy in proxies:
            f.write(proxy + '\n')
    print(f"✅ Duplikat dihapus. Total unik: {len(proxies)} proxy.")

def count_file_lines(path):
    try:
        with open(path) as f:
            return len([line for line in f if line.strip()])
    except FileNotFoundError:
        return 0

def input_links():
    print("🔗 Masukkan link shortlink satu per satu (DONE untuk selesai):")
    count = 1
    while True:
        try:
            link = input(f"Kirim link {count}: ").strip()
        except KeyboardInterrupt:
            print("\n⛔ Dibatalkan oleh pengguna.")
            break
        if link.upper() == 'DONE':
            break
        if link:
            domain = link.split('/')[2] if '://' in link else link.split('/')[0]
            path = os.path.join('links', f'{domain}.txt')
            with open(path, 'a') as f:
                f.write(link + '\n')
            count += 1
    print("✅ Link berhasil disimpan.")

def start_bot():
    all_links = []
    for file in os.listdir("links"):
        with open(os.path.join("links", file)) as f:
            all_links.extend([l.strip() for l in f if l.strip()])
    if all_links:
        print(f"🚀 Menjalankan bot pada {len(all_links)} link...")
        click_links(all_links)
    else:
        print("❌ Tidak ada link ditemukan di folder /links")

def show_summary():
    total_raw = count_file_lines('proxies_raw.txt')
    total_valid = count_file_lines('proxies_valid.txt')
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        ip = "Tidak terdeteksi"
    duration = 0
    show_banner(total_valid, total_raw, ip, duration)

def menu():
    check_resources()
    while True:
        print("\n┌────────────────────────────┐")
        print("│        🔧 PSK ENGINE        │")
        print("├────────────────────────────┤")
        print("│ 1. Scrape Proxy            │")
        print("│ 2. Cek Duplikat Proxy      │")
        print("│ 3. Validasi Proxy          │")
        print("│ 4. Masukkan Link Shortlink │")
        print("│ 5. Mulai Klik Bot          │")
        print("│ 6. Tampilkan Ringkasan     │")
        print("│ 0. Keluar                  │")
        print("└────────────────────────────┘")
        choice = input("Pilih menu: ").strip()
        
        if choice == '1':
            print("🔎 Scraping proxy...")
            scrape_proxies()
            print("✅ Scraping selesai.")
        elif choice == '2':
            remove_duplicate_proxies()
        elif choice == '3':
            print("🧪 Validasi proxy...")
            validate_all()
            print("✅ Validasi selesai.")
        elif choice == '4':
            input_links()
        elif choice == '5':
            start_bot()
        elif choice == '6':
            show_summary()
        elif choice == '0':
            print("👋 Keluar.")
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == '__main__':
    menu()