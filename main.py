"""
Web scraper developed to extract FIFA World Cup final data from Wikipedia.
Objective: Demonstrate proficiency with Beautiful Soup and Pandas for data extraction and export.
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

class Scraper:
    def __init__(self):
        self.data = []

    def extract_data(self):
        """Fetches and parses world cup finals data from Wikipedia."""
        url = 'https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate the main table containing the finals data
        table = soup.find('table', class_="sortable")
        # Skip the header row (index 0) and iterate through data rows
        rows = table.find_all('tr')[1:] 

        for row in rows:
            cols = row.find_all(['td', 'th'])

            if len(cols) >= 5:
                # Extract and clean text content from columns
                final_data = {
                    'year': cols[0].get_text(strip=True),
                    'winner': cols[1].get_text(strip=True),
                    'score': cols[2].get_text(strip=True),
                    'runners-up': cols[3].get_text(strip=True),
                    'attendance': cols[4].get_text(strip=True)
                }
                self.data.append(final_data)
  
    def save_data(self, base_name='world_cup_finals'):
        """Exports the collected data to CSV and XLSX formats."""
        df = pd.DataFrame(self.data)
        
        # Export to Excel and CSV
        df.to_excel(f'{base_name}.xlsx', index=False)
        df.to_csv(f'{base_name}.csv', index=False, encoding='utf-8-sig', sep=';')
        print(f"Data successfully saved as {base_name}.xlsx and {base_name}.csv")

if __name__ == "__main__":
    # Execution entry point
    scraper = Scraper()
    scraper.extract_data()
    scraper.save_data()
