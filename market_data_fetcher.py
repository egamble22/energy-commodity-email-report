import yfinance as yf
from tabulate import tabulate

def fetch_market_data():
    tickers = {
        "CL=F": "WTI Crude",
        "NG=F": "Natural Gas",
        "RB=F": "Gasoline",
        "XLE": "Energy ETF",
        "UNG": "NatGas ETF"
    }

    rows = []

    for symbol, name in tickers.items():
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="7d")

        if data.empty or len(data) < 2:
            continue

        latest = data.iloc[-1]
        previous = data.iloc[-2]

        current_price = latest['Close']
        prev_price = previous['Close']
        abs_change = current_price - prev_price
        pct_change = (abs_change / prev_price) * 100

        week_ago = data.iloc[0]['Close']
        weekly_change = ((current_price - week_ago) / week_ago) * 100

        high_24h = latest['High']
        low_24h = latest['Low']
        volume = latest['Volume']
        volatility = ((high_24h - low_24h) / prev_price) * 100

        rows.append([
            f"{name}",
            symbol,
            f"${current_price:.2f}",
            f"{abs_change:+.2f} ({pct_change:+.2f}%)",
            f"{weekly_change:+.2f}%",
            f"${high_24h:.2f}",
            f"${low_24h:.2f}",
            f"{volatility:.2f}%",
            f"{volume:,.0f}"
        ])

    headers = ["Name", "Ticker", "Current Price", "1D Change (%)", "7D Change (%)", "24H High", "24H Low", "Volatility (7D)", "Volume"]

    return rows, headers

