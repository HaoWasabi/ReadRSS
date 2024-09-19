from datetime import datetime
from ..DTO.channel_dto import ChannelDTO
from ..DTO.user_dto import UserDTO


class UserChannelDTO:
    def __init__(self, user: UserDTO, channel: ChannelDTO, date: datetime):
        self.__user = user
        self.__channel = channel
        self.__date = date
        
    def __str__(self) -> str:
        return f"UserChannelDTO({self.__user}, {self.__channel}, {self.__date})"
    
    def set_user(self, user: UserDTO) -> None:
        self.__user = user
        
    def set_channel(self, channel: ChannelDTO) -> None:
        self.__channel = channel
    
    def set_date(self, date: datetime) -> None:
        self.__date = date
        
    def get_user(self) -> UserDTO:
        return self.__user
    
    def get_channel(self) -> ChannelDTO:
        return self.__channel
    
    def get_date(self) -> datetime:
        return self.__date
        