#!/usr/bin/env python3
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from fake_useragent import UserAgent

LOG_FILE = 'log.txt'

def load_proxies():
    if not os.path.exists('proxies_valid.txt'):
        return []
    with open('proxies_valid.txt') as f:
        return [x.strip() for x in f if x.strip()]

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
    proxies = load_proxies()
    ua = UserAgent()
    os.makedirs("screenshots", exist_ok=True)

    for i, url in enumerate(links, 1):
        print(f"🔗 [{i}/{len(links)}] Mengunjungi: {url}")
        proxy = random.choice(proxies) if proxies else None
        user_agent = ua.random

        print(f"🌐 Proxy: {proxy or 'None'}")
        print(f"🧠 User-Agent: {user_agent[:80]}...")

        driver = init_browser(proxy, user_agent)
        if not driver:
            continue

        try:
            driver.get(url)
            time.sleep(5)  # bisa disesuaikan jika loading lambat
            status = driver.execute_script("return document.readyState")
            if status != "complete":
                raise WebDriverException("Halaman tidak selesai dimuat")

            # Screenshot untuk debug (opsional)
            screenshot_path = f'screenshots/page_{i}.png'
            driver.save_screenshot(screenshot_path)

            print(f"✅ Berhasil akses halaman (Screenshot: {screenshot_path})")
            with open(LOG_FILE, 'a') as log:
                log.write(f"{time.asctime()} OK {url} via {proxy} [screenshot: {screenshot_path}]\n")

        except Exception as e:
            print(f"⛔ Gagal via proxy: {e}")
            with open(LOG_FILE, 'a') as log:
                log.write(f"{time.asctime()} ERROR {url} via {proxy} reason:{e}\n")
        finally:
            driver.quit()