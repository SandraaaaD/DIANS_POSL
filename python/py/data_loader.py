import pandas as pd
from db import get_pool

async def load_ohlcv(symbol: str, timeframe: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT date, close
            FROM ohlcv
            WHERE symbol = $1
            ORDER BY date ASC
        """, symbol)

    await pool.close()

    df = pd.DataFrame(rows, columns=["date", "close"])
    df["date"] = pd.to_datetime(df["date"])
    return df


