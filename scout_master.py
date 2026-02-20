import feedparser
import json
from datetime import datetime, timedelta

# --- 1. CONFIGURATION: 28 COMMODITIES & FILTERS ---
COMMODITIES = {
    "Wheat": "Wheat India News", 
    "Sugar": "Sugar Price India News",
    "Oil": "Palm Oil Soyoil India Price",
    "General": "Agriculture Policy India OR MSP OR Crop"
}

# The Surgical Search Filter from your Streamlit model
NEGATIVE_FILTER = " -price -mandi -rate -US -Global -Pakistan"

def fetch_rss_news(query, limit=50):
    # Surgical URL construction
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    
    results = []
    for entry in feed.entries:
        # Calculate aging
        dt = datetime(*entry.published_parsed[:6])
        diff = datetime.utcnow() - dt
        
        aging_text = f"{diff.days}d ago" if diff.days > 0 else f"{diff.seconds // 3600}h ago"
        
        results.append({
            "title": entry.title,
            "url": entry.link,
            "date": dt.strftime("%d-%b-%Y"),
            "aging": aging_text,
            "timestamp": dt.isoformat()
        })
    return sorted(results, key=lambda x: x['timestamp'], reverse=True)[:limit]

def run_sync():
    # Segment 1: Wheat News (Strict 6 months)
    wheat_data = fetch_rss_news(COMMODITIES["Wheat"] + NEGATIVE_FILTER)
    with open('wheat_news.json', 'w') as f:
        json.dump(wheat_data, f, indent=4)

    # Segment 2: PIB Style (Official News)
    # We use "site:pib.gov.in" to force only official results
    pib_query = "site:pib.gov.in (Wheat OR Sugar OR Oil OR MSP OR Export)"
    pib_data = fetch_rss_news(pib_query)
    with open('pib_data.json', 'w') as f:
        json.dump(pib_data, f, indent=4)

    # Segment 3: Regulatory (FSSAI/Standard News)
    reg_query = "FSSAI OR 'Food Standard' OR 'Regulatory Framework' India"
    reg_data = fetch_rss_news(reg_query)
    with open('fssai_data.json', 'w') as f:
        json.dump(reg_data, f, indent=4)

    print("Intelligence Sync Complete.")

if __name__ == "__main__":
    run_sync()
