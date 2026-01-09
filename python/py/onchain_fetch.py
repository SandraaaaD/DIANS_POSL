import requests


def fetch_onchain_metrics(symbol: str):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": symbol.lower(),
        "order": "market_cap_desc",
        "sparkline": "false",
        "price_change_percentage": "24h"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if len(data) == 0:
            return {"error": "Coin not found"}

        coin = data[0]

        metrics = {
            "current_price_usd": coin.get("current_price"),
            "market_cap_usd": coin.get("market_cap"),
            "total_volume_usd": coin.get("total_volume"),
            "price_change_percentage_24h": coin.get("price_change_percentage_24h"),
            "circulating_supply": coin.get("circulating_supply"),
            "total_supply": coin.get("total_supply"),
            "ath": coin.get("ath"),
            "atl": coin.get("atl")
        }
        return metrics

    except requests.RequestException as e:
        return {"error": str(e)}