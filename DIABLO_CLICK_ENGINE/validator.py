#!/usr/bin/env python3 from selenium import webdriver from selenium.webdriver.chrome.options import Options from selenium.common.exceptions import WebDriverException import concurrent.futures import time

MAX_WORKERS = 20 TIMEOUT = 15  # Detik TEST_URL = "https://httpbin.org/ip"

def load_proxies(): try: with open('proxies_raw.txt') as f: return list(set(line.strip() for line in f if line.strip())) except FileNotFoundError: print("❌ File proxies_raw.txt tidak ditemukan.") return []

def test_proxy(proxy): chrome_options = Options() chrome_options.add_argument('--headless') chrome_options.add_argument('--disable-gpu') chrome_options.add_argument('--no-sandbox') chrome_options.add_argument(f'--proxy-server=http://{proxy}')

try:
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(TIMEOUT)
    driver.get(TEST_URL)
    page = driver.page_source
    driver.quit()
    return proxy if "origin" in page else None
except WebDriverException:
    return None

def validate_proxies(): proxies = load_proxies() if not proxies: return 0

print(f"🔍 Memulai validasi turbo dengan Selenium ({len(proxies)} proxy) menggunakan {MAX_WORKERS} thread...\n")
start = time.time()
valid = []

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        proxy = futures[future]
        if result:
            print(f"\033[92m✅ Aktif: {proxy}\033[0m")
            valid.append(proxy)
        else:
            print(f"\033[91m⛔ Gagal: {proxy}\033[0m")

with open('proxies_valid.txt', 'w') as f:
    for proxy in valid:
        f.write(proxy + '\n')

print(f"\n✅ Validasi selesai. Total proxy aktif: {len(valid)} / {len(proxies)}")
print(f"⏱️ Durasi: {time.time() - start:.2f} detik\n")
return len(valid)

if name == "main": validate_proxies()

