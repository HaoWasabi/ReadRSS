from ..DTO.server_channel_dto import ServerChannelDTO
from ..DAL.server_channel_dal import ServerChannelDAL
from typing import Optional, List

class ServerChannelBLL:
    def __init__(self):
        self.__serverChannelDAL = ServerChannelDAL()

    def insert_server_channel(self, server_channel_dto: ServerChannelDTO) -> bool:
        try:
            return self.__serverChannelDAL.insert_server_channel(server_channel_dto)
        except Exception as e:
            print(f"Error inserting server_channel: {e}")
            return False
            
    def delete_server_channel_by_id_server_and_id_channel(self, id_server: str, id_channel: str) -> bool:
        try:
            return self.__serverChannelDAL.delete_server_channel_by_id_server_and_id_channel(id_server, id_channel)
        except Exception as e:
            print(f"Error deleting server_channel: {e}")
            return False
    
    def delete_all_server_channel(self) -> bool:
        try:
            return self.__serverChannelDAL.delete_all_server_channel()
        except Exception as e:
            print(f"Error deleting server_channel: {e}")
            return False
            
    def get_server_channel_by_id_server_and_id_channel(self, id_server: str, id_channel: str) -> Optional[ServerChannelDTO]:
        try:
            return self.__serverChannelDAL.get_server_channel_by_id_server_and_id_channel(id_server, id_channel)
        except Exception as e:
            print(f"Error fetching server_channel: {e}")
            
    def get_all_server_channel(self) -> List[ServerChannelDTO]:
        try:
            return self.__serverChannelDAL.get_all_server_channel()
        except Exception as e:
            print(f"Error fetching server_channel: {e}")
            return []
            