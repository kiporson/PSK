def click_links(links: list) -> None:
    """Request each link using random proxy and user-agent, with real-time output."""
    proxies = load_proxies()
    user_agents = load_useragents()

    if not user_agents:
        print('⚠️  Daftar User-Agent kosong.')
        return
    if not proxies:
        print('⚠️  Tidak ada proxy valid, menggunakan koneksi langsung.\n')

    with open(LOG_FILE, 'a') as log:
        for i, url in enumerate(links, 1):
            proxy = random.choice(proxies) if proxies else None
            ua = random.choice(user_agents)
            headers = get_headers(ua)
            proxy_dict = {'http': proxy, 'https': proxy} if proxy else None

            print(f"🔗 [{i}/{len(links)}] Mengunjungi: {url}")
            if proxy:
                print(f"🌐 Proxy: {proxy}")
            print(f"🧠 User-Agent: {ua[:60]}...")

            try:
                r = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10, allow_redirects=True)
                print(f"✅ Status: {r.status_code} | Redirect: {r.url}\n")
                log.write(f"{time.asctime()} SUCCESS {url} via {proxy} status:{r.status_code}\n")
            except Exception as e:
                print(f"⛔ Gagal: {e}\n")
                log.write(f"{time.asctime()} ERROR {url} via {proxy} reason:{e}\n")

            time.sleep(random.uniform(2, 5))  # Jeda 2–5 detik biar aman