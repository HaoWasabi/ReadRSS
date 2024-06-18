from bot.DAL.FeedEmtyDAL import FeedEmtyDAL

class FeedEmtyBLL:
    def __init__(self):
        self.__FeedEmtyDAL = FeedEmtyDAL()
        
    def insertFeedEmty(self, feedEmty_dto):
        try:
            return self.__FeedEmtyDAL.insertFeedEmty(feedEmty_dto)
        except Exception as e:
            print(f"Error inserting FeedEmty: {e}")
    
    def deleteFeedEmtyByLink_feed(self, feed_link):
        try:
            return self.__FeedEmtyDAL.deleteFeedEmtyByLink_feed(feed_link)
        except Exception as e:
            print(f"Error deleting FeedEmty: {e}")
    
    def deleteFeedEmtyByLink_emty(self, emty_link):
        try:
            return self.__FeedEmtyDAL.deleteFeedEmtyByLink_emty(emty_link)
        except Exception as e:
            print(f"Error deleting FeedEmty: {e}")
            
    def deleteAllFeedEmty(self):
        try:
            return self.__FeedEmtyDAL.deleteAllFeedEmty()
        except Exception as e:
            print(f"Error deleting FeedEmty: {e}")
            
    def updateFeedEmtyByLink_feed(self, feed_link, feedEmty_dto):
        try:
            return self.__FeedEmtyDAL.updateFeedEmtyByLink_feed(feed_link, feedEmty_dto)
        except Exception as e:
            print(f"Error updating FeedEmty: {e}")
               
    def updateFeedEmtyByLink_emty(self, emty_link, feedEmty_dto):
        try:
            return self.__FeedEmtyDAL.updateFeedEmtyByLink_emty(emty_link, feedEmty_dto)
        except Exception as e:
            print(f"Error updating FeedEmty: {e}")    
    
    def getFeedEmtyByLink_feed(self, feed_link):
        try:
            return self.__FeedEmtyDAL.getFeedEmtyByLink_feed(feed_link)
        except Exception as e:
            print(f"Error fetching FeedEmty: {e}")
               
    def getFeedEmtyByLink_emty(self, emty_link):
        try:
            return self.__FeedEmtyDAL.getFeedEmtyByLink_emty(emty_link)
        except Exception as e:
            print(f"Error fetching FeedEmty: {e}")
            
    def getAllFeedEmty(self):
        try:
            return self.__FeedEmtyDAL.getAllFeedEmty()
        except Exception as e:
            print(f"Error fetchting FeedEmty: {e}")