from ..DTO.feed_dto import FeedDTO
from ..DTO.emty_dto import EmtyDTO
from types import NotImplementedType
class FeedEmtyDTO:
    def __init__(self, feed_dto: FeedDTO, emty_dto: EmtyDTO):
        self.__feed_dto = feed_dto
        self.__emty_dto = emty_dto

    def __str__(self) -> str:
        return f"FeedEmtyDTO(feed={self.__feed_dto}, emty={self.__emty_dto})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FeedEmtyDTO):
            return NotImplementedType
        return self.__feed_dto == other.__feed_dto and self.__emty_dto == other.__emty_dto
    
    def set_feed(self, feed_dto: FeedDTO) -> None:
        self.__feed_dto = feed_dto
        
    def set_emty(self, emty_dto: EmtyDTO) -> None:
        self.__emty_dto = emty_dto
        
    def get_feed(self) -> FeedDTO:
        return self.__feed_dto
    
    def get_emty(self) -> EmtyDTO:
        return self.__emty_dto
    
    