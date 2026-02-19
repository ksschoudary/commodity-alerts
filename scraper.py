import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

# Target URLs
URL = "https://fssai.gov.in/cms/advisories-directions-orders-circulars.php"
# Expanded keywords based on your request
KEYWORDS = ["Wheat", "Sugar", "Oil", "Agri", "Maida", "Atta", "Fortification", "Edible"]

def scrape_fssai():
    # Calculate the date 60 days ago
    date_limit = datetime.now() - timedelta(days=60)
    print(f"Scanning for circulars since: {date_limit.strftime('%d-%m-%Y')}")

    try:
        response = requests.get(URL, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        alerts = []
        
        table = soup.find('table')
        if not table:
            print("Table not found on FSSAI page.")
            return

        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) < 2: continue
            
            # 1. Parse the Date
            date_text = cols[0].text.strip()
            try:
                # FSSAI typically uses DD-MM-YYYY
                item_date = datetime.strptime(date_text, '%d-%m-%Y')
            except:
                continue # Skip if date format is weird

            # 2. Check if within 60 days
            if item_date < date_limit:
                continue

            # 3. Check for Keywords
            title = cols[1].text.strip()
            if any(key.lower() in title.lower() for key in KEYWORDS):
                link_tag = cols[1].find('a')
                link = link_tag['href'] if link_tag else ""
                
                alerts.append({
                    "date": date_text,
                    "title": title,
                    "url": link if link.startswith('http') else f"https://fssai.gov.in{link}"
                })

        # Save the filtered results
        with open('fssai_data.json', 'w') as f:
            json.dump(alerts, f, indent=4)
        print(f"Found {len(alerts)} relevant circulars in last 60 days.")

    except Exception as e:
        print(f"Error during scrape: {e}")

if __name__ == "__main__":
    scrape_fssai()
