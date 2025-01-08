import os
import requests
import logging
from typing import List
from time import sleep

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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
            logger.info(
                "Fetching Binance trading symbols from %s...", BINANCE_API_URL
            )
            response = requests.get(BINANCE_API_URL, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the JSON response
            data = response.json()
            symbols = [item["symbol"] for item in data.get("symbols", [])]

            if not symbols:
                logger.warning("No symbols found in the response.")
                return []

            logger.info("Successfully fetched %d symbols.", len(symbols))
            return symbols

        except requests.exceptions.Timeout:
            logger.error("Request timed out. Retrying...")
        except requests.exceptions.RequestException as e:
            logger.error("Request failed: %s", e)
        except KeyError as e:
            logger.error("Unexpected response format: missing key %s", e)
            break

        retries += 1
        if retries < MAX_RETRIES:
            logger.info("Retrying in %d seconds...", RETRY_DELAY)
            sleep(RETRY_DELAY)

    logger.error(
        "Failed to fetch Binance symbols after %d attempts.", MAX_RETRIES
    )
    return []


def main():
    """Main function to fetch and display Binance trading symbols."""
    symbols = fetch_binance_coins()
    if symbols:
        print(f"Fetched {len(symbols)} symbols.")
        print("First 10 symbols:", symbols[:10])
    else:
        print("Failed to fetch symbols.")


if __name__ == "__main__":
    main()
