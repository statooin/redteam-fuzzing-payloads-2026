#!/usr/bin/env python3
"""
asm_fuzz_runner.py - Attack Surface Management Fuzzer (2026 Edition)

Designed for integrating DevSecOps CI/CD pipelines and automated Red Team
infrastructure validation. This asynchronous HTTP fuzzer validates exposure
against cloud-native deployments, LLM gateways, and microservices.

Author: Senior SRE / DevSecOps Architect
"""

import asyncio
import aiohttp
import argparse
import logging
import random
import sys
from typing import List

# Setup SRE-level logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(module)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("asm_fuzzer")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "ASM-Validation-Bot/2026.1 (+https://security.internal)",
    "Prometheus/2.45.0",
    "Go-http-client/1.1"
]

async def fetch(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> None:
    """Perform an asynchronous HTTP GET request with rate limiting."""
    async with semaphore:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "*/*",
            "Connection": "close"
        }
        try:
            async with session.get(url, headers=headers, timeout=5) as response:
                status = response.status
                # Log interesting findings (e.g., 200 OK or 403 Forbidden on hidden assets)
                if status in [200, 204, 301, 302, 401, 403]:
                    logger.info(f"FOUND - [{status}] {url}")
                else:
                    logger.debug(f"MISSED - [{status}] {url}")
        except asyncio.TimeoutError:
            logger.warning(f"TIMEOUT - {url}")
        except Exception as e:
            logger.error(f"ERROR - {url} - {str(e)}")

async def run_fuzzer(target: str, wordlist_path: str, concurrency: int) -> None:
    """Main execution loop for asynchronous fuzzing."""
    logger.info(f"Initializing ASM Fuzzer targeting: {target}")
    logger.info(f"Loading payloads from: {wordlist_path}")
    logger.info(f"Concurrency level set to: {concurrency}")

    try:
        with open(wordlist_path, 'r') as file:
            payloads = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        logger.error(f"Wordlist not found: {wordlist_path}")
        sys.exit(1)

    # Normalize target URL
    if not target.endswith('/'):
        target += '/'

    urls: List[str] = [f"{target}{payload}" for payload in payloads]
    semaphore = asyncio.Semaphore(concurrency)

    connector = aiohttp.TCPConnector(limit=concurrency, verify_ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch(session, url, semaphore) for url in urls]
        await asyncio.gather(*tasks)
        
    logger.info("Fuzzing cycle completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ASM Async HTTP Fuzzer for CI/CD pipelines.")
    parser.add_argument("-t", "--target", required=True, help="Target base URL (e.g., https://api.staging.internal)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the payload wordlist file")
    parser.add_argument("-c", "--concurrency", type=int, default=10, help="Number of concurrent requests (default: 10)")
    parser.add_argument("--debug", action="store_true", help="Enable debug level logging")
    
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        # Compatibility for Windows environments in modern Python
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        asyncio.run(run_fuzzer(args.target, args.wordlist, args.concurrency))
    except KeyboardInterrupt:
        logger.info("Fuzzing aborted by user.")
        sys.exit(0)