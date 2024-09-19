

from ..BLL.singleton import Singleton
from ..DTO.server_pay_dto import ServerPayDTO
from ..DAL.server_pay_dal import ServerPayDAL


class ServerPayBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__ServerPayDAL = ServerPayDAL()
            self._initialized = True
    
    def get_all_server_pay(self):
        return self.__ServerPayDAL.get_all_server_pay()
    def get_server_pay_by_server_id(self, server_id: str):
        return self.__ServerPayDAL.get_server_pay_by_server_id(server_id)
        
    def insert_server_pay(self, server_pay: ServerPayDTO):
        self.__ServerPayDAL.insert_server_pay(server_pay)

    def update_server_pay(self, server_pay: ServerPayDTO):
        self.__ServerPayDAL.update_server_pay(server_pay)
    
    def delete_server_pay_by_server_id(self, server_id: str):
        self.__ServerPayDAL.delete_server_pay_by_server_id(server_id)