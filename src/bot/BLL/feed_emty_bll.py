from ..DTO.feed_emty_dto import FeedEmtyDTO
from ..DAL.feed_emty_dal import FeedEmtyDAL
from typing import Optional, List

class FeedEmtyBLL:
    def __init__(self):
        self.__FeedEmtyDAL = FeedEmtyDAL()
        
    def insert_feed_emty(self, feedEmty_dto: FeedEmtyDTO) -> bool:
        return self.__FeedEmtyDAL.insert_feed_emty(feedEmty_dto)

    
    def delete_feed_emty_by_link_atom_feed_and_link_emty(self, feed_link: str, emty_link: str) -> bool:
        return self.__FeedEmtyDAL.delete_feed_emty_by_link_atom_feed_and_link_emty(feed_link, emty_link)

        
    def delete_feed_emty_by_link_feed_and_link_emty(self, feed_link: str, emty_link: str) -> bool:
        return self.__FeedEmtyDAL.delete_feed_emty_by_link_feed_and_link_emty(feed_link, emty_link)

            
    def delete_feed_emty_by_link_feed(self, link_feed: str) -> bool:
        return self.__FeedEmtyDAL.delete_feed_emty_by_link_feed(link_feed)

        
    def delete_all_feed_emty(self) -> bool:
        return self.__FeedEmtyDAL.delete_all_feed_emty()

    
    def get_feed_emty_by_link_atom_feed_and_link_emty(self, linkAtom_feed: str, link_emty: str) -> Optional[FeedEmtyDTO]:
        return self.__FeedEmtyDAL.get_feed_emty_by_link_atom_feed_and_link_emty(linkAtom_feed, link_emty)

    def get_all_feed_emty_by_link_atom_feed(self, link_atom_feed: str) -> List[FeedEmtyDTO]:
        return self.__FeedEmtyDAL.get_all_feed_emty_by_link_atom_feed(link_atom_feed)

    
    def get_all_feed_emty_by_link_feed(self, link_feed: str) -> List[FeedEmtyDTO]:
        return self.__FeedEmtyDAL.get_all_feed_emty_by_link_feed(link_feed)

            
    def get_all_feed_emty(self) -> List[FeedEmtyDTO]:
        return self.__FeedEmtyDAL.get_all_feed_emty()