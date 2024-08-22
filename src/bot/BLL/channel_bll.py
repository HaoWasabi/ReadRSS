from ..DAL.channel_dal import ChannelDAL
from ..DTO.channel_dto import ChannelDTO
from typing import Optional, List

class ChannelBLL:
    def __init__(self):
        self.__channelDAL = ChannelDAL()
    
    def insert_channel(self, channel_dto: ChannelDTO) -> bool:
        try:
            return self.__channelDAL.insert_channel(channel_dto)
        except Exception as e:
            print(f"Error inserting channel: {e}")
            return False

    def delete_channel_by_id_channel(self, channel_link: str) -> bool:
        try:
            return self.__channelDAL.delete_channel_by_id_channel(channel_link)
        except Exception as e:
            print(f"Error deleting channel: {e}")
            return False
            
    def delete_all_channel(self) -> bool:
        try:
            return self.__channelDAL.delete_all_channel()
        except Exception as e:
            print(f"Error deleting channel: {e}")
            return False

    def update_channel_by_id_channel(self, channel_link: str, Channel_dto: ChannelDTO) -> bool:
        try:
            return self.__channelDAL.update_channel_by_id_channel(channel_link, Channel_dto)
        except Exception as e:
            print(f"Error updating Channel: {e}")
            return False
            
    def get_channel_by_id_channel(self, channel_link: str) -> Optional[ChannelDTO]:
        try:
            return self.__channelDAL.get_channel_by_id_channel(channel_link)
        except Exception as e:
            print(f"Error fetching Channel: {e}")

    def get_all_channel(self) -> List[ChannelDTO]:
        try:
            return self.__channelDAL.get_all_channel()
        except Exception as e:
            print(f"Error fetching Channel: {e}")
            return []
    