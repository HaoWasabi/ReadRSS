from types import NotImplementedType

class ChannelDTO:
    def __init__(self, id_channel: str, name__channel: str):
        self.__id_channel = id_channel
        self.__name_channel = name__channel
        
    def __str__(self) -> str:
        return f"ChannelDTO(id_channel={self.__id_channel}, name_channel={self.__name_channel})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChannelDTO):
            return NotImplementedType
        return self.__id_channel == other.__id_channel and self.__name_channel == other.__name_channel
    
    def set_id_channel(self, id_channel: str) -> None:
        self.__id_channel = id_channel
    
    def set_name_channel(self, name_channel: str) -> None:
        self.__name_channel = name_channel
        
    def get_id_channel(self) -> str:
        return self.__id_channel
    
    def get_name_channel(self) -> str:
        return self.__name_channel  