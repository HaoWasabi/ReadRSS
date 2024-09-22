
from ..BLL.singleton import Singleton
from ..DTO.channel_emty_dto import ChannelEmtyDTO
from ..DAL.channel_emty_dal import ChannelEmtyDAL
from typing import Optional, List


class ChannelEmtyBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__channelEmtyDAL = ChannelEmtyDAL()
            self._initialized = True
            
    def insert_channel_emty(self, channel_emty_dto: ChannelEmtyDTO):
        return self.__channelEmtyDAL.insert_channel_emty(channel_emty_dto)
    
    def delete_channel_emty_by_channel_id(self, channel_id: str):
        return self.__channelEmtyDAL.delete_channel_emty_by_channel_id(channel_id)
    
    def delete_all_channel_emty(self):
        return self.__channelEmtyDAL.delete_all_channel_emty()
    
    def get_all_channel_emty(self):
        return self.__channelEmtyDAL.get_all_channel_emty()
    
    def get_all_channel_emty_by_channel_id(self, channel_id: str):
        return self.__channelEmtyDAL.get_all_channel_emty_by_channel_id(channel_id)
    
    def get_channel_emty_by_channel_id_and_link_emty(self, channel_id: str, link_emty: str):
        return self.__channelEmtyDAL.get_channel_emty_by_channel_id_and_link_emty(channel_id, link_emty)