from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.DAL.FeedEmtyDAL import FeedEmtyDAL
from typing import Optional, List

class FeedEmtyBLL:
    def __init__(self):
        self.__FeedEmtyDAL = FeedEmtyDAL()
        
    def insertFeedEmty(self, feedEmty_dto: FeedEmtyDTO) -> bool:
        try:
            return self.__FeedEmtyDAL.insertFeedEmty(feedEmty_dto)
        except Exception as e:
            print(f"Error inserting FeedEmty: {e}")
    
    def deleteFeedEmtyByLink_feedAndLink_emty(self, feed_link: str, emty_link: str) -> bool:
        try:
            return self.__FeedEmtyDAL.deleteFeedEmtyByLink_feedAndLink_emty(feed_link, emty_link)
        except Exception as e:
            print(f"Error deleting FeedEmty: {e}")
            
    def deleteAllFeedEmty(self) -> bool:
        try:
            return self.__FeedEmtyDAL.deleteAllFeedEmty()
        except Exception as e:
            print(f"Error deleting FeedEmty: {e}")
            
    def updateFeedEmtyByLink_feedAndLink_emty(self, feed_link: str, emty_link: str, feedEmty_dto: FeedEmtyDTO) -> bool:
        try:
            return self.__FeedEmtyDAL.updateFeedEmtyByLink_feedAndLink_emty(feed_link, emty_link, feedEmty_dto)
        except Exception as e:
            print(f"Error updating FeedEmty: {e}")
    
    def getFeedEmtyByLink_feedAndLink_emty(self, feed_link: str, emty_link: str) -> Optional[FeedEmtyDTO]:
        try:
            return self.__FeedEmtyDAL.getFeedEmtyByLink_feedAndLink_emty(feed_link, emty_link)
        except Exception as e:
            print(f"Error fetching FeedEmty: {e}")
            
    def getAllFeedEmty(self) -> List[FeedEmtyDTO]:
        try:
            return self.__FeedEmtyDAL.getAllFeedEmty()
        except Exception as e:
            print(f"Error fetchting FeedEmty: {e}")