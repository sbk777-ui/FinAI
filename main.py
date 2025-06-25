import yfinance as yf
import pandas as pd
from scorer import score_asset

def fetch_price_data(ticker: str) -> pd.DataFrame:
    data = yf.Ticker(ticker)
    hist = data.history(period="1mo")
    if hist.empty:
        return None
    hist.reset_index(inplace=True)
    return hist[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

def mock_headline(ticker: str) -> str:
    # This simulates a headline per stock (in real use: fetch from News API)
    return f"{ticker} shows strong momentum after earnings release"

def main():
    tickers = ["AAPL", "NVDA", "AMZN", "MSFT"]
    results = []

    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        price_data = fetch_price_data(ticker)
        if price_data is None:
            print(f"No data for {ticker}")
            continue

        headline = mock_headline(ticker)
        score = score_asset(price_data, headline)
        results.append((ticker, score))

    print("\n📊 Scoring Summary:")
    for symbol, score in results:
        print(f"{symbol}: Score = {score}")

if __name__ == "__main__":
    main()
