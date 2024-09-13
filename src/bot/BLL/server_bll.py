from ..DTO.server_dto import ServerDTO
from ..DAL.server_dal import ServerDAL
from typing import Optional, List


class ServerBLL:
    def __init__(self):
        self.__serverDAL = ServerDAL()
        
    def insert_server(self, server_dto: ServerDTO) -> bool:
            return self.__serverDAL.insert_server(server_dto)

            
    def update_server_by_id_server(self, id_server: str, server_dto: ServerDTO) -> bool:
            return self.__serverDAL.update_server_by_id_server(id_server, server_dto)

            
    def delete_all_server(self) -> bool:
            return self.__serverDAL.delete_all_server()

            
    def delete_server_by_id_server(self, id_server: str) -> bool:
            return self.__serverDAL.delete_server_by_id_server(id_server)

            
    def get_server_by_id_server(self, id_server: str) -> Optional[ServerDTO]:
            return self.__serverDAL.get_server_by_id_server(id_server)

    def get_all_server(self) -> List[ServerDTO]:
            return self.__serverDAL.get_all_server()

            


