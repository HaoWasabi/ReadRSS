from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.EmtyDTO import EmtyDTO

class FeedEmtyDTO:
    def __init__(self, feed_dto: FeedDTO, emty_dto: EmtyDTO):
        self.__feed_dto = feed_dto
        self.__emty_dto = emty_dto

    def __str__(self) -> str:
        return f"FeedEmtyDTO(feed={self.__feed_dto}, emty={self.__emty_dto})"

    def setFeed(self, feed_dto: FeedDTO) -> None:
        self.__feed_dto = feed_dto
        
    def setEmty(self, emty_dto: EmtyDTO) -> None:
        self.__emty_dto = emty_dto
        
    def getFeed(self) -> FeedDTO:
        return self.__feed_dto
    
    def getEmty(self) -> EmtyDTO:
        return self.__emty_dto
    
    