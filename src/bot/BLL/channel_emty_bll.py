from ..DTO.channel_emty_dto import ChannelEmtyDTO
from ..DAL.channel_emty_dal import ChannelEmtyDAL
from typing import Optional, List

class ChannelEmtyBLL:
    def __init__(self):
        self.__channelEmtyDAL = ChannelEmtyDAL()
        
    def insert_channel_emty(self, channel_emty_dto: ChannelEmtyDTO) -> bool:
        return self.__channelEmtyDAL.insert_channel_emty(channel_emty_dto)

    
    def delete_channel_emty_by_id_channel(self, id_channel: str) -> bool:  
        return self.__channelEmtyDAL.delete_channel_emty_by_id_channel(id_channel)

            
    def delete_channel_emty_by_id_channel_and_link_emty(self, id_channel: str, link_emty: str) -> bool:
        return self.__channelEmtyDAL.delete_channel_emty_by_id_channel_and_link_emty(id_channel, link_emty)

            
    def delete_all_channel_emty(self) -> bool:
        return self.__channelEmtyDAL.delete_all_channel_emty()

    
    def get_channel_emty_by_id_channel_and_link_emty(self, id_channel: str, link_emty: str) -> Optional[ChannelEmtyDTO]:
        return self.__channelEmtyDAL.get_channel_emty_by_id_channel_and_link_emty(id_channel, link_emty)

    def get_all_channel_emty(self) -> List[ChannelEmtyDTO]:
        return self.__channelEmtyDAL.get_all_channel_emty()

        
    def get_all_channel_emty_by_id_channel(self, id_channel: str) -> List[ChannelEmtyDTO]:
        return self.__channelEmtyDAL.get_all_channel_emty_by_id_channel(id_channel)
