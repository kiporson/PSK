import requests
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor

PROXY_FILE = "proxies.txt"
VALID_FILE = "valid_proxies.txt"
MAX_WORKERS = 20
MAX_VALID = 1000
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

def validate_all(max_valid=MAX_VALID):
    proxies = load_proxies()
    if not proxies:
        print("⚠️ Tidak ada proxy untuk divalidasi.")
        return

    print(f"\n🔎 Memvalidasi hingga {max_valid} proxy valid dari {len(proxies)} total...")

    valid = []
    invalid_count = 0
    checked_count = 0
    lock = threading.Lock()
    start = time.time()

    def check(proxy):
        nonlocal checked_count, invalid_count
        # Cegah validasi berlebihan
        if len(valid) >= max_valid:
            return
        if validate_proxy(proxy):
            with lock:
                if len(valid) < max_valid:
                    valid.append(proxy)
        else:
            with lock:
                invalid_count += 1
        with lock:
            checked_count += 1

    def progress():
        while checked_count < len(proxies) and len(valid) < max_valid:
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
    print(f"\r🎯 Validasi selesai! ✅ {len(valid)} valid | ❌ {invalid_count} gagal | ⏱️ {durasi}s\n")

if __name__ == "__main__":
    print("🚀 VALIDATOR MODE: OTOMATIS MAX 1000 VALID")
    validate_all()