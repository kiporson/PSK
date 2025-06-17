#!/usr/bin/env python3
import os
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from fake_useragent import UserAgent

LOG_FILE = 'log.txt'
USAGE_FILE = 'proxy_usage.json'
PROXY_FILE = 'proxies_valid.txt'

def load_useragents():
    if not os.path.exists('useragents.txt'):
        return ['Mozilla/5.0 (Linux) Gecko/20100101 Firefox/89.0']
    with open('useragents.txt') as f:
        return [x.strip() for x in f if x.strip()]

def count_file_lines(path):
    try:
        with open(path) as f:
            return len([line for line in f if line.strip()])
    except:
        return 0

def save_proxy_usage(usage_dict):
    with open(USAGE_FILE, "w") as f:
        json.dump(usage_dict, f, indent=2)

def load_proxies_batch(size=1000):
    if not os.path.exists(PROXY_FILE):
        return [], {}

    with open(PROXY_FILE) as f:
        proxies = [line.strip() for line in f if line.strip()]

    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE) as f:
            usage = json.load(f)
    else:
        usage = {}

    proxies.sort(key=lambda p: usage.get(p, 0))  # prioritas yang fresh
    return proxies[:size], usage

def check_and_reload_proxies_if_needed(threshold=100):
    proxies_left = count_file_lines(PROXY_FILE)
    if proxies_left < threshold:
        print("🔄 Proxy kurang dari 100! Scraping + Validasi...")
        from scraper import scrape_proxies
        from validator import validate_all
        scrape_proxies()
        validate_all()

def init_browser(proxy=None, user_agent=None):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if user_agent:
        options.add_argument(f"user-agent={user_agent}")
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"❌ Gagal inisialisasi Chrome: {e}")
        return None
    return driver

def click_links(links: list):
    user_agents = load_useragents()
    proxies, usage = load_proxies_batch()
    os.makedirs("screenshots", exist_ok=True)

    for i, url in enumerate(links, 1):
        if not proxies:
            print("⚠️ Proxy batch habis, ambil batch baru...")
            check_and_reload_proxies_if_needed()
            proxies, usage = load_proxies_batch()

        proxy = proxies.pop(0)
        usage[proxy] = usage.get(proxy, 0) + 1
        user_agent = random.choice(user_agents)

        print(f"\n🔗 [{i}/{len(links)}] Mengunjungi: {url}")
        print(f"🌐 Proxy: {proxy}")
        print(f"🧠 User-Agent: {user_agent[:70]}...")

        driver = init_browser(proxy, user_agent)
        if not driver:
            continue

        try:
            driver.get(url)
            time.sleep(5)
            status = driver.execute_script("return document.readyState")
            if status != "complete":
                raise WebDriverException("Halaman tidak selesai dimuat")

            screenshot_path = f'screenshots/page_{i}.png'
            driver.save_screenshot(screenshot_path)

            print(f"✅ BERHASIL (Screenshot: {screenshot_path})")
            with open(LOG_FILE, 'a') as log:
                log.write(f"{time.asctime()} OK {url} via {proxy} [ss: {screenshot_path}]\n")
        except Exception as e:
            print(f"⛔ Gagal via proxy: {e}")
            with open(LOG_FILE, 'a') as log:
                log.write(f"{time.asctime()} ERROR {url} via {proxy} reason:{e}\n")
        finally:
            driver.quit()

        save_proxy_usage(usage)