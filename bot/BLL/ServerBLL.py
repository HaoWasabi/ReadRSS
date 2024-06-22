from bot.DTO.ServerDTO import ServerDTO
from bot.DAL.ServerDAL import ServerDAL


class ServerBLL:
    def __init__(self):
        self.__serverDAL = ServerDAL()
        
    def insert_server(self, server_dto):
        try:
            return self.__serverDAL.insert_server(server_dto)
        except Exception as e:
            print(f"Error inserting server: {e}")
            
    def update_server_by_id(self, id_server, server_dto):
        try:
            return self.__serverDAL.update_server_by_id(id_server, server_dto)
        except Exception as e:
            print(f"Error updating server: {e}")
            
    def delete_all_server(self):
        try:
            return self.__serverDAL.delete_all_server()
        except Exception as e:
            print(f"Error deleting server: {e}")
            
    def delete_server_by_id(self, id_server):
        try:
            return self.__serverDAL.delete_server_by_id(id_server)
        except Exception as e:
            print(f"Error deleting server: {e}")
            
    def get_server_by_id(self, id_server):
        try:
            return self.__serverDAL.get_server_by_id(id_server)
        except Exception as e:
            print(f"Error fetching server: {e}")
            
    def get_all_server(self):
        try:
            return self.__serverDAL.get_all_server()
        except Exception as e:
            print(f"Error fetching server: {e}")
            


