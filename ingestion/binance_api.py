import requests

def fetch_binance_coins():
    response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
    symbols = [item["symbol"] for item in response.json()["symbols"]]
    return symbols
