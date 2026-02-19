import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

# Target URL (Full Archive)
URL = "https://fssai.gov.in/cms/advisories-directions-orders-circulars.php"

# Broader keywords to capture general policy and specific commodities
KEYWORDS = [
    "Wheat", "Atta", "Maida", "Sugar", "Oil", "Palm", "Fats", 
    "Agri", "Fortification", "Adulteration", "Draft", "Amendment", "Standard"
]

def scrape_fssai():
    # Calculate the date 60 days ago
    date_limit = datetime.now() - timedelta(days=60)
    print(f"Scanning circulars since: {date_limit.strftime('%d-%m-%Y')}")

    try:
        # Headers help prevent being blocked by the government website
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, timeout=20, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        alerts = []
        table = soup.find('table')
        if not table: return

        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) < 2: continue
            
            # 1. Parse Date (FSSAI format: DD-MM-YYYY)
            date_text = cols[0].text.strip()
            try:
                item_date = datetime.strptime(date_text, '%d-%m-%Y')
            except: continue

            # 2. Filter: Only last 60 days
            if item_date < date_limit:
                continue

            # 3. Filter: Keywords
            title = cols[1].text.strip()
            if any(key.lower() in title.lower() for key in KEYWORDS):
                link_tag = cols[1].find('a')
                link = link_tag['href'] if link_tag else ""
                
                alerts.append({
                    "date": date_text,
                    "title": title,
                    "url": link if link.startswith('http') else f"https://fssai.gov.in{link}"
                })

        # Save the results
        with open('fssai_data.json', 'w') as f:
            json.dump(alerts, f, indent=4)
        print(f"Success! Found {len(alerts)} alerts.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_fssai()
