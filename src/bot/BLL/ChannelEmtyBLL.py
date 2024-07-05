from bot.DTO.ChannelEmtyDTO import ChannelEmtyDTO
from bot.DAL.ChannelEmtyDAL import ChannelEmtyDAL
from typing import Optional, List

class ChannelEmtyBLL:
    def __init__(self):
        self.__channelEmtyDAL = ChannelEmtyDAL()
        
    def insertChannelEmty(self, channel_emty_dto: ChannelEmtyDTO) -> bool:
        try:
            return self.__channelEmtyDAL.insertChannelEmty(channel_emty_dto)
        except Exception as e:
            print(f"Error inserting ChannelEmty: {e}")
    
    def deleteChannelEmtyById_channel(self, id_channel: str) -> bool:
        try:
            return self.__channelEmtyDAL.deleteChannelEmtyById_channel(id_channel)
        except Exception as e:
            print(f"Error deleting ChannelEmty: {e}")
    
    def deleteChannelEmtyById_channelAndLink_emty(self, id_channel: str, link_emty: str) -> bool:
        try:
            return self.__channelEmtyDAL.deleteChannelEmtyById_channelAndLink_emty(id_channel, link_emty)
        except Exception as e:
            print(f"Error deleting ChannelEmty: {e}")
            
    def deleteAllChannelEmty(self) -> bool:
        try:
            return self.__channelEmtyDAL.deleteAllChannelEmty()
        except Exception as e:
            print(f"Error deleting ChannelEmty: {e}")
            
    def updateChannelEmtyById_channelAndLink_emty(self, id_channel: str, link_emty: str, channel_emty_dto: ChannelEmtyDTO) -> bool:
        try:
            return self.__channelEmtyDAL.updateChannelEmtyById_channelAndLink_emty(id_channel, link_emty, channel_emty_dto)
        except Exception as e:
            print(f"Error updating ChannelEmty: {e}")
    
    def getChannelEmtyById_channelAndLink_emty(self, id_channel: str, link_emty: str) -> Optional[ChannelEmtyDTO]:
        try:
            return self.__channelEmtyDAL.getChannelEmtyById_channelAndLink_emty(id_channel, link_emty)
        except Exception as e:
            print(f"Error fetching ChannelEmty: {e}")
            
    def getAllChannelEmty(self) -> List[ChannelEmtyDTO]:
        try:
            return self.__channelEmtyDAL.getAllChannelEmty()
        except Exception as e:
            print(f"Error fetchting ChannelEmty: {e}")