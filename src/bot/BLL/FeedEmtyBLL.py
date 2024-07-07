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
    
    def deleteFeedEmtyByLinkAtom_feedAndLink_emty(self, feed_link: str, emty_link: str) -> bool:
        try:
            return self.__FeedEmtyDAL.deleteFeedEmtyByLinkAtom_feedAndLink_emty(feed_link, emty_link)
        except Exception as e:
            print(f"Error deleting FeedEmty: {e}")
            
    def deleteAllFeedEmty(self) -> bool:
        try:
            return self.__FeedEmtyDAL.deleteAllFeedEmty()
        except Exception as e:
            print(f"Error deleting FeedEmty: {e}")
            
    def updateFeedEmtyByLinkAtom_feedAndLink_emty(self, feed_linkAtom: str, emty_link: str, feedEmty_dto: FeedEmtyDTO) -> bool:
        try:
            return self.__FeedEmtyDAL.updateFeedEmtyByLinkAtom_feedAndLink_emty(feed_linkAtom, emty_link, feedEmty_dto)
        except Exception as e:
            print(f"Error updating FeedEmty: {e}")
    

    def getFeedEmtyByLinkAtom_feedAndLink_emty(self, linkAtom_feed: str, link_emty: str) -> Optional[FeedEmtyDTO]:
        try:
            return self.__FeedEmtyDAL.getFeedEmtyByLinkAtom_feedAndLink_emty(linkAtom_feed, link_emty)
        except Exception as e:
            print(f"Error fetching FeedEmty: {e}")
            
    def getFeedEmtyByLinkAtom_feed(self, feed_link: str) -> Optional[FeedEmtyDTO]:
        try:
            return self.__FeedEmtyDAL.getFeedEmtyByLinkAtom_feed(feed_link)
        except Exception as e:
            print(f"Error fetching FeedEmty: {e}")
            
    def getAllFeedEmty(self) -> List[FeedEmtyDTO]:
        try:
            return self.__FeedEmtyDAL.getAllFeedEmty()
        except Exception as e:
            print(f"Error fetchting FeedEmty: {e}")