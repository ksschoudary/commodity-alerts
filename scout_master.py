import feedparser
import json
import os
from datetime import datetime

QUERIES = {
    "wheat": "Wheat+India+News+OR+MSP+OR+Policy",
    "pib": "site:pib.gov.in+Wheat+OR+Sugar+OR+Oil",
    "reg": "FSSAI+India+Advisory+OR+Order"
}

def fetch_data(query_key):
    url = f"https://news.google.com/rss/search?q={QUERIES[query_key]}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    
    results = []
    for entry in feed.entries:
        # Get raw timestamp for sorting
        ts = entry.published_parsed if hasattr(entry, 'published_parsed') else None
        
        results.append({
            "title": entry.title,
            "url": entry.link,
            "date": entry.published if hasattr(entry, 'published') else "Recent",
            "sort_key": datetime(*ts[:6]).timestamp() if ts else 0,
            "aging": "Latest Pulse"
        })
    
    # SORT BY FRESHNESS: Newest (highest timestamp) first
    sorted_results = sorted(results, key=lambda x: x['sort_key'], reverse=True)
    return sorted_results[:100]

def sync():
    # Capture sync time in IST
    sync_time = datetime.now().strftime("%d %b, %I:%M %p")
    
    data = {
        "last_updated": sync_time,
        "wheat": fetch_data("wheat"),
        "pib": fetch_data("pib"),
        "reg": fetch_data("reg")
    }

    # Save to one master file or keep independent? 
    # Let's keep independent but add the timestamp to each
    for key in ["wheat", "pib", "reg"]:
        output = {"sync_time": sync_time, "news": data[key]}
        with open(f'{key}_news.json' if key == 'wheat' else f'{key}_data.json', 'w') as f:
            json.dump(output, f, indent=4)
        
    print(f"Sync Complete at {sync_time}")

if __name__ == "__main__":
    sync()
