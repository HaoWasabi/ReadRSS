from bot.DTO.ServerDTO import ServerDTO
from bot.DAL.ServerDAL import ServerDAL
from typing import Optional, List


class ServerBLL:
    def __init__(self):
        self.__serverDAL = ServerDAL()
        
    def insertServer(self, server_dto: ServerDTO) -> bool:
        try:
            return self.__serverDAL.insertServer(server_dto)
        except Exception as e:
            print(f"Error inserting server: {e}")
            
    def updateServerById(self, id_server: str, server_dto: ServerDTO) -> bool:
        try:
            return self.__serverDAL.updateServerById(id_server, server_dto)
        except Exception as e:
            print(f"Error updating server: {e}")
            
    def deleteAllServer(self) -> bool:
        try:
            return self.__serverDAL.deleteAllServer()
        except Exception as e:
            print(f"Error deleting server: {e}")
            
    def deleteServerById(self, id_server: str) -> bool:
        try:
            return self.__serverDAL.deleteServerById(id_server)
        except Exception as e:
            print(f"Error deleting server: {e}")
            
    def getServerById(self, id_server: str) -> Optional[ServerDTO]:
        try:
            return self.__serverDAL.getServerById(id_server)
        except Exception as e:
            print(f"Error fetching server: {e}")
            
    def getAllServer(self) -> List[ServerDTO]:
        try:
            return self.__serverDAL.getAllServer()
        except Exception as e:
            print(f"Error fetching server: {e}")
            


