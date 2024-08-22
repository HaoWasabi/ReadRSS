from ..DTO.server_dto import ServerDTO
from ..DAL.server_dal import ServerDAL
from typing import Optional, List


class ServerBLL:
    def __init__(self):
        self.__serverDAL = ServerDAL()
        
    def insert_server(self, server_dto: ServerDTO) -> bool:
        try:
            return self.__serverDAL.insert_server(server_dto)
        except Exception as e:
            print(f"Error inserting server: {e}")
            return False
            
    def update_server_by_id_server(self, id_server: str, server_dto: ServerDTO) -> bool:
        try:
            return self.__serverDAL.update_server_by_id_server(id_server, server_dto)
        except Exception as e:
            print(f"Error updating server: {e}")
            return False
            
    def delete_all_server(self) -> bool:
        try:
            return self.__serverDAL.delete_all_server()
        except Exception as e:
            print(f"Error deleting server: {e}")
            return False
            
    def delete_server_by_id_server(self, id_server: str) -> bool:
        try:
            return self.__serverDAL.delete_server_by_id_server(id_server)
        except Exception as e:
            print(f"Error deleting server: {e}")
            return False
            
    def get_server_by_id_server(self, id_server: str) -> Optional[ServerDTO]:
        try:
            return self.__serverDAL.get_server_by_id_server(id_server)
        except Exception as e:
            print(f"Error fetching server: {e}")
            
    def get_all_server(self) -> List[ServerDTO]:
        try:
            return self.__serverDAL.get_all_server()
        except Exception as e:
            print(f"Error fetching server: {e}")
            return []
            


