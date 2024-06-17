from bot.DAL.FeedEmtyDAL import FeedEmtyDAL

class FeedEmtyBLL:
    def __init__(self):
        self.FeedEmtyDAL = FeedEmtyDAL()
        
    def insertFeedEmty(self, feedEmty_dto):
        return self.FeedEmtyDAL.insertFeedEmty(feedEmty_dto)
    
    def deleteFeedEmtyByLink_feed(self, feed_link):
        return self.FeedEmtyDAL.deleteFeedEmtyByLink_feed(feed_link)
    
    def deleteFeedEmtyByLink_emty(self, emty_link):
        return self.FeedEmtyDAL.deleteFeedEmtyByLink_emty(emty_link)
    
    def deleteAllFeedEmty(self):
        return self.FeedEmtyDAL.deleteAllFeedEmty()
    
    def updateFeedEmtyByLink_feed(self, feed_link, feedEmty_dto):
        return self.FeedEmtyDAL.updateFeedEmtyByLink_feed(feed_link, feedEmty_dto)
    
    def updateFeedEmtyByLink_emty(self, emty_link, feedEmty_dto):
        return self.FeedEmtyDAL.updateFeedEmtyByLink_emty(emty_link, feedEmty_dto)
    
    def getFeedEmtyByLink_feed(self, feed_link):
        return self.FeedEmtyDAL.getFeedEmtyByLink_feed(feed_link)
    
    def getFeedEmtyByLink_emty(self, emty_link):
        return self.FeedEmtyDAL.getFeedEmtyByLink_emty(emty_link)
    
    def getAllFeedEmty(self):
        return self.FeedEmtyDAL.getAllFeedEmty()