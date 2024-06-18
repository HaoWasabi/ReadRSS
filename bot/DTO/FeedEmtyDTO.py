class FeedEmtyDTO:
    
    def __init__(self, feed_dto, emty_dto):
        self.__feed_dto = feed_dto
        self.__emty_dto = emty_dto

    def __str__(self):
        return f"FeedEmtyDTO(feed={self.__feed_dto}, emty={self.__emty_dto})"

    def setFeed(self, feed_dto):
        self.__feed_dto = feed_dto
        
    def setEmty(self, emty_dto):
        self.__emty_dto = emty_dto
        
    def getFeed(self):
        return self.__feed_dto
    
    def getEmty(self):
        return self.__emty_dto
    
print(FeedEmtyDTO("a", "a"))
    