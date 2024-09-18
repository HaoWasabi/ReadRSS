
from typing import List, Optional
from ..DTO.user_dto import UserDTO
from ..BLL.Singleton import Singleton
from ..DAL.user_dal import UserDAL


class UserBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__userDAL = UserDAL()
            self._initialized = True
    
    def insert_user(self, user_dto: UserDTO) -> bool:
        return self.__userDAL.insert_user(user_dto)
    
    def update_user(self, user_dto: UserDTO) -> bool:
        return self.__userDAL.update_user(user_dto)
    
    def get_all_user(self) -> List[UserDTO]:
        return self.__userDAL.get_all_user()
    
    def get_user_by_user_id(self, user_id: str) -> Optional[UserDTO]:
        return self.__userDAL.get_user_by_user_id(user_id)