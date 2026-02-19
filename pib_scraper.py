import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

# Press Information Bureau "All Releases" URL
BASE_URL = "https://pib.gov.in/allrelease.aspx"
KEYWORDS = ["Wheat", "Sugar", "Oil", "Maida", "Atta"]
LOOKBACK_DAYS = 90

def get_pib_news():
    today = datetime.now()
    results = []
    
    # Check the current and past 2 months to cover 90 days
    for i in range(3):
        # Calculate target month/year
        target_date = today - timedelta(days=i*30)
        m = target_date.strftime("%m")
        y = target_date.strftime("%Y")
        
        # Build URL for Ministry of Consumer Affairs & Food Distribution (id=24)
        query_url = f"{BASE_URL}?month={m}&year={y}&reg=3&lang=1"
        
        try:
            response = requests.get(query_url, timeout=20)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # PIB lists releases in <ul> bullets
            for li in soup.find_all('li'):
                title = li.text.strip()
                if any(key.lower() in title.lower() for key in KEYWORDS):
                    link = li.find('a')['href'] if li.find('a') else ""
                    
                    # Extract the release date if possible, otherwise use target_date
                    # This is a simplified aging calculation
                    aging_days = (today - target_date).days
                    
                    results.append({
                        "title": title,
                        "url": f"https://pib.gov.in{link}" if link.startswith('/') else link,
                        "date": target_date.strftime("%d-%m-%Y"),
                        "aging": f"{aging_days} days ago" if aging_days > 0 else "Today"
                    })
        except Exception as e:
            print(f"Error scraping month {m}: {e}")

    with open('pib_data.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    get_pib_news()
