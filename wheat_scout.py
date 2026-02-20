import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

# Search keywords as requested
KEYWORDS = ["wheat", "india", "msp", "price", "policy", "market", "govt", "australia", "russia"]
RSS_URL = "https://news.google.com/rss/search?q=wheat+india+msp+policy+price&hl=en-IN&gl=IN&ceid=IN:en"

def scrape_wheat_news():
    six_months_ago = datetime.now() - timedelta(days=180)
    response = requests.get(RSS_URL)
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')
    
    wheat_news = []
    for item in items:
        title = item.title.text
        link = item.link.text
        pub_date = datetime.strptime(item.pubDate.text, '%a, %d %b %Y %H:%M:%S %Z')
        
        # Filter by aging (6 months) and keywords
        if pub_date >= six_months_ago:
            if any(key.lower() in title.lower() for key in KEYWORDS):
                wheat_news.append({
                    "title": title,
                    "url": link,
                    "date": pub_date.strftime("%d-%b-%Y"),
                    "source": "Global News"
                })
    
    with open('wheat_news.json', 'w') as f:
        json.dump(wheat_news[:100], f, indent=4) # Max 100 items

if __name__ == "__main__":
    scrape_wheat_news()
