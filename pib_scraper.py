import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

KEYWORDS = ["Wheat", "Sugar", "Oil", "Maida", "Atta", "Food"]

def get_pib_news():
    today = datetime.now()
    results = []
    
    # Target Ministry of Consumer Affairs, Food & Public Distribution (id=24)
    # Most PIB URLs use this structure for All Releases
    url = "https://pib.gov.in/allrelease.aspx"
    
    try:
        # Headers help prevent being blocked
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=20, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for all links in the main content area
        for link in soup.find_all('a'):
            title = link.text.strip()
            # If a keyword is found
            if any(key.lower() in title.lower() for key in KEYWORDS):
                href = link.get('href', '')
                full_link = f"https://pib.gov.in{href}" if href.startswith('/') else href
                
                results.append({
                    "title": title,
                    "url": full_link,
                    "date": today.strftime("%d-%m-%Y"),
                    "aging": "Latest"
                })
                print(f"Found: {title}")

        # Save results - even if empty, save the [] brackets
        with open('pib_data.json', 'w') as f:
            json.dump(results, f, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_pib_news()
