import pandas as pd
from textblob import TextBlob

def calculate_ema(prices: pd.Series, span: int) -> pd.Series:
    return prices.ewm(span=span, adjust=False).mean()

def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> float:
    tr = pd.concat([
        (high - low),
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(window=period).mean().iloc[-1]

def analyze_sentiment(text: str) -> float:
    return TextBlob(text).sentiment.polarity  # -1 to +1

def score_asset(price_data: pd.DataFrame, headline: str, market_volatility: float = 0.02) -> float:
    if price_data is None or len(price_data) < 20:
        return 0.0

    prices = price_data['Close']
    high = price_data['High']
    low = price_data['Low']
    close = price_data['Close']

    ema_short = calculate_ema(prices, span=5).iloc[-1]
    ema_long = calculate_ema(prices, span=20).iloc[-1]
    momentum_score = 1 if ema_short > ema_long else 0

    atr = calculate_atr(high, low, close)
    volatility_score = 1 if atr <= market_volatility else 0

    sentiment_score = analyze_sentiment(headline)
    sentiment_normalized = (sentiment_score + 1) / 2  # convert -1→1 to 0→1

    final_score = 0.4 * momentum_score + 0.3 * volatility_score + 0.3 * sentiment_normalized
    return round(final_score, 3)