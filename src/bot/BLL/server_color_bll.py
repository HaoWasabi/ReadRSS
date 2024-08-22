from ..DTO.server_color_dto import ServerColorDTO
from ..DAL.server_color_dal import ServerColorDAL
from typing import Optional, List

class ServerColorBLL:
    def __init__(self):
        self.__serverColorDAL = ServerColorDAL()
        
    def insert_server_color(self, server_color_dto: ServerColorDTO) -> bool:
        try:
            return self.__serverColorDAL.insert_server_color(server_color_dto)
        except Exception as e:
            print(f"Error inserting server color: {e}")
            return False
            
    def delete_server_color_by_id_server(self, id_server: str) -> bool:
        try:
            return self.__serverColorDAL.delete_server_color_by_id_server(id_server)
        except Exception as e:
            print(f"Error deleting server color: {e}")
            return False
            
    def delete_all_server_color(self) -> bool:
        try:
            return self.__serverColorDAL.delete_all_server_color()
        except Exception as e:
            print(f"Error deleting server color: {e}")
            return False
            
    def update_server_color_by_id_server(self, id_server: str, server_color_dto: ServerColorDTO) -> bool:
        try:
            return self.__serverColorDAL.update_server_color_by_id_server(id_server, server_color_dto)
        except Exception as e:
            print(f"Error updating server color: {e}")
            return False
            
    def get_server_color_by_id_server(self, id_server: str) -> Optional[ServerColorDTO]:
        try:
            return self.__serverColorDAL.get_server_color_by_id_server(id_server)
        except Exception as e:
            print(f"Error fetching server color: {e}")
            
    def get_all_server_color(self) -> List[ServerColorDTO]:
        try:
            return self.__serverColorDAL.get_all_server_color()
        except Exception as e:
            print(f"Error fetching server color: {e}")
            return []
            
