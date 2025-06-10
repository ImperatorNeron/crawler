from pathlib import Path
import random

# Rotating headers
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "uk,en-US;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "sec-ch-ua": f'"Chromium";v="{random.randint(120,126)}", "Google Chrome";v="{random.randint(120,126)}", "Not-A.Brand";v="24"',
    "sec-ch-ua-mobile": random.choice(["?0", "?1"]),
    "sec-ch-ua-platform": random.choice(['"Windows"', '"Android"', '"Linux"']),
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "upgrade-insecure-requests": "1",
    "user-agent": random.choice(
        [
            "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        ]
    ),
}

# Core directories and settings
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = "https://github.com/search"
TIMEOUT = 10
MAX_RETRIES = 3
DEFAULT_INPUT_DIR = BASE_DIR / "inputs"
DEFAULT_OUTPUT_DIR = BASE_DIR / "outputs"
