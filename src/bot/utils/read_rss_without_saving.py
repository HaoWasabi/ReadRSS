import feedparser
from typing import Optional
from ..DTO.feed_dto import FeedDTO
from ..DTO.emty_dto import EmtyDTO
from ..DTO.feed_emty_dto import FeedEmtyDTO
from ..utils.text_processor import TextProcessor


class ReadRSSWithoutSaving:
    def __init__(self, linkAtom_feed: str):
        self.__feed = feedparser.parse(linkAtom_feed)
        logo_url = self.__feed.feed.image.href if 'image' in self.__feed.feed else ''
        self.__feed_dto = FeedDTO(self.__feed.feed.link, self.__feed.feed.title_detail.base, self.__feed.feed.title, self.__feed.feed.description, logo_url, self.__feed.feed.updated) # type: ignore
        
        if self.__feed.entries:
            emty = self.__feed.entries[0]
            media_content = emty.media_content[0]['url']
            # if 'media_content' in emty: 
            #     if 'https://scontent-dus1-1.xx.fbcdn.net' not in media_content:
            #         media_content = ""
            self.__emty_dto = EmtyDTO(emty.link, emty.title, TextProcessor.parse_html(emty.description), media_content, emty.published) # type: ignore
            self.__feed_emty_dto = FeedEmtyDTO(self.__feed_dto, self.__emty_dto)

    def get_first_feed_emty(self) -> Optional[FeedEmtyDTO]:
        if self.__feed is not None and self.__feed.entries:
            return self.__feed_emty_dto
        return None
        
    