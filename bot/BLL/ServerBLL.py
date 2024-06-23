from bot.DTO.ServerDTO import ServerDTO
from bot.DAL.ServerDAL import ServerDAL


class ServerBLL:
    def __init__(self):
        self.__serverDAL = ServerDAL()
        
    def insertServer(self, server_dto):
        try:
            return self.__serverDAL.insertServer(server_dto)
        except Exception as e:
            print(f"Error inserting server: {e}")
            
    def updateServerById(self, id_server, server_dto):
        try:
            return self.__serverDAL.updateServerById(id_server, server_dto)
        except Exception as e:
            print(f"Error updating server: {e}")
            
    def deleteAllServer(self):
        try:
            return self.__serverDAL.deleteAllServer()
        except Exception as e:
            print(f"Error deleting server: {e}")
            
    def deleteServerById(self, id_server):
        try:
            return self.__serverDAL.deleteServerById(id_server)
        except Exception as e:
            print(f"Error deleting server: {e}")
            
    def getServerById(self, id_server):
        try:
            return self.__serverDAL.getServerById(id_server)
        except Exception as e:
            print(f"Error fetching server: {e}")
            
    def getAllServer(self):
        try:
            return self.__serverDAL.getAllServer()
        except Exception as e:
            print(f"Error fetching server: {e}")
            


