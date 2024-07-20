from bot.DTO.FeedDTO import FeedDTO
from bot.DAL.FeedDAL import FeedDAL
from typing import Optional, List

class FeedBLL:
    def __init__(self):
        self.__FeedDAL = FeedDAL()

    def insertFeed(self, feed_dto: FeedDTO) -> bool:
        try:
            return self.__FeedDAL.insertFeed(feed_dto)
        except Exception as e:
            print(f"Error inserting Feed: {e}")
    
    def deleteFeedByLink_feed(self, feed_link: str) -> bool:
        try:
            return self.__FeedDAL.deleteFeedByLink_feed(feed_link)
        except Exception as e:
            print(f"Error deleting Feed: {e}")

    def deleteFeedByLinkAtom_feed(self, linkAtom_feed: str) -> bool:
        try:
            return self.__FeedDAL.deleteFeedByLinkAtom_feed(linkAtom_feed)
        except Exception as e:
            print(f"Error deleting Feed: {e}")

    def deleteFeedByTitle_feed(self, title_feed: str) -> bool:
        try:
            return self.__FeedDAL.deleteFeedByTitle_feed(title_feed)
        except Exception as e:
            print(f"Error deleting Feed: {e}")
    
    def deleteAllFeed(self) -> bool:
        try:
            return self.__FeedDAL.deleteAllFeed()
        except Exception as e:
            print(f"Error deleting Feed: {e}")

    def updateFeedByLink_feed(self, feed_link: str, feed_dto: FeedDTO) -> bool:
        try:
            return self.__FeedDAL.updateFeedByLink_feed(feed_link, feed_dto)
        except Exception as e:
            print(f"Error updating Feed: {e}")
    
    def updateFeedByLinkAtom_feed(self, linkAtom_feed: str, feed_dto: FeedDTO) -> bool:
        try:
            return self.__FeedDAL.updateFeedByLinkAtom_feed(linkAtom_feed, feed_dto)
        except Exception as e:
            print(f"Error updating Feed: {e}")
            
    def updateFeedByTitle_feed(self, title_feed: str, feed_dto: FeedDTO) -> bool:
        try:
            return self.__FeedDAL.updateFeedByTitle_feed(title_feed, feed_dto)
        except Exception as e:
            print(f"Error updating Feed: {e}")
            
    def getFeedByLink_feed(self, feed_link: str) -> Optional[FeedDTO]:
        try:
            return self.__FeedDAL.getFeedByLink_feed(feed_link)
        except Exception as e:
            print(f"Error fetching Feed: {e}")
            
    def getFeedByLinkAtom_feed(self, linkAtom_feed: str) -> Optional[FeedDTO]:
        try:
            return self.__FeedDAL.getFeedByLinkAtom_feed(linkAtom_feed)
        except Exception as e:
            print(f"Error fetching Feed: {e}")
            
    def getFeedByTitle_feed(self, title_feed: str) -> Optional[FeedDTO]:
        try:
            return self.__FeedDAL.getFeedByTitle_feed(title_feed)
        except Exception as e:
            print(f"Error fetching Feed: {e}")
            
    def getAllFeed(self) -> List[FeedDTO]:
        try:
            return self.__FeedDAL.getAllFeed()
        except Exception as e:
            print(f"Error fetching Feed: {e}")