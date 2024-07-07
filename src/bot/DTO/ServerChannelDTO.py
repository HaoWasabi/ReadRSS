from bot.DTO.ServerDTO import ServerDTO
from bot.DTO.ChannelDTO import ChannelDTO

class ServerChannelDTO:
    def __init__(self, server_dto: ServerDTO, channel_dto: ChannelDTO):
        self.__server_dto = server_dto
        self.__channel_dto = channel_dto
        
    def __str__(self) -> str:
        return f"ServerChannelDTO(server_dto={self.__server_dto}, channel_dto={self.__channel_dto})"
    
    def setServer(self, server_dto: ServerDTO) -> None:
        self.__server_dto = server_dto
        
    def setChannel(self, channel_dto: ChannelDTO) -> None:
        self.__channel_dto = channel_dto
    
    def getServer(self) -> ServerDTO:
        return self.__server_dto
    
    def getChannel(self) -> ChannelDTO:
        return self.__channel_dto