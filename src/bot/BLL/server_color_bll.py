from ..DTO.server_color_dto import ServerColorDTO
from ..DAL.server_color_dal import ServerColorDAL
from typing import Optional, List

class ServerColorBLL:
    def __init__(self):
        self.__serverColorDAL = ServerColorDAL()
        
    def insert_server_color(self, server_color_dto: ServerColorDTO) -> bool:
            return self.__serverColorDAL.insert_server_color(server_color_dto)

            
    def delete_server_color_by_id_server(self, id_server: str) -> bool:
            return self.__serverColorDAL.delete_server_color_by_id_server(id_server)

            
    def delete_all_server_color(self) -> bool:
            return self.__serverColorDAL.delete_all_server_color()

            
    def update_server_color_by_id_server(self, id_server: str, server_color_dto: ServerColorDTO) -> bool:
            return self.__serverColorDAL.update_server_color_by_id_server(id_server, server_color_dto)

            
    def get_server_color_by_id_server(self, id_server: str) -> Optional[ServerColorDTO]:
            return self.__serverColorDAL.get_server_color_by_id_server(id_server)

    def get_all_server_color(self) -> List[ServerColorDTO]:
            return self.__serverColorDAL.get_all_server_color()

            
