import asyncio
from analysis_strategy import AnalysisStrategy
from onchein_news_and_analize import analyze_sentiment

class SentimentStrategy(AnalysisStrategy):
    async def analyze(self, symbol, df=None):
        return await asyncio.to_thread(analyze_sentiment, symbol)
