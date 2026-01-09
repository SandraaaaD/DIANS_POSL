from analysis_strategy import AnalysisStrategy
from data_loader import load_ohlcv
from indicators import calculate_indicators

class TechnicalStrategy(AnalysisStrategy):
    async def analyze(self, symbol, df=None):
        if df is None:
            raise ValueError("df is required for technical analysis")
        # return calculate_indicators(df)
        indicators, signals = calculate_indicators(df)

        return {
            "indicators": indicators.fillna(0).to_dict(),
            "signals": signals.fillna(0).to_dict()
        }