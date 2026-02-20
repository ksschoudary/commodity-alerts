import feedparser
import json
from datetime import datetime, timedelta

# BROADENING SEARCH: Removed strict filters to ensure results
# Using exactly what usually works for Google News RSS
QUERIES = {
    "wheat": "Wheat+India+News",
    "pib": "site:pib.gov.in+Wheat+OR+Sugar+OR+Oil",
    "reg": "FSSAI+India+Notice+OR+Order"
}

def fetch_data(query_key):
    url = f"https://news.google.com/rss/search?q={QUERIES[query_key]}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    
    # Debug print for GitHub Logs
    print(f"DEBUG: Found {len(feed.entries)} items for {query_key}")
    
    results = []
    for entry in feed.entries:
        # We will keep the latest 50 results regardless of age for now to test output
        results.append({
            "title": entry.title,
            "url": entry.link,
            "date": entry.published,
            "aging": "Latest" 
        })
    return results[:50]

def sync():
    # Save all files
    with open('wheat_news.json', 'w') as f: json.dump(fetch_data("wheat"), f, indent=4)
    with open('pib_data.json', 'w') as f: json.dump(fetch_data("pib"), f, indent=4)
    with open('fssai_data.json', 'w') as f: json.dump(fetch_data("reg"), f, indent=4)
    print("Files updated successfully.")

if __name__ == "__main__":
    sync()
