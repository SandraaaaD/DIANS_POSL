# from py.onchain_strategy import OnchainStrategy
from onchain_strategy import OnchainStrategy
from sentiment_strategy import SentimentStrategy
from technical_strategy import TechnicalStrategy

class StrategyFactory:
    @staticmethod
    def get_strategy(name):
        if name == "onchain":
            return OnchainStrategy()
        elif name == "sentiment":
            return SentimentStrategy()
        elif name == "technical":
            return TechnicalStrategy()
        else:
            raise ValueError(f"Unknown strategy: {name}")
