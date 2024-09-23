from typing import Optional
from .singleton import Singleton
from ..DAL import PremiumDAL
from ..DTO import PremiumDTO


class PremiumBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__premiumDAL = PremiumDAL()
            self._initialized = True

    def insert_premium(self, premium: PremiumDTO) -> bool:
        return self.__premiumDAL.insert_premium(premium)

    def delete_premium_by_id(self, premium_id: str) -> bool:
        return self.__premiumDAL.delete_premium_by_id(premium_id)

    def get_premium_by_id(self, premium_id: str) -> Optional[PremiumDTO]:
        return self.__premiumDAL.get_premium_by_id(premium_id)

    def get_all_premiums(self, ignore_state=False, is_active=True):
        return self.__premiumDAL.get_all_premium(ignore_state, is_active)
