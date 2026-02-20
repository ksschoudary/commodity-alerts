import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

# Enhanced Search Query for broader coverage
RSS_URL = "https://news.google.com/rss/search?q=wheat+india+OR+wheat+msp+OR+wheat+policy&hl=en-IN&gl=IN&ceid=IN:en"

def scrape_wheat_news():
    six_months_ago = datetime.now() - timedelta(days=180)
    print(f"--- Starting Wheat Scan (Limit: {six_months_ago.strftime('%d-%b-%Y')}) ---")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(RSS_URL, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        print(f"DEBUG: Found {len(items)} items in the raw RSS feed.")
        
        wheat_news = []
        for item in items:
            title = item.title.text
            link = item.link.text
            
            # Parsing Google's date format
            raw_date = item.pubDate.text
            try:
                # Truncate timezone for parsing
                clean_date = " ".join(raw_date.split(" ")[:-1])
                pub_date = datetime.strptime(clean_date, '%a, %d %b %Y %H:%M:%S')
            except:
                continue
            
            # Filter Logic: Must contain 'wheat' and be within 6 months
            if pub_date >= six_months_ago and "wheat" in title.lower():
                wheat_news.append({
                    "title": title,
                    "url": link,
                    "date": pub_date.strftime("%d-%b-%Y"),
                    "source": "Market Intel"
                })

        print(f"DEBUG: Successfully matched {len(wheat_news)} wheat articles.")
        
        # Write to JSON
        with open('wheat_news.json', 'w') as f:
            json.dump(wheat_news[:100], f, indent=4)
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    scrape_wheat_news()
