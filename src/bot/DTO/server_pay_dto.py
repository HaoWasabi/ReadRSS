from types import NotImplementedType
from .server_dto import ServerDTO

class ServerPayDTO:
    def __init__(self, server_dto: str, is_pay: bool):
        
        
        self.__server_dto = server_dto
        self.__is_pay = is_pay
    
    def __str__(self) -> str:
        return f"ChannelPayDTO(server={self.__server_dto}, is_pay={self.__is_pay})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ServerPayDTO):
            return NotImplementedType
        return self.__server_dto == other.__server_dto and self.__is_pay == other.__is_pay
    
    def set_server(self, channel_dto: str) -> None:
        self.__server_dto = channel_dto
        
    def set_pay(self, is_pay: bool) -> None:
        self.__is_pay = is_pay
        
    def get_server(self) -> str:
        return self.__server_dto
    
    def get_pay(self) -> bool:
        return self.__is_pay
    