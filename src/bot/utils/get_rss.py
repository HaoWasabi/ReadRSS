from bs4 import BeautifulSoup
from typing import Optional
import requests

class GetRSS:
    def __init__(self, url: str):
        self.__url = url  # Keep the original URL
        response = requests.get(self.__url)  # Fetch the content of the URL
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the RSS link in the HTML content
        rss_link = soup.find('link', attrs={'type': 'application/rss+xml'})
        if rss_link:
            self.__rss_link = rss_link.get('href')  # type: ignore
        else:
            self.__rss_link = None

    def get_rss_link(self) -> Optional[str]:
        return str(self.__rss_link) if self.__rss_link else None
