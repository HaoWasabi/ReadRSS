import feedparser
from bs4 import BeautifulSoup
from typing import Optional
from bot.dto.feed_dto import FeedDTO
from bot.dto.emty_dto import EmtyDTO
from bot.dto.feed_emty_dto import FeedEmtyDTO
from bot.bll.feed_bll import FeedBLL
from bot.bll.emty_bll import EmtyBLL
from bot.bll.feed_emty_bll import FeedEmtyBLL

def parse_html(content):
    if content is None:
        return None
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')
    
    # Strip away HTML tags and keep only the text
    text = soup.get_text()
    return text

class ReadRSS:
    def __init__(self, linkAtom_feed: str):
        self.__feed = feedparser.parse(linkAtom_feed)
        logo_url = self.__feed.feed.image.href if 'image' in self.__feed.feed else None
        feed_dto = FeedDTO(self.__feed.feed.link, self.__feed.feed.title_detail.base, self.__feed.feed.title, self.__feed.feed.description, logo_url, self.__feed.feed.updated)
        
        feed_bll = FeedBLL()
        feed_bll.insert_feed(feed_dto)
        
        entry_bll = EmtyBLL()
        feed_entry_bll = FeedEmtyBLL()
        if self.__feed.entries:
            media_content = ""
            for entry in reversed(self.__feed.entries):
                media_content = entry.media_content[0]['url']
                if 'media_content' in entry: 
                    if 'https://scontent-dus1-1.xx.fbcdn.net' not in media_content:
                        media_content = ""
                
                entry_dto = EmtyDTO(entry.link, entry.title, parse_html(entry.description), media_content, entry.published)
                entry_bll.insert_emty(entry_dto)
                
                feed_entry_dto = FeedEmtyDTO(feed_dto, entry_dto)
                feed_entry_bll.insert_feed_emty(feed_entry_dto)
                
            print(f"{len(self.__feed.entries)} entries found in this feed.")

    def get_link_first_entry(self) -> Optional[str]:
        if self.__feed is not None and self.__feed.entries:
            return self.__feed.entries[0].link
        print("No entries found in this feed.")
        return None
