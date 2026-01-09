from abc import ABC, abstractmethod

class AnalysisStrategy(ABC):
    @abstractmethod
    async def analyze(self, symbol, df=None):
        pass