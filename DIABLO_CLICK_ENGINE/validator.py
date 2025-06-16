import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor

PROXY_FILE = "proxies.txt"
VALID_FILE = "valid_proxies.txt"
MAX_WORKERS = 20  # biar gak dibanned endpoint

TEST_URL = "http://icanhazip.com"

def validate_proxy(proxy):
    try:
        res = requests.get(TEST_URL, proxies={
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }, timeout=10)
        if res.status_code == 200 and len(res.text.strip()) > 5:
            return True
        else:
            print(f"⚠️ BAD RESPONSE [{res.status_code}] from {proxy}")
    except Exception as e:
        print(f"🛑 ERROR {proxy} ➤ {e}")
    return False

def load_proxies():
    if not os.path.exists(PROXY_FILE):
        print("❌ File proxies.txt tidak ditemukan!")
        return []
    with open(PROXY_FILE) as f:
        return [line.strip() for line in f if line.strip()]

def save_valid_proxies(valid_list):
    with open(VALID_FILE, "w") as f:
        for proxy in valid_list:
            f.write(proxy + "\n")

def validate_all():
    proxies = load_proxies()
    if not proxies:
        print("⚠️ Tidak ada proxy untuk divalidasi.")
        return

    print(f"\n🔎 Validasi {len(proxies)} proxy...")
    valid = []
    start = time.time()

    def check(proxy):
        if validate_proxy(proxy):
            print(f"✅ VALID: {proxy}")
            valid.append(proxy)
        else:
            print(f"⛔ INVALID: {proxy}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(check, proxies)

    save_valid_proxies(valid)
    durasi = round(time.time() - start, 2)
    print(f"\n🎯 Total valid: {len(valid)} dari {len(proxies)}")
    print(f"⏱️ Durasi: {durasi} detik")

    if len(valid) == 0:
        print("\n🚨 SEMUA PROXY GAGAL TOTAL!")
        print("💡 Coba scraping ulang atau ganti endpoint.")

if __name__ == "__main__":
    print("🚀 VALIDATOR MODE: ANTI-ZONK AKTIF...")
    validate_all()