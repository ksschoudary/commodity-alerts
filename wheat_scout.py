import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

# Broader Search Query for Google News RSS
# This searches for Wheat in India OR Wheat MSP OR Wheat Policy
RSS_URL = "https://news.google.com/rss/search?q=wheat+india+OR+wheat+msp+OR+wheat+policy&hl=en-IN&gl=IN&ceid=IN:en"

# We will look for ANY of these keywords in the title
KEYWORDS = ["wheat", "india", "msp", "price", "policy", "market", "govt", "australia", "russia", "crop"]

def scrape_wheat_news():
    six_months_ago = datetime.now() - timedelta(days=180)
    print(f"--- Starting Wheat Scan (Looking back to {six_months_ago.strftime('%Y-%m-%d')}) ---")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(RSS_URL, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        print(f"Found {len(items)} total items in RSS feed.")
        
        wheat_news = []
        for item in items:
            title = item.title.text
            link = item.link.text
            # Parse Google News date format: 'Fri, 20 Feb 2026 08:00:00 GMT'
            raw_date = item.pubDate.text
            try:
                # Remove timezone for easier parsing
                clean_date_str = " ".join(raw_date.split(" ")[:-1])
                pub_date = datetime.strptime(clean_date_str, '%a, %d %b %Y %H:%M:%S')
            except Exception as e:
                print(f"Date error for '{title}': {e}")
                continue
            
            # 1. Check aging (6 months)
            if pub_date >= six_months_ago:
                # 2. Check if 'wheat' is in title (the main requirement)
                if "wheat" in title.lower():
                    wheat_news.append({
                        "title": title,
                        "url": link,
                        "date": pub_date.strftime("%d-%b-%Y"),
                        "source": "Market Intel"
                    })

        print(f"Successfully matched {len(wheat_news)} wheat articles.")
        
        with open('wheat_news.json', 'w') as f:
            json.dump(wheat_news[:100], f, indent=4)
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    scrape_wheat_news()
