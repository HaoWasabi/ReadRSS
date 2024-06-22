from bot.DTO.ServerDTO import ServerDTO
from bot.BLL.ServerBLL import ServerBLL
from bot.DAL.ServerChannelDAL import ServerChannelDAL


class ServerChannelBLL:
    def __init__(self):
        self.__serverChannelDAL = ServerChannelDAL()

    def insert_server_channel(self, server_channel_dto):
        try:
            return self.__serverChannelDAL.insert_server_channel(server_channel_dto)
        except Exception as e:
            print(f"Error inserting server_channel: {e}")
            
    def delete_server_channel_by_id_server_and_id_channel(self, id_server, id_channel):
        try:
            return self.__serverChannelDAL.delete_server_channel_by_id_server_and_id_channel(id_server, id_channel)
        except Exception as e:
            print(f"Error deleting server_channel: {e}")
    
    def delete_all_server_channel(self):
        try:
            return self.__serverChannelDAL.delete_all_server_channel()
        except Exception as e:
            print(f"Error deleting server_channel: {e}")
            
    def update_server_channel_by_id_server_and_id_channel(self, id_server, id_channel, server_channel_dto):
        try:
            return self.__serverChannelDAL.update_server_channel_by_id_server_and_id_channel(id_server, id_channel, server_channel_dto)
        except Exception as e:
            print(f"Error updating server_channel: {e}")
            
    def get_server_channel_by_id_server_and_id_channel(self, id_server, id_channel):
        try:
            return self.__serverChannelDAL.get_server_channel_by_id_server_and_id_channel(id_server, id_channel)
        except Exception as e:
            print(f"Error fetching server_channel: {e}")
            
    def get_all_server_channel(self):
        try:
            return self.__serverChannelDAL.get_all_server_channel()
        except Exception as e:
            print(f"Error fetching server_channel: {e}")
            