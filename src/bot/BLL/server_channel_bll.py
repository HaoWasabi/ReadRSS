from ..DTO.server_channel_dto import ServerChannelDTO
from ..DAL.server_channel_dal import ServerChannelDAL
from typing import Optional, List

class ServerChannelBLL:
    def __init__(self):
        self.__serverChannelDAL = ServerChannelDAL()

    def insert_server_channel(self, server_channel_dto: ServerChannelDTO) -> bool:
            return self.__serverChannelDAL.insert_server_channel(server_channel_dto)
            
    def delete_server_channel_by_id_server_and_id_channel(self, id_server: str, id_channel: str) -> bool:
            return self.__serverChannelDAL.delete_server_channel_by_id_server_and_id_channel(id_server, id_channel)
    
    def delete_server_channel_by_id_channel(self, id_channel: str) -> bool:
            return self.__serverChannelDAL.delete_server_channel_by_id_channel(id_channel)
        
    def delete_all_server_channel(self) -> bool:
            return self.__serverChannelDAL.delete_all_server_channel()
            
    def get_server_channel_by_id_server_and_id_channel(self, id_server: str, id_channel: str) -> Optional[ServerChannelDTO]:
            return self.__serverChannelDAL.get_server_channel_by_id_server_and_id_channel(id_server, id_channel)
    def get_all_server_channel(self) -> List[ServerChannelDTO]:
            return self.__serverChannelDAL.get_all_server_channel()
        
    def get_all_server_channel_by_id_server(self, id_server: str) -> List[ServerChannelDTO]:
            return self.__serverChannelDAL.get_all_server_channel_by_id_server(id_server)
        
            