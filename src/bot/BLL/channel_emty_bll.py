from bot.dto.channel_emty_dto import ChannelEmtyDTO
from bot.dal.channel_emty_dal import ChannelEmtyDAL
from typing import Optional, List

class ChannelEmtyBLL:
    def __init__(self):
        self.__channelEmtyDAL = ChannelEmtyDAL()
        
    def insert_channel_emty(self, channel_emty_dto: ChannelEmtyDTO) -> bool:
        try:
            return self.__channelEmtyDAL.insert_channel_emty(channel_emty_dto)
        except Exception as e:
            print(f"Error inserting ChannelEmty: {e}")
    
    def delete_channel_emty_by_id_channel(self, id_channel: str) -> bool:  
        try:
            return self.__channelEmtyDAL.delete_channel_emty_by_id_channel(id_channel)
        except Exception as e:
            print(f"Error deleting ChannelEmty: {e}")
            
    def delete_channel_emty_by_id_channel_and_link_emty(self, id_channel: str, link_emty: str) -> bool:
        try:
            return self.__channelEmtyDAL.delete_channel_emty_by_id_channel_and_link_emty(id_channel, link_emty)
        except Exception as e:
            print(f"Error deleting ChannelEmty: {e}")
            
    def delete_all_channel_emty(self) -> bool:
        try:
            return self.__channelEmtyDAL.delete_all_channel_emty()
        except Exception as e:
            print(f"Error deleting ChannelEmty: {e}")
    
    def get_channel_emty_by_id_channel_and_link_emty(self, id_channel: str, link_emty: str) -> Optional[ChannelEmtyDTO]:
        try:
            return self.__channelEmtyDAL.get_channel_emty_by_id_channel_and_link_emty(id_channel, link_emty)
        except Exception as e:
            print(f"Error fetching ChannelEmty: {e}")
            
    def get_all_channel_emty(self) -> List[ChannelEmtyDTO]:
        try:
            return self.__channelEmtyDAL.get_all_channel_emty()
        except Exception as e:
            print(f"Error fetchting ChannelEmty: {e}")