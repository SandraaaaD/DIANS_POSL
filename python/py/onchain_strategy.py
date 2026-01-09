import asyncio
from analysis_strategy import AnalysisStrategy
from onchein_analize import analyze_onchain

class OnchainStrategy(AnalysisStrategy):
    async def analyze(self, symbol, df=None):
        return await asyncio.to_thread(analyze_onchain, symbol)
