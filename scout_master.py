import feedparser
import json
import os
from datetime import datetime

# 28 Commodity Logic + Official Sources
QUERIES = {
    "wheat": "Wheat+India+News+OR+MSP+OR+Policy",
    "pib": "site:pib.gov.in+Wheat+OR+Sugar+OR+Oil+OR+Edible+Oil",
    "reg": "FSSAI+India+Advisory+OR+Order+OR+Standard"
}

def fetch_data(query_key):
    url = f"https://news.google.com/rss/search?q={QUERIES[query_key]}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    
    print(f"DEBUG: Found {len(feed.entries)} items for {query_key}")
    
    results = []
    for entry in feed.entries:
        # We use strict lowercase keys: title, url, date, aging
        results.append({
            "title": entry.title,
            "url": entry.link,
            "date": entry.published if hasattr(entry, 'published') else "Recent",
            "aging": "Latest Pulse"
        })
    return results[:100] # Max 100 items per segment

def sync():
    # This creates the 3 files your PWA is looking for
    with open('wheat_news.json', 'w') as f: 
        json.dump(fetch_data("wheat"), f, indent=4)
    
    with open('pib_data.json', 'w') as f: 
        json.dump(fetch_data("pib"), f, indent=4)
        
    with open('fssai_data.json', 'w') as f: 
        json.dump(fetch_data("reg"), f, indent=4)
        
    print("Sync Complete: All JSON files updated.")

if __name__ == "__main__":
    sync()
