from ..BLL.singleton import Singleton
from ..DTO.emty_dto import EmtyDTO
from ..DAL.emty_dal import EmtyDAL
from typing import Optional, List


class EmtyBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__emtyDAL = EmtyDAL()
            self._initialized = True

    def insert_emty(self, emty_dto: EmtyDTO) -> bool:
        return self.__emtyDAL.insert_emty(emty_dto)

    def delete_emty_by_link_emty(self, emty_link: str) -> bool:
        return self.__emtyDAL.delete_emty_by_link_emty(emty_link)

    def delete_all_emty(self) -> bool:
        return self.__emtyDAL.delete_all_emty()

    def update_emty_by_link_emty(self, emty_link: str, emty_dto: EmtyDTO) -> bool:
        return self.__emtyDAL.update_emty_by_link_emty(emty_link, emty_dto)

    def get_emty_by_link_emty(self, emty_link: str) -> Optional[EmtyDTO]:
        return self.__emtyDAL.get_emty_by_link_emty(emty_link)

    def get_all_emty(self) -> List[EmtyDTO]:
        return self.__emtyDAL.get_all_emty()
