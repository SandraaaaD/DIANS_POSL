from textblob import TextBlob
def fetch_news(symbol: str):
    return [
        f"{symbol} price shows strong growth and investor confidence",
        f"Analysts warn about possible correction for {symbol}",
        f"{symbol} adoption increases among institutions"
    ]

def analyze_sentiment(symbol: str):
    news = fetch_news(symbol)

    polarity_sum = 0
    for article in news:
        blob = TextBlob(article)
        polarity_sum += blob.sentiment.polarity

    avg_polarity = polarity_sum / len(news)

    if avg_polarity > 0.1:
        sentiment = "positive"
    elif avg_polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment_score": round(avg_polarity, 3),
        "sentiment_signal": sentiment,
        "articles": news
    }
