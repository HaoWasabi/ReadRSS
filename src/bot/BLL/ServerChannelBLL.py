from bot.DAL.ServerChannelDAL import ServerChannelDAL
from bot.DTO.ServerChannelDTO import ServerChannelDTO
from typing import Optional, List

class ServerChannelBLL:
    def __init__(self):
        self.__serverChannelDAL = ServerChannelDAL()

    def insertServerChannel(self, server_channel_dto: ServerChannelDTO) -> bool:
        try:
            return self.__serverChannelDAL.insertServerChannel(server_channel_dto)
        except Exception as e:
            print(f"Error inserting server_channel: {e}")
            
    def deleteServerChannelById_serverAndId_channel(self, id_server: str, id_channel: str) -> bool:
        try:
            return self.__serverChannelDAL.deleteServerChannelById_serverAndId_channel(id_server, id_channel)
        except Exception as e:
            print(f"Error deleting server_channel: {e}")
    
    def deleteAllServerChannel(self) -> bool:
        try:
            return self.__serverChannelDAL.deleteAllServerChannel()
        except Exception as e:
            print(f"Error deleting server_channel: {e}")
            
    def updateServerChannelById_serverAndId_channel(self, id_server: str, id_channel: str, server_channel_dto: ServerChannelDTO) -> bool:
        try:
            return self.__serverChannelDAL.updateServerChannelById_serverAndId_channel(id_server, id_channel, server_channel_dto)
        except Exception as e:
            print(f"Error updating server_channel: {e}")
            
    def getServerChannelById_serverAndId_channel(self, id_server: str, id_channel: str) -> Optional[ServerChannelDTO]:
        try:
            return self.__serverChannelDAL.getServerChannelById_serverAndId_channel(id_server, id_channel)
        except Exception as e:
            print(f"Error fetching server_channel: {e}")
            
    def getAllServerChannel(self) -> List[ServerChannelDTO]:
        try:
            return self.__serverChannelDAL.getAllServerChannel()
        except Exception as e:
            print(f"Error fetching server_channel: {e}")
            