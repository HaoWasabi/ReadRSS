from ..DTO.feed_emty_dto import FeedEmtyDTO
from ..DAL.feed_emty_dal import FeedEmtyDAL
from typing import Optional, List

class FeedEmtyBLL:
    def __init__(self):
        self.__FeedEmtyDAL = FeedEmtyDAL()
        
    def insert_feed_emty(self, feedEmty_dto: FeedEmtyDTO) -> bool:
        try:
            return self.__FeedEmtyDAL.insert_feed_emty(feedEmty_dto)
        except Exception as e:
            print(f"Error inserting FeedEmty: {e}")
            return False
    
    def delete_feed_emty_by_link_atom_feed_and_link_emty(self, feed_link: str, emty_link: str) -> bool:
        try:
            return self.__FeedEmtyDAL.delete_feed_emty_by_link_atom_feed_and_link_emty(feed_link, emty_link)
        except Exception as e:
            print(f"Error deleting FeedEmty: {e}")
            return False
            
    def delete_all_feed_emty(self) -> bool:
        try:
            return self.__FeedEmtyDAL.delete_all_feed_emty()
        except Exception as e:
            print(f"Error deleting FeedEmty: {e}")
            return False
    
    def get_feed_emty_by_link_atom_feed_and_link_emty(self, linkAtom_feed: str, link_emty: str) -> Optional[FeedEmtyDTO]:
        try:
            return self.__FeedEmtyDAL.get_feed_emty_by_link_atom_feed_and_link_emty(linkAtom_feed, link_emty)
        except Exception as e:
            print(f"Error fetching FeedEmty: {e}")
            
    def get_all_feed_emty(self) -> List[FeedEmtyDTO]:
        try:
            return self.__FeedEmtyDAL.get_all_feed_emty()
        except Exception as e:
            print(f"Error fetchting FeedEmty: {e}")
            return []