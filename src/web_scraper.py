from typing import Optional
import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, user_agent: str):
        self.headers = {'User-Agent': user_agent}
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None