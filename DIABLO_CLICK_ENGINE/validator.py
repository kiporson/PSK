#!/usr/bin/env python3 import time import concurrent.futures import undetected_chromedriver as uc from selenium.webdriver.chrome.options import Options from selenium.common.exceptions import WebDriverException from datetime import datetime import json import os

MAX_WORKERS = 10 TIMEOUT = 20 TEST_URL = "https://httpbin.org/ip" LOG_FILE = "validation_log.json"

CHROMEDRIVER_PATH = os.path.expanduser("~/.local/share/undetected_chromedriver/chromedriver")

Pastikan path valid atau berikan fallback

if not os.path.exists(CHROMEDRIVER_PATH): CHROMEDRIVER_PATH = None

def load_proxies(): try: with open("proxies_raw.txt") as f: return list(set(line.strip() for line in f if line.strip())) except FileNotFoundError: print("❌ File proxies_raw.txt tidak ditemukan.") return []

def log_result(proxy, status, reason=""): entry = { "proxy": proxy, "status": status, "timestamp": datetime.utcnow().isoformat(), "reason": reason } with open(LOG_FILE, "a") as logf: logf.write(json.dumps(entry) + "\n")

def test_proxy(proxy): options = uc.ChromeOptions() options.add_argument("--headless") options.add_argument("--no-sandbox") options.add_argument("--disable-gpu") options.add_argument(f"--proxy-server=http://{proxy}")

try:
    driver = uc.Chrome(options=options, use_subprocess=True, driver_executable_path=CHROMEDRIVER_PATH)
    driver.set_page_load_timeout(TIMEOUT)
    driver.get(TEST_URL)
    if "origin" in driver.page_source:
        log_result(proxy, "active")
        driver.quit()
        return proxy
    else:
        log_result(proxy, "invalid", "no origin in page")
        driver.quit()
        return None
except WebDriverException as e:
    log_result(proxy, "error", str(e))
    return None

def validate_proxies(): proxies = load_proxies() if not proxies: return 0

print(f"🔍 Memulai validasi expert mode ({len(proxies)} proxy) dengan {MAX_WORKERS} thread...\n")
start = time.time()
valid = []

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}
    for future in concurrent.futures.as_completed(futures):
        proxy = futures[future]
        try:
            result = future.result()
            if result:
                print(f"\033[92m✅ Aktif: {proxy}\033[0m")
                valid.append(proxy)
            else:
                print(f"\033[91m⛔ Gagal: {proxy}\033[0m")
        except Exception as e:
            print(f"\033[91m⛔ Exception: {proxy} - {e}\033[0m")
            log_result(proxy, "exception", str(e))

with open("proxies_valid.txt", "w") as f:
    for proxy in valid:
        f.write(proxy + "\n")

print(f"\n✅ Validasi selesai. Proxy aktif: {len(valid)} / {len(proxies)}")
print(f"⏱️ Durasi: {time.time() - start:.2f} detik\n")
return len(valid)

if name == "main": validate_proxies()

