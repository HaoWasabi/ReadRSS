from types import NotImplementedType

from ..DTO.color_dto import ColorDTO

class ChannelDTO:
    def __init__(self, id_channel: str, id_server: str, name__channel: str, hex_color: str, is_active=True):
        self.__id_channel = id_channel
        self.__id_server = id_server
        self.__name_channel = name__channel
        self.__hex_color = hex_color
        self.__is_active = is_active
        
    def __str__(self) -> str:
        return f"ChannelDTO(id_channel={self.__id_channel}, id_server={self.__id_server}, name_channel={self.__name_channel}, hex_color={self.__hex_color}, is_active={self.__is_active})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChannelDTO):
            return NotImplementedType
        return self.__id_channel == other.__id_channel and self.__name_channel == other.__name_channel
    
    def set_id_channel(self, id_channel: str) -> None:
        self.__id_channel = id_channel
    
    def set_id_server(self, id_server: str) -> None:
        self.__id_server = id_server
        
    def set_name_channel(self, name_channel: str) -> None:
        self.__name_channel = name_channel
    
    def set_hex_color(self, hex_color: str) -> None:
        self.__hex_color = hex_color
        
    def set_state(self, is_active: bool) -> None:
        self.__is_active = is_active
        
    def get_id_channel(self) -> str:
        return self.__id_channel
    
    def get_id_server(self) -> str:
        return self.__id_server
    
    def get_name_channel(self) -> str:
        return self.__name_channel
    
    def get_hex_color(self) -> str:
        return self.__hex_color
    
    def get_state(self) -> bool:
        return self.__is_active