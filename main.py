from market_data_fetcher import fetch_market_data
from email_sender_script import send_email
from fetch_relevant_news import fetch_relevant_news
from tabulate import tabulate

def main():
    rows, headers = fetch_market_data()
    news_articles = fetch_relevant_news()

    if not rows:
        print("⚠️ No market data available.")
        return

    print("\nFormatted Market Data:\n")
    print(tabulate(rows, headers=headers, tablefmt="pretty"))

    print("\nTop Suggested Articles:\n")
    for article in news_articles:
        print(f"- {article['title']} ({article['source']})")

    send_email(rows, headers, news_articles)

if __name__ == "__main__":
    main()