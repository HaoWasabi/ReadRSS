from bot.DAL.FeedDAL import FeedDAL

class FeedBLL:
    def __init__(self):
        self.FeedDAL = FeedDAL()

    def insertFeed(self, feed_dto):
        return self.FeedDAL.insertFeed(feed_dto)
    
    def deleteFeedByLink_feed(self, feed_link):
        return self.FeedDAL.deleteFeedByLink_feed(feed_link)

    def deleteFeedByLinkAtom_feed(self, linkAtom_feed):
        return self.FeedDAL.deleteFeedByLinkAtom_feed(linkAtom_feed)

    def deleteFeedByTitle_feed(self, title_feed):
        return self.FeedDAL.deleteFeedByTitle_feed(title_feed)
    
    def deleteAllFeed(self):
        return self.FeedDAL.deleteAllFeed()

    def updateFeedByLink_feed(self, feed_link, feed_dto):
        return self.FeedDAL.updateFeedByLink_feed(feed_link, feed_dto)
    
    def updateFeedByLinkAtom_feed(self, linkAtom_feed, feed_dto):
        return self.FeedDAL.updateFeedByLinkAtom_feed(linkAtom_feed, feed_dto)

    def updateFeedByTitle_feed(self, title_feed, feed_dto):
        return self.FeedDAL.updateFeedByTitle_feed(title_feed, feed_dto)
    
    def getFeedByLink_feed(self, feed_link):
        return self.FeedDAL.getFeedByLink_feed(feed_link)

    def getFeedByLinkAtom_feed(self, linkAtom_feed):
        return self.FeedDAL.getFeedByLinkAtom_feed(linkAtom_feed)
    
    def getFeedByTitle_feed(self, title_feed):
        return self.FeedDAL.getFeedByTitle_feed(title_feed)
    
    def getAllFeed(self):
        return self.FeedDAL.getAllFeed()