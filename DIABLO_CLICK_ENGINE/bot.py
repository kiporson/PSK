#!/usr/bin/env python3 import os import time import requests from scraper import scrape_proxies from validator import validate_proxies from banner import show_banner from clicker import click_links

def check_resources() -> None: """Pastikan semua file dan folder penting tersedia.""" for filename in ['proxies_raw.txt', 'proxies_valid.txt', 'log.txt', 'useragents.txt']: open(filename, 'a').close() os.makedirs('links', exist_ok=True)

def main(): check_resources() start = time.time()

print("🔎 Mulai scraping proxy...")
scrape_proxies()

# Hitung jumlah hasil scraping
try:
    with open('proxies_raw.txt') as f:
        total = len([x for x in f if x.strip()])
except FileNotFoundError:
    total = 0

print("🧪 Mulai validasi proxy...")
valid = validate_proxies()
duration = time.time() - start

# Ambil IP publik
try:
    ip = requests.get('https://api.ipify.org', timeout=5).text.strip()
except Exception:
    ip = 'Tidak terdeteksi'

show_banner(valid, total, ip, duration)

if valid == 0:
    print('\033[91m⚠️ WARNING: Semua proxy gagal! Akan menggunakan koneksi langsung jika dipaksa.\033[0m')

# Input shortlink
links = []
count = 1
print("🔗 Masukkan link shortlink satu per satu (ketik DONE jika selesai):")
while True:
    try:
        link = input(f'Kirim link {count}: ').strip()
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
        links.append(link)
        count += 1

# Proses klik
if links:
    print(f"\n🚀 Menjalankan klik otomatis pada {len(links)} link...")
    click_links(links)
else:
    print('\u274c Tidak ada shortlink ditemukan!')

if name == 'main': main()

