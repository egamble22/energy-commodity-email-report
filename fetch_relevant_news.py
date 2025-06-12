import requests
from datetime import datetime, timedelta
import os
import json
from dotenv import load_dotenv

load_dotenv()  

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
HISTORY_FILE = "sent_articles.json"


ENERGY_KEYWORDS = [
    "energy", "oil", "gas", "electricity", "renewable", "power", 
    "natural gas", "fossil", "solar", "wind", "grid"
]

def is_relevant(article):
    
    text = f"{article.get('title', '')} {article.get('description', '')}".lower()
    return any(keyword in text for keyword in ENERGY_KEYWORDS)

def load_sent_urls():
    try:
        with open(HISTORY_FILE, "r") as file:
            return set(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_sent_urls(urls):
    try:
        with open(HISTORY_FILE, "w") as file:
            json.dump(list(urls), file)
    except Exception as e:
        print(f"❌ Failed to save history: {e}")

def fetch_relevant_news():
    if not NEWS_API_KEY:
        print("❌ NEWS_API_KEY not found in environment variables.")
        return []

    url = "https://newsapi.org/v2/everything"
    from_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    params = {
        "q": "energy OR oil OR gas OR electricity OR renewables",
        "from": from_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 25,
        "apiKey": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])

        previously_sent = load_sent_urls()
        new_articles = []

        for article in articles:
            if not is_relevant(article):
                continue

            url = article["url"]
            if url in previously_sent:
                continue  # Skip previously sent articles

            new_articles.append({
                "title": article["title"],
                "url": url,
                "source": article["source"]["name"]
            })

            if len(new_articles) == 5:
                break

        
        updated_urls = previously_sent.union([a["url"] for a in new_articles])
        save_sent_urls(updated_urls)

        return new_articles

    except Exception as e:
        print(f"❌ Failed to fetch news: {e}")
        return []

if __name__ == "__main__":
    from pprint import pprint
    pprint(fetch_relevant_news())