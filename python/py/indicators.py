import pandas as pd
import ta


async def fetch_ohlcv(symbol: str, timeframe='1d', db_pool=None):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT date, open, high, low, close, volume FROM ohlcv WHERE symbol=$1 ORDER BY date ASC",
            symbol
        )
    df = pd.DataFrame(rows, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    if timeframe != '1d':
        if timeframe == '1w':
            df = df.resample('W').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
        elif timeframe == '1M':
            df = df.resample('M').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
    return df


def calculate_indicators(df: pd.DataFrame):
    indicators = pd.DataFrame(index=df.index)

    indicators['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    macd = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
    indicators['macd'] = macd.macd()
    stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'], window=14, smooth_window=3)
    indicators['stoch'] = stoch.stoch()
    indicators['adx'] = ta.trend.ADXIndicator(df['high'], df['low'], df['close'], window=14).adx()
    indicators['cci'] = ta.trend.CCIIndicator(df['high'], df['low'], df['close'], window=20).cci()

    indicators['sma'] = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator()
    indicators['ema'] = ta.trend.EMAIndicator(df['close'], window=20).ema_indicator()
    indicators['wma'] = ta.trend.WMAIndicator(df['close'], window=20).wma()
    bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
    indicators['bollinger_h'] = bb.bollinger_hband()
    indicators['bollinger_l'] = bb.bollinger_lband()
    indicators['vma'] = df['volume'].rolling(20).mean()

    signals = pd.DataFrame(index=df.index)
    signals['buy'] = ((indicators['rsi'] < 30) & (df['close'] > indicators['ema'])).astype(int)
    signals['sell'] = ((indicators['rsi'] > 70) & (df['close'] < indicators['ema'])).astype(int)
    signals['hold'] = 1 - (signals['buy'] + signals['sell'])

    return indicators, signals
