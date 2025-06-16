#!/usr/bin/env python3
import asyncio
import httpx
import time

TEST_URL = "https://httpbin.org/ip"
MAX_CONCURRENT = 200
TIMEOUT = 10

async def check_proxy(proxy: str, client: httpx.AsyncClient) -> str | None:
    try:
        proxies = {
            "http://": f"http://{proxy}",
            "https://": f"http://{proxy}",
        }
        resp = await client.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if resp.status_code == 200 and "origin" in resp.text:
            print(f"\033[92m✅ VALID: {proxy}\033[0m")
            return proxy
    except Exception:
        pass
    print(f"\033[91m⛔ INVALID: {proxy}\033[0m")
    return None

async def validate_all() -> int:
    try:
        with open("proxies_raw.txt") as f:
            raw_proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("❌ File proxies_raw.txt tidak ditemukan.")
        return 0

    connector = httpx.AsyncHTTPTransport(retries=1)
    async with httpx.AsyncClient(http2=False, transport=connector) as client:
        tasks = [check_proxy(proxy, client) for proxy in raw_proxies]
        results = await asyncio.gather(*tasks)

    valid = [r for r in results if r]
    with open("proxies_valid.txt", "w") as f:
        for p in valid:
            f.write(p + "\n")

    print(f"\n✅ Total proxy valid: {len(valid)} dari {len(raw_proxies)}")
    return len(valid)

def validate_proxies() -> int:
    start = time.time()
    valid_count = asyncio.run(validate_all())
    print(f"⏱️ Durasi validasi: {time.time() - start:.2f} detik")
    return valid_count