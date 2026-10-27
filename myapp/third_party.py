import requests
import time
import logging

logger = logging.getLogger('myapp.third_party')

FALLBACK_QUOTES = [
    {
        "quote": "First, solve the problem. Then, write the code.",
        "author": "John Johnson",
        "category": "Software Engineering"
    },
    {
        "quote": "Simplicity is prerequisite for reliability.",
        "author": "Edsger W. Dijkstra",
        "category": "System Design"
    },
    {
        "quote": "Code is like humor. When you have to explain it, it’s bad.",
        "author": "Cory House",
        "category": "Clean Code"
    },
    {
        "quote": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
        "author": "Martin Fowler",
        "category": "Architecture"
    }
]

def fetch_external_quote_with_fallback(timeout_seconds=2.0):
    """
    Calls a third-party API with a strict time limit (timeout).
    If the API exceeds the time limit or encounters any error,
    it engages a zero-latency curated fallback without throwing errors.
    """
    api_url = "https://zenquotes.io/api/today"
    start_time = time.time()
    
    try:
        # Strict timeout enforcement
        response = requests.get(api_url, timeout=timeout_seconds, headers={"User-Agent": "StreamFlix-Platform/1.0"})
        latency_ms = round((time.time() - start_time) * 1000, 2)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0 and 'q' in data[0]:
                return {
                    "quote": data[0]['q'],
                    "author": data[0]['a'],
                    "source": "live_third_party_api (zenquotes.io)",
                    "latency_ms": latency_ms,
                    "timeout_limit_seconds": timeout_seconds,
                    "status": "success"
                }
    except requests.Timeout:
        logger.warning(f"Third-party API timed out (> {timeout_seconds}s). Fallback engaged.")
    except Exception as e:
        logger.warning(f"Third-party API request failed ({e}). Fallback engaged.")
        
    # Offline Fallback logic
    import random
    fallback = random.choice(FALLBACK_QUOTES)
    latency_ms = round((time.time() - start_time) * 1000, 2)
    return {
        "quote": fallback["quote"],
        "author": fallback["author"],
        "source": "offline_fallback_system",
        "latency_ms": latency_ms,
        "timeout_limit_seconds": timeout_seconds,
        "status": "fallback_engaged",
        "note": f"Primary API exceeded {timeout_seconds}s or was unreachable. Resilient fallback activated."
    }
