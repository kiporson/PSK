import requests
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor

PROXY_FILE = "proxies.txt"
VALID_FILE = "valid_proxies.txt"
MAX_WORKERS = 20
TEST_URL = "http://icanhazip.com"

def validate_proxy(proxy):
    try:
        res = requests.get(TEST_URL, proxies={
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }, timeout=10)
        return res.status_code == 200 and len(res.text.strip()) > 5
    except:
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

    print(f"\n🔎 Memvalidasi {len(proxies)} proxy...")
    valid = []
    invalid_count = 0
    checked_count = 0
    start = time.time()
    lock = threading.Lock()

    def check(proxy):
        nonlocal invalid_count, checked_count
        if validate_proxy(proxy):
            with lock:
                valid.append(proxy)
        else:
            with lock:
                invalid_count += 1
        with lock:
            checked_count += 1

    def progress():
        while checked_count < len(proxies):
            with lock:
                print(f"\r⏳ Valid: {len(valid)} | Gagal: {invalid_count}", end='', flush=True)
            time.sleep(0.2)

    monitor = threading.Thread(target=progress)
    monitor.start()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(check, proxies)

    monitor.join()
    save_valid_proxies(valid)

    durasi = round(time.time() - start, 2)
    print(f"\r🎯 Selesai! ✅ {len(valid)} valid | ❌ {invalid_count} gagal | ⏱️ {durasi}s\n")

if __name__ == "__main__":
    print("🚀 VALIDATOR MODE: TENANG & CEPAT")
    validate_all()