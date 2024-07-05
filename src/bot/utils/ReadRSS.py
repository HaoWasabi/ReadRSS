import feedparser
from bs4 import BeautifulSoup
from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.EmtyDTO import EmtyDTO
from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.BLL.FeedBLL import FeedBLL
from bot.BLL.EmtyBLL import EmtyBLL
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL

def parse_html(content):
    if content is None:
        return None
    
    # Sử dụng BeautifulSoup để phân tích nội dung HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Lọc bỏ các thẻ HTML và chỉ lấy văn bản
    text = soup.get_text()
    return text

def ReadRSS(url):
    # Đọc dữ liệu từ URL RSS
    feed = feedparser.parse(url)
    print("\n__FEED__")
    print(f"Link: {feed.feed.link}")
    print(f"Link atom: {feed.feed.title_detail.base}")
    print(f"Title: {feed.feed.title}")
    print(f"Description: {feed.feed.description}")
    print(f"Logo: {feed.feed.image.url}")
    print(f"Updated: {feed.feed.updated}")
    
    feed_dto = FeedDTO(feed.feed.link, feed.feed.title_detail.base, feed.feed.title, feed.feed.description, feed.feed.image.url, feed.feed.updated)
    feed_bll = FeedBLL()
    feed_bll.insertFeed(feed_dto)
    
    # Kiểm tra nếu feed có dữ liệu
    print("\n__EMTY__")
    entry_bll = EmtyBLL()
    feed_entry_bll = FeedEmtyBLL()
    
    if feed.entries:
        for entry in feed.entries:
            if 'media_content' in entry: 
                media_content = entry.media_content[0]
            else: media_content = ""
            
            entry_dto = EmtyDTO(entry.link, entry.title, parse_html(entry.description), media_content, entry.published)
            entry_bll.insertEmty(entry_dto)
            
            feed_entry_dto = FeedEmtyDTO(feed_dto, entry_dto)
            feed_entry_bll.insertFeedEmty(feed_entry_dto)
            
        print(f"{len(feed.entries)} entries found in this feed.")
    else:
        print("No entries found in this feed.")
