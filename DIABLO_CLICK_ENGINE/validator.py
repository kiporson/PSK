#!/usr/bin/env python3
import os
import asyncio
import httpx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Validate proxies scraped to ensure they are usable

async def _check(session: httpx.AsyncClient, proxy: str) -> str | None:
    """Return proxy if reachable."""
    try:
        r = await session.get("http://httpbin.org/ip", proxies=f"http://{proxy}", timeout=5)
        if r.status_code == 200:
            return proxy
    except Exception:
        return None


def validate_proxies(concurrency: int = 20) -> int:
    """Check proxies from proxies_raw.txt asynchronously and save working ones."""
    try:
        with open(os.path.join(BASE_DIR, "proxies_raw.txt")) as f:
            raw_proxies = [p.strip() for p in f if p.strip()]
    except FileNotFoundError:
        return 0

    async def run() -> list[str]:
        good: list[str] = []
        sem = asyncio.Semaphore(concurrency)
        async with httpx.AsyncClient() as session:
            async def worker(proxy: str) -> None:
                async with sem:
                    res = await _check(session, proxy)
                    if res:
                        good.append(res)

            tasks = [worker(p) for p in raw_proxies]
            await asyncio.gather(*tasks)
        return good

    good = asyncio.run(run())

    with open(os.path.join(BASE_DIR, "proxies_valid.txt"), "w") as f:
        for p in good:
            f.write(p + "\n")
    return len(good)

