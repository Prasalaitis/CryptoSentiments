import os
import requests
import logging
from typing import List
from time import sleep

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# API configuration
BINANCE_API_URL = os.getenv(
    "BINANCE_API_URL", "https://api.binance.com/api/v3/exchangeInfo"
)
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", 5))  # in seconds


def fetch_binance_coins() -> List[str]:
    """
    Fetches the list of trading symbols from Binance's API with retry logic.

    Returns:
        List[str]: A list of trading symbols available on Binance.
    """
    retries = 0
    while retries < MAX_RETRIES:
        try:
            logging.info(
                "Fetching Binance trading symbols from %s...", BINANCE_API_URL
            )
            response = requests.get(BINANCE_API_URL, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the JSON response
            data = response.json()
            symbols = [item["symbol"] for item in data.get("symbols", [])]

            logging.info("Successfully fetched %d symbols.", len(symbols))
            return symbols
        except requests.exceptions.RequestException as e:
            retries += 1
            logging.error(
                "Error fetching Binance symbols (attempt %d/%d): %s",
                retries,
                MAX_RETRIES,
                e,
            )
            if retries < MAX_RETRIES:
                logging.info("Retrying in %d seconds...", RETRY_DELAY)
                sleep(RETRY_DELAY)
        except KeyError as e:
            logging.error("Unexpected response format: missing key %s", e)
            break

    logging.error(
        "Failed to fetch Binance symbols after %d attempts.", MAX_RETRIES
    )
    return []


if __name__ == "__main__":
    symbols = fetch_binance_coins()
    if symbols:
        print(f"Fetched {len(symbols)} symbols.")
    else:
        print("Failed to fetch symbols.")
