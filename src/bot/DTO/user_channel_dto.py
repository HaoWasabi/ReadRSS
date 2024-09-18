from ..DTO.channel_dto import ChannelDTO
from ..DTO.user_dto import UserDTO


class UserChannelDTO:
    def __init__(self, user: UserDTO, channel: ChannelDTO):
        self.__user = user
        self.__channel = channel
        
    def __str__(self) -> str:
        return f"UserChannelDTO(user={self.__user}, channel={self.__channel})"
    
    def set_user(self, user: UserDTO) -> None:
        self.__user = user
        
    def set_channel(self, channel: ChannelDTO) -> None:
        self.__channel = channel
    
    def get_user(self) -> UserDTO:
        return self.__user
    
    def get_channel(self) -> ChannelDTO:
        return self.__channel
    