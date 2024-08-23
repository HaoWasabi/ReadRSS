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
        
        emty_bll = EmtyBLL()
        feed_emty_bll = FeedEmtyBLL()
        if self.__feed.entries:
            media_content = ""
            for emty in reversed(self.__feed.entries):
                media_content = emty.media_content[0]['url']
                # if 'media_content' in emty: 
                #     if 'https://scontent-dus1-1.xx.fbcdn.net' not in media_content:
                #         media_content = ""
                
                emty_dto = EmtyDTO(emty.link, emty.title, parse_html(emty.description), media_content, emty.published)
                emty_bll.insert_emty(emty_dto)
                
                feed_emty_dto = FeedEmtyDTO(feed_dto, emty_dto)
                feed_emty_bll.insert_feed_emty(feed_emty_dto)

    def get_link_first_entry(self) -> Optional[str]:
        if self.__feed is not None and self.__feed.entries:
            return self.__feed.entries[0].link
        return None
