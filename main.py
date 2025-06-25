from extract.extract_market import fetch_quote

def run():
    tickers = ["AAPL", "NVDA", "AMZN"]
    results = [fetch_quote(t) for t in tickers]
    for r in results:
        print(f"{r['symbol']} @ ${r['price']} — Volume: {r['volume']}")

if __name__ == "__main__":
    run()