import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Full list of your 28 commodities
COMMODITIES = [
    "Wheat", "Maize", "Paddy", "Chana", "Sugar", "Palm Oil", "Rice bran oil", 
    "Soyabean", "Sunflower oil", "Cotton seed oil", "Groundnut", "Turmeric", 
    "Black pepper", "Cardamom", "Chilli", "Cashew", "Almond", "Raisins", 
    "Oats", "Isabgol", "Potato", "Onion", "Milk", "Dairy", "Cocoa", "Ethanol"
]

def scrape_pib():
    today = datetime.now()
    # Ministry of Consumer Affairs & Food Distribution (reg=3, lang=1)
    URL = "https://www.pib.gov.in/AllRelease.aspx?MenuId=286&reg=3&lang=1"
    
    print(f"--- Starting PIB Scan: {today.strftime('%d-%b-%Y')} ---")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        pib_updates = []
        # PIB lists releases under <ul> or specific content divs
        for link in soup.find_all('a'):
            title = link.text.strip()
            # Check if any commodity is in the title
            if any(com.lower() in title.lower() for com in COMMODITIES):
                href = link.get('href', '')
                pib_updates.append({
                    "title": title,
                    "url": f"https://pib.gov.in{href}" if href.startswith('/') else href,
                    "date": today.strftime("%d-%b-%Y"),
                    "aging": "Latest Policy"
                })
                print(f"Found PIB: {title[:50]}...")

        with open('pib_data.json', 'w') as f:
            json.dump(pib_updates[:100], f, indent=4)
        print(f"Success: Saved {len(pib_updates)} PIB entries.")

    except Exception as e:
        print(f"PIB Error: {e}")

if __name__ == "__main__":
    scrape_pib()
