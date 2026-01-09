from onchain_fetch import *

def analyze_onchain(symbol: str):
    data = fetch_onchain_metrics(symbol)

    if "error" in data:
        return {"error": data["error"], "onchain_signal": "neutral"}

    pct = data.get("price_change_percentage_24h", 0)
    if pct > 0.1:
        signal = "bullish"
    elif pct < -0.1:
        signal = "bearish"
    else:
        signal = "neutral"

    return {
        "metrics": data,
        "onchain_signal": signal
    }