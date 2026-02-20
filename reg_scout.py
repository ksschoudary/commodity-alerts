import requests
from bs4 import BeautifulSoup
import json

REG_KEYWORDS = ["fssai", "standard", "regulation", "framework", "order", "advisory", "compliance"]
COMMODITIES = ["Wheat", "Sugar", "Oil", "Atta", "Maida"]

def scrape_regulatory():
    # Scraping FSSAI Advisories page
    URL = "https://fssai.gov.in/cms/advisories.php"
    response = requests.get(URL, verify=False) # FSSAI often has SSL issues
    soup = BeautifulSoup(response.text, 'html.parser')
    
    reg_updates = []
    # Logic to find rows in FSSAI table
    for row in soup.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) > 1:
            title = cols[1].text.strip()
            if any(key.lower() in title.lower() for key in REG_KEYWORDS) or \
               any(com.lower() in title.lower() for com in COMMODITIES):
                reg_updates.append({
                    "title": title,
                    "url": cols[1].find('a')['href'] if cols[1].find('a') else "N/A",
                    "date": cols[0].text.strip()
                })

    with open('fssai_data.json', 'w') as f:
        json.dump(reg_updates, f, indent=4)

if __name__ == "__main__":
    scrape_regulatory()
