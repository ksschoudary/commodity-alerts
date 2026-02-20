import requests
from bs4 import BeautifulSoup
import json

KEYWORDS = ["standard", "order", "advisory", "circular", "framework", "compliance", "fssai"]
COMMODITIES = ["Wheat", "Sugar", "Oil", "Atta", "Maida", "Cereal", "Fortification"]

def scrape_regulatory():
    URL = "https://fssai.gov.in/cms/advisories.php"
    print("--- Starting Regulatory (FSSAI) Scan ---")
    
    try:
        # FSSAI often requires bypassing SSL verify in some environments
        response = requests.get(URL, timeout=20, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        reg_updates = []
        # FSSAI structure: Typically <table> -> <tr> -> <td>
        table = soup.find('table')
        if not table:
            print("No table found on FSSAI page.")
            return

        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                title = cols[1].text.strip()
                date = cols[0].text.strip()
                
                # If keyword OR commodity is mentioned
                if any(k.lower() in title.lower() for k in KEYWORDS) or \
                   any(c.lower() in title.lower() for c in COMMODITIES):
                    
                    link_tag = cols[1].find('a')
                    reg_updates.append({
                        "title": title,
                        "url": link_tag['href'] if link_tag else "https://fssai.gov.in",
                        "date": date,
                        "source": "FSSAI Official"
                    })
                    print(f"Found Reg: {title[:50]}...")

        with open('fssai_data.json', 'w') as f:
            json.dump(reg_updates, f, indent=4)
        print(f"Success: Saved {len(reg_updates)} Regulatory entries.")

    except Exception as e:
        print(f"Regulatory Error: {e}")

if __name__ == "__main__":
    scrape_regulatory()
