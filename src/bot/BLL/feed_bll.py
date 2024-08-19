from bot.dto.feed_dto import FeedDTO
from bot.dal.feed_dal import FeedDAL
from typing import Optional, List

class FeedBLL:
    def __init__(self):
        self.__FeedDAL = FeedDAL()

    def insert_feed(self, feed_dto: FeedDTO) -> bool:
        try:
            return self.__FeedDAL.insert_feed(feed_dto)
        except Exception as e:
            print(f"Error inserting Feed: {e}")

    def delete_feed_by_link_atom_feed(self, linkAtom_feed: str) -> bool:
        try:
            return self.__FeedDAL.delete_feed_by_link_atom_feed(linkAtom_feed)
        except Exception as e:
            print(f"Error deleting Feed: {e}")
    
    def delete_all_feed(self) -> bool:
        try:
            return self.__FeedDAL.delete_all_feed()
        except Exception as e:
            print(f"Error deleting Feed: {e}")
    
    def update_feed_by_link_atom_feed(self, linkAtom_feed: str, feed_dto: FeedDTO) -> bool:
        try:
            return self.__FeedDAL.update_feed_by_link_atom_feed(linkAtom_feed, feed_dto)
        except Exception as e:
            print(f"Error updating Feed: {e}")
            
    def get_feed_by_link_atom_feed(self, linkAtom_feed: str) -> Optional[FeedDTO]:
        try:
            return self.__FeedDAL.get_feed_by_link_atom_feed(linkAtom_feed)
        except Exception as e:
            print(f"Error fetching Feed: {e}")
            
    def get_all_feed(self) -> List[FeedDTO]:
        try:
            return self.__FeedDAL.get_all_feed()
        except Exception as e:
            print(f"Error fetching Feed: {e}")