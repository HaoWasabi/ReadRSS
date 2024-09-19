from typing import List
from ..BLL.singleton import Singleton
from ..DAL.user_premium_dal import UserPremiumDAL
from ..DTO.user_premium_dto import UserPremiumDTO


class UserPremiumBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__userpremiumDAL = UserPremiumDAL()
            self._initialized = True
            
    def insert_user_premium(self, userpremium: UserPremiumDTO) -> bool:
        return self.__userpremiumDAL.insert_user_premium(userpremium)
    
    def get_all_userpremiums(self) -> List[UserPremiumDTO]:
        return self.__userpremiumDAL.get_all_userpremium()
    
    def get_all_userpremiums_by_user_id(self, user_id: str) -> List[UserPremiumDTO]:
        return self.__userpremiumDAL.get_all_userpremium_by_user_id(user_id)