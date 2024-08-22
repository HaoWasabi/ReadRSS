from bot.dto.server_dto import ServerDTO
from bot.dto.color_dto import ColorDTO

class ServerColorDTO:
    def __init__(self, server_dto: ServerDTO, color_dto: ColorDTO):
        self.__server_dto = server_dto
        self.__color_dto = color_dto
    
    def __str__(self) -> str:
        return f"ServerColorDTO(server={self.__server_dto}, color={self.__color_dto})"
    
    def __eq__(self, other: object) -> bool:
        return self.__server_dto == other.__server_dto and self.__color_dto == other.__color_dto
    
    def set_server(self, server_dto: ServerDTO) -> None:
        self.__server_dto = server_dto
        
    def set_color(self, color_dto: ColorDTO) -> None:
        self.__color_dto = color_dto
        
    def get_server(self) -> ServerDTO:
        return self.__server_dto
    
    def get_color(self) -> ColorDTO:
        return self.__color_dto
