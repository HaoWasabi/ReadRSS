from ..DTO.emty_dto import EmtyDTO
from ..DAL.emty_dal import EmtyDAL
from typing import Optional, List

class EmtyBLL:
    def __init__(self):
        self.__EmtyDAL = EmtyDAL()
    
    def insert_emty(self, emty_dto: EmtyDTO) -> bool:
        try:
            return self.__EmtyDAL.insert_emty(emty_dto)
        except Exception as e:
            print(f"Error inserting Emty: {e}")
            return False

    def delete_emty_by_link_emty(self, emty_link: str) -> bool:
        try:
            return self.__EmtyDAL.delete_emty_by_link_emty(emty_link)
        except Exception as e:
            print(f"Error deleting Emty: {e}")
            return False
            
    def delete_all_emty(self) -> bool:
        try:
            return self.__EmtyDAL.delete_all_emty()
        except Exception as e:
            print(f"Error deleting Emty: {e}")
            return False

    def update_emty_by_link_emty(self, emty_link: str, emty_dto: EmtyDTO) -> bool:
        try:
            return self.__EmtyDAL.update_emty_by_link_emty(emty_link, emty_dto)
        except Exception as e:
            print(f"Error updating Emty: {e}")
            return False
            
    def get_emty_by_link_emty(self, emty_link: str) -> Optional[EmtyDTO]:
        try:
            return self.__EmtyDAL.get_emty_by_link_emty(emty_link)
        except Exception as e:
            print(f"Error fetching Emty: {e}")

    def get_all_emty(self) -> List[EmtyDTO]:
        try:
            return self.__EmtyDAL.get_all_emty()
        except Exception as e:
            print(f"Error fetching Emty: {e}")
            return []
    