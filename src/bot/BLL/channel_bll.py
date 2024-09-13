from ..DAL.channel_dal import ChannelDAL
from ..DTO.channel_dto import ChannelDTO
from typing import Optional, List

class ChannelBLL:
    def __init__(self):
        self.__channelDAL = ChannelDAL()
    
    def insert_channel(self, channel_dto: ChannelDTO) -> bool:
        return self.__channelDAL.insert_channel(channel_dto)

    def delete_channel_by_id_channel(self, channel_link: str) -> bool:
        return self.__channelDAL.delete_channel_by_id_channel(channel_link)
            
    def delete_all_channel(self) -> bool:
        return self.__channelDAL.delete_all_channel()

    def update_channel_by_id_channel(self, channel_link: str, Channel_dto: ChannelDTO) -> bool:
        return self.__channelDAL.update_channel_by_id_channel(channel_link, Channel_dto)
            
    def get_channel_by_id_channel(self, channel_link: str) -> Optional[ChannelDTO]:
        return self.__channelDAL.get_channel_by_id_channel(channel_link)
    def get_all_channel(self) -> List[ChannelDTO]:
        return self.__channelDAL.get_all_channel()
    