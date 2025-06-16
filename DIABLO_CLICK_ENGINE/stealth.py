#!/usr/bin/env python3
# Generate extra HTTP headers to mimic real browser

def get_headers(user_agent: str) -> dict:
    """Return headers using the given user-agent."""
    return {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
