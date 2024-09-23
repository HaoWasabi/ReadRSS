import feedparser
import cloudscraper
from bs4 import BeautifulSoup
from typing import Optional
from ..DTO.feed_dto import FeedDTO
from ..DTO.emty_dto import EmtyDTO
from ..utils.text_processor import TextProcessor

class GetRSS:
    def __init__(self, url: str):
        self.__rss_link = self.__fetch_rss_link(url)

    def __fetch_rss_link(self, url: str) -> Optional[str]:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rss_link = soup.find('link', attrs={'type': 'application/rss+xml'})
        return rss_link['href'] if rss_link else None # type: ignore

    def get_rss_link(self) -> Optional[str]:
        return self.__rss_link

def handle_url(url: str) -> str:
    
    return f"https://{url}" if "http://" not in url and "https://" not in url else url

def get_rss_link(url: str) -> Optional[str]:
    return GetRSS(handle_url(url)).get_rss_link()

def read_rss_link(url: Optional[str] = None, rss_link: Optional[str] = None) -> Optional[tuple[FeedDTO, EmtyDTO]]:
    if url:
        rss_link = get_rss_link(url)
    if not rss_link:
        raise ValueError("Either 'url' or 'rss_link' must be provided")

    feed = feedparser.parse(rss_link)
    logo_url = feed.feed.image.href if 'image' in feed.feed else ''
    description = feed.feed.description if hasattr(feed.feed, 'description') else ''
    feed_dto = FeedDTO(
        feed.feed.link,
        feed.feed.title_detail.base,
        feed.feed.title,
        description,
        logo_url,
        feed.feed.updated
    )
    
    if feed.entries:
        entry = feed.entries[0]
        media_content = ""
        if hasattr(entry, 'media_content') and entry.media_content:
            if  hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                media_content = entry.media_thumbnail[0]['url']
                
            else:    
                media_content = entry.media_content[0]['url']
                # Kiểm tra điều kiện bổ sung nếu cần thiết
                # if 'https://scontent-dus1-1.xx.fbcdn.net' in media_content:
                #     media_content = ""
                
        emty_dto = EmtyDTO(
            link_emty=entry.link,
            link_feed=feed_dto.link_feed,
            link_atom_feed=feed_dto.link_atom_feed,
            title_emty=entry.title,
            description_emty=str(TextProcessor.parse_html(entry.description)),
            image_emty=media_content,
            pubdate_emty=entry.published
        )
        return (feed_dto, emty_dto)