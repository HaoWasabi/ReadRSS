from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.EmtyDTO import EmtyDTO

class FeedEmtyDTO:
    
    def __init__(self, feed_dto, emty_dto):
        self.feed_dto = feed_dto
        self.emty_dto = emty_dto

    def __str__(self):
        return f"FeedEmtyDTO(feed={self.feed_dto}, emty={self.emty_dto})"

    def setFeed(self, feed_dto):
        self.feed_dto = feed_dto
        
    def setEmty(self, emty_dto):
        self.emty_dto = emty_dto
        
    def getFeed(self):
        return self.feed_dto
    
    def getEmty(self):
        return self.emty_dto