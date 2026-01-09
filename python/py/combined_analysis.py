from strategy_factory import StrategyFactory
from data_loader import load_ohlcv


async def combined_analysis(symbol: str, timeframe="1d"):
    results = {}

    # 1️⃣ Onchain + Sentiment стратегии
    # strategies = [
    #     OnchainStrategy(),
    #     SentimentStrategy()
    # ]
    strategy_names = ["onchain", "sentiment"]
    strategies = [StrategyFactory.get_strategy(name) for name in strategy_names]

    for strategy in strategies:
        data = await strategy.analyze(symbol)
        if data and isinstance(data, dict):
            results.update(data)

    # 2️⃣ Technical strategy

    df = await load_ohlcv(symbol, timeframe)

    tech_strategy = StrategyFactory.get_strategy("technical")

    if df is not None and not df.empty:
        # tech_strategy = TechnicalStrategy()
        tech_result = await tech_strategy.analyze(symbol, df=df)
        results["technical"] = tech_result
    else:
        results["technical"] = {"indicators": {}, "signals": {}}

    # 3️⃣ Финален сигнал
    final_signal = "neutral"
    onchain_signal = results.get("onchain_signal")
    sentiment_signal = results.get("sentiment_signal")

    if onchain_signal == "bullish" and sentiment_signal == "positive":
        final_signal = "strong_buy"
    elif onchain_signal == "bearish" and sentiment_signal == "negative":
        final_signal = "strong_sell"

    results["final_signal"] = final_signal
    return results
#



















# import httpx
# from data_loader import load_ohlcv
#
# async def combined_analysis(symbol: str, timeframe="1d"):
#     results = {}
#
#     # 1️⃣ ONCHAIN + SENTIMENT (МИКРОСЕРВИСИ)
#     async with httpx.AsyncClient() as client:
#         onchain_resp = await client.get(
#             "http://localhost:8001/analyze",
#             params={"symbol": symbol}
#         )
#         sentiment_resp = await client.get(
#             "http://localhost:8002/analyze",
#             params={"symbol": symbol}
#         )
#
#     results.update(onchain_resp.json())
#     results.update(sentiment_resp.json())
#
#     # 2️⃣ TECHNICAL (ОСТАНУВА ЛОКАЛНО)
#     df = await load_ohlcv(symbol, timeframe)
#
#     if df is not None and not df.empty:
#         from technical_strategy import TechnicalStrategy
#         tech = TechnicalStrategy()
#         results["technical"] = await tech.analyze(symbol, df=df)
#     else:
#         results["technical"] = {"indicators": {}, "signals": {}}
#
#     # 3️⃣ ФИНАЛЕН СИГНАЛ
#     final_signal = "neutral"
#     onchain_signal = results.get("onchain_signal")
#     sentiment_signal = results.get("sentiment_signal")
#
#     if onchain_signal == "bullish" and sentiment_signal == "positive":
#         final_signal = "strong_buy"
#     elif onchain_signal == "bearish" and sentiment_signal == "negative":
#         final_signal = "strong_sell"
#
#     results["final_signal"] = final_signal
#     return results
