from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.EmtyDTO import EmtyDTO

class ChannelEmtyDTO:
    def __init__(self, channel_dto: ChannelDTO, emty_dto: EmtyDTO):
        self.__channel_dto = channel_dto
        self.__emty_dto = emty_dto
    
    def __str__(self) -> str:
        return f"ChannelEmtyDTO(channel={self.__channel_dto}, emty={self.__emty_dto})"
    
    def setChannel(self, channel_dto: ChannelDTO) -> None:
        self.__channel_dto = channel_dto
        
    def setEmty(self, emty_dto: EmtyDTO) -> None:
        self.__emty_dto = emty_dto
        
    def getChannel(self) -> ChannelDTO:
        return self.__channel_dto
    
    def getEmty(self) -> EmtyDTO:
        return self.__emty_dto
    