import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# 1. Target URL (FSSAI Advisories & Orders)
URL = "https://fssai.gov.in/cms/advisories-directions-orders-circulars.php"
KEYWORDS = ["Wheat", "Atta", "Sugar", "Oil", "Fortification"]

def scrape_fssai():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    alerts = []
    # FSSAI typically uses tables for these lists
    table = soup.find('table')
    if not table: return
    
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) < 2: continue
        
        title = cols[1].text.strip()
        # Check if any of our keywords are in the title
        if any(key.lower() in title.lower() for key in KEYWORDS):
            link = cols[1].find('a')['href'] if cols[1].find('a') else ""
            alerts.append({
                "date": cols[0].text.strip(),
                "title": title,
                "url": link if link.startswith('http') else f"https://fssai.gov.in{link}",
                "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
    
    # Save the hits to a JSON file for your PWA to read
    with open('fssai_data.json', 'w') as f:
        json.dump(alerts, f, indent=4)

if __name__ == "__main__":
    scrape_fssai()
