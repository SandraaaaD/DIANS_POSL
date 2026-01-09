from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import pandas as pd
import numpy as np
import ta
from contextlib import asynccontextmanager

from data_loader import load_ohlcv
from train import train_lstm
from predict import predict_future
from onchain_fetch import *
from onchein_analize import *
from onchein_news_and_analize import *

from combined_analysis import combined_analysis

DB_CONFIG = {
    'host': 'my_postgres',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',
    'database': 'dians_baza',
}

# DB_CONFIG = { 'host': 'das-db-2026.postgres.database.azure.com',
#               'port': 5432,
#               'user': 'postgres',
#               'password': 'sd7589F!nk!',
#               'database': 'example_db',
#               }


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting FastAPI + creating DB pool...")
    app.state.db_pool = await asyncpg.create_pool(**DB_CONFIG)
    yield
    print("Closing DB pool...")
    await app.state.db_pool.close()




app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test-db")
async def test_db():
    pool = app.state.db_pool
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT symbol FROM ohlcv LIMIT 5")
        print(result)
    return {"result": result}

@app.get("/symbols")
async def get_symbols():
    pool = app.state.db_pool
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT DISTINCT symbol FROM ohlcv ORDER BY symbol ASC")
    return [row["symbol"] for row in rows]


@app.get("/indicators/{symbol}")
async def get_indicators(symbol: str, timeframe: str = "1d"):
    try:
        pool = app.state.db_pool
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT date, close FROM ohlcv WHERE symbol = $1 ORDER BY date ASC",
                symbol
            )
        if not rows:
            return {"indicators": {}, "signals": {}}

        df = pd.DataFrame(rows, columns=['date', 'close'])
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        if len(df) < 2:
            return {"indicators": {}, "signals": {}}

        # EMA/SMA/RSI/MACD
        df["ema"] = ta.trend.EMAIndicator(df["close"], window=3).ema_indicator()
        df["sma"] = ta.trend.SMAIndicator(df["close"], window=3).sma_indicator()
        df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=3).rsi()
        df["macd"] = ta.trend.MACD(df["close"]).macd()

        df.fillna(method='ffill', inplace=True)
        df.fillna(0, inplace=True)

        signals = {}
        prev_ema = None
        prev_close = None
        for date, row in df.iterrows():
            ema = row["ema"]
            close = row["close"]
            signal = {}
            if prev_ema is not None:
                if close > ema and prev_close <= prev_ema:
                    signal["buy"] = True
                elif close < ema and prev_close >= prev_ema:
                    signal["sell"] = True
            if signal:
                signals[str(date.date())] = signal
            prev_ema = ema
            prev_close = close

        indicators_dict = {
            str(date.date()): {
                "ema": row["ema"],
                "sma": row["sma"],
                "rsi": row["rsi"],
                "macd": row["macd"]
            }
            for date, row in df.iterrows()
        }

        return {"indicators": indicators_dict, "signals": signals}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


@app.get("/lstm/predict")
async def lstm_predict(symbol: str, timeframe: str = "1d", days: int = 7):
    df = await load_ohlcv(symbol, timeframe)

    model, scaler, last_window, predicted_price, prob_up, prob_down = train_lstm(df)

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "predicted_price": round(predicted_price, 2),
        "prob_up": round(prob_up, 2),
        "prob_down": round(prob_down, 2)
    }



# @app.get("/onchain-sentiment/{symbol}")
# def combined_analysis(symbol: str):
#     onchain = analyze_onchain(symbol)
#     sentiment = analyze_sentiment(symbol)
#
#     final_signal = "neutral"
#
#     if onchain["onchain_signal"] == "bullish" and sentiment["sentiment_signal"] == "positive":
#         final_signal = "strong_buy"
#     elif onchain["onchain_signal"] == "bearish" and sentiment["sentiment_signal"] == "negative":
#         final_signal = "strong_sell"
#
#     return {
#         "symbol": symbol,
#         "onchain": onchain,
#         "sentiment": sentiment,
#         "final_signal": final_signal
#     }

@app.get("/onchain-sentiment/{symbol}")
async def get_combined_analysis(symbol: str):
    try:
        return await combined_analysis(symbol)
    except Exception as e:
        return {
            "error": str(e),
            "final_signal": "error"
        }