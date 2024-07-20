import feedparser
from bs4 import BeautifulSoup
from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.EmtyDTO import EmtyDTO
from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.BLL.FeedBLL import FeedBLL
from bot.BLL.EmtyBLL import EmtyBLL
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL
from typing import Optional
import re

def parse_html(content):
    if content is None:
        return None
    
    # Sử dụng BeautifulSoup để phân tích nội dung HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Lọc bỏ các thẻ HTML và chỉ lấy văn bản
    text = soup.get_text()
    return text

class ReadRSS:
    def __init__(self, linkAtom_feed: str):
        # Đọc dữ liệu từ URL RSS
        self.__feed = feedparser.parse(linkAtom_feed)
        logo_url = self.__feed.feed.image.url if hasattr(self.__feed.feed.image, 'url') else None
        print(f'''\n__FEED__
        Link: {self.__feed.feed.link}.
        Link atom: {self.__feed.feed.title_detail.base}
        Title: {self.__feed.feed.title}
        Description_entry: {self.__feed.feed.description}
        Logo: {logo_url}
        Updated: {self.__feed.feed.updated}''')
        
        feed_dto = FeedDTO(self.__feed.feed.link, self.__feed.feed.title_detail.base, self.__feed.feed.title, self.__feed.feed.description, logo_url, self.__feed.feed.updated)
        feed_bll = FeedBLL()
        feed_bll.insertFeed(feed_dto)
        
        # Kiểm tra nếu feed có dữ liệu
        print("\n__EMTY__")
        entry_bll = EmtyBLL()
        feed_entry_bll = FeedEmtyBLL()
        
        if self.__feed.entries:
            media_content = ""
            for entry in self.__feed.entries:
                # media_content = entry.media_content[0]['url']
                # print("media_content: " + media_content)
                # if 'media_content' in entry: 
                #     if 'https://scontent-dus1-1.xx.fbcdn.net' not in media_content:
                        # media_content = ""
                
                entry_dto = EmtyDTO(entry.link, entry.title, parse_html(entry.description), media_content, entry.published)
                entry_bll.insertEmty(entry_dto)
                
                feed_entry_dto = FeedEmtyDTO(feed_dto, entry_dto)
                feed_entry_bll.insertFeedEmty(feed_entry_dto)
                
            print(f"{len(self.__feed.entries)} entries found in this feed.")

    def getLink_firstEntry(self) -> Optional[str]:
        if self.__feed is not None and self.__feed.entries:
            return self.__feed.entries[0].link
        print("No entries found in this feed.")
        return None