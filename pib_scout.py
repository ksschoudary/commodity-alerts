import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

COMMODITIES = ["Wheat", "Maize", "Paddy", "Chana", "Sugar", "Palm Oil", "Soyabean", "Turmeric", "Cashew", "Isabgol", "Milk", "Potato", "Onion"] # Expanded to 28 in your full list
PIB_URL = "https://pib.gov.in/allrelease.aspx"

def scrape_pib():
    today = datetime.now()
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(PIB_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pib_updates = []
    for link in soup.find_all('a'):
        title = link.text.strip()
        if any(com.lower() in title.lower() for com in COMMODITIES):
            href = link.get('href', '')
            pib_updates.append({
                "title": title,
                "url": f"https://pib.gov.in{href}" if href.startswith('/') else href,
                "date": today.strftime("%d-%b-%Y"),
                "aging": "Latest Update"
            })
            
    with open('pib_data.json', 'w') as f:
        json.dump(pib_updates[:100], f, indent=4)

if __name__ == "__main__":
    scrape_pib()
