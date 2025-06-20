import requests
import random
import time
import os
from concurrent.futures import ThreadPoolExecutor

PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://proxyspace.pro/http.txt",
    "https://multiproxy.org/txt_all/proxy.txt"
]

PROXY_FILE = "proxies.txt"
VALID_FILE = "valid_proxies.txt"
SCRAPE_INTERVAL_MINUTES = 30

def scrape_proxies():
    proxies = set()
    for url in PROXY_SOURCES:
        try:
            print(f"🌐 Mengambil dari: {url}")
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            for line in res.text.strip().splitlines():
                if ":" in line:
                    proxies.add(line.strip())
        except Exception as e:
            print(f"⚠️ Gagal fetch dari {url} => {e}")
    with open(PROXY_FILE, "w") as f:
        for p in proxies:
            f.write(p + "\n")
    print(f"✅ Total proxy diambil: {len(proxies)}")

def validate_proxy(proxy):
    test_url = "http://www.google.com/generate_204"
    try:
        res = requests.get(test_url, proxies={
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }, timeout=7)
        return res.status_code in [200, 204]
    except:
        return False

def validate_all():
    if not os.path.exists(PROXY_FILE):
        print("📂 Proxy file tidak ditemukan. Scraping dulu...")
        scrape_proxies()

    with open(PROXY_FILE) as f:
        proxies = [line.strip() for line in f if line.strip()]

    valid = []
    print(f"🔎 Validasi {len(proxies)} proxy...")
    start = time.time()

    def check(proxy):
        if validate_proxy(proxy):
            print(f"✅ VALID: {proxy}")
            valid.append(proxy)
        else:
            print(f"⛔ INVALID: {proxy}")

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check, proxies)

    with open(VALID_FILE, "w") as f:
        for p in valid:
            f.write(p + "\n")

    durasi = round(time.time() - start, 2)
    print(f"\n🎯 Total valid: {len(valid)} dari {len(proxies)}")
    print(f"⏱️ Durasi validasi: {durasi} detik")

    if not valid:
        print("⚠️ Proxy valid = 0! 🔁 Scraping ulang...")
        time.sleep(3)
        scrape_proxies()
        return validate_all()

    return valid

def get_random_proxy():
    if os.path.exists(VALID_FILE):
        with open(VALID_FILE) as f:
            proxies = [line.strip() for line in f if line.strip()]
        if proxies:
            return random.choice(proxies)
    return None

def get_stealth_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                      "AppleWebKit/537.36 (KHTML, like Gecko) " +
                      "Chrome/114.0.0.0 Safari/537.36"
    }

def stealth_request(url):
    print(f"👣 STEALTH MODE: Akses langsung {url}")
    try:
        res = requests.get(url, headers=get_stealth_headers(), timeout=15)
        return res.text
    except Exception as e:
        print(f"💥 Gagal stealth request: {e}")
        return None

# LOOP scraping setiap 30 menit (optional)
def continuous_scraping_loop():
    while True:
        print("\n🔄 LOOP SCRAPER JALAN...")
        scrape_proxies()
        validate_all()
        print(f"🛌 Tidur {SCRAPE_INTERVAL_MINUTES} menit...")
        time.sleep(SCRAPE_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    print("🚀 SCRAPER MODE TURBO AKTIF...")
    scrape_proxies()
    validate_all()
    # Uncomment di bawah untuk loop nonstop:
    # continuous_scraping_loop()