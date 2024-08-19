from bot.dto.server_dto import ServerDTO
from bot.dto.channel_dto import ChannelDTO

class ServerChannelDTO:
    def __init__(self, server_dto: ServerDTO, channel_dto: ChannelDTO):
        self.__server_dto = server_dto
        self.__channel_dto = channel_dto
        
    def __str__(self) -> str:
        return f"ServerChannelDTO(server_dto={self.__server_dto}, channel_dto={self.__channel_dto})"
    
    def __eq__(self, other: object) -> bool:
        return self.__server_dto == other.__server_dto and self.__channel_dto == other.__channel_dto
    
    def set_server(self, server_dto: ServerDTO) -> None:
        self.__server_dto = server_dto
        
    def set_channel(self, channel_dto: ChannelDTO) -> None:
        self.__channel_dto = channel_dto
    
    def get_server(self) -> ServerDTO:
        return self.__server_dto
    
    def get_channel(self) -> ChannelDTO:
        return self.__channel_dto