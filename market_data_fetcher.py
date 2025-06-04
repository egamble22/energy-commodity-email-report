import yfinance as yf

tickers = {
    "CL=F": "WTI Crude",
    "NG=F": "Natural Gas",
    "RB=F": "Gasoline",
    "XLE": "Energy ETF",
    "UNG": "NatGas ETF"
}

for symbol, name in tickers.items():
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="7d")

    if data.empty:
        print(f"No data found for {name} ({symbol})")
        continue

    latest = data.iloc[-1]
    previous = data.iloc[-2]

    current_price = latest['Close']
    prev_price = previous['Close']
    abs_change = current_price - prev_price
    pct_change = (abs_change / prev_price) * 100

    print(f"\n{name} ({symbol})")
    print(f"Current Price: ${current_price:.2f}")
    print(f"Change: {abs_change:+.2f} ({pct_change:+.2f}%)")
    print(f"High (24h): ${latest['High']:.2f}")
    print(f"Low (24h): ${latest['Low']:.2f}")

print("\nFinished fetching all tickers.")