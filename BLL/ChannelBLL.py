from bot.DTO.ChannelDTO import ChannelDTO
from bot.DAL.ChannelDAL import ChannelDAL
from typing import Optional, List

class ChannelBLL:
    def __init__(self):
        self.__channelDAL = ChannelDAL()
    
    def insertChannel(self, channel_dto: ChannelDTO) -> bool:
        try:
            return self.__channelDAL.insertChannel(channel_dto)
        except Exception as e:
            print(f"Error inserting channel: {e}")

    def deleteChannelById_channel(self, channel_link: str) -> bool:
        try:
            return self.__channelDAL.deleteChannelById_channel(channel_link)
        except Exception as e:
            print(f"Error deleting channel: {e}")
            
    def deleteAllChannel(self) -> bool:
        try:
            return self.__channelDAL.deleteAllChannel()
        except Exception as e:
            print(f"Error deleting channel: {e}")

    def updateChannelById_channel(self, channel_link: str, Channel_dto: ChannelDTO) -> bool:
        try:
            return self.__channelDAL.updateChannelById_channel(channel_link, Channel_dto)
        except Exception as e:
            print(f"Error updating Channel: {e}")
            
    def getChannelById_channel(self, channel_link: str) -> Optional[ChannelDTO]:
        try:
            return self.__channelDAL.getChannelById_channel(channel_link)
        except Exception as e:
            print(f"Error fetching Channel: {e}")

    def getAllChannel(self) -> List[ChannelDTO]:
        try:
            return self.__channelDAL.getAllChannel()
        except Exception as e:
            print(f"Error fetching Channel: {e}")
    