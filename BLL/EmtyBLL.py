from bot.DTO.EmtyDTO import EmtyDTO
from bot.DAL.EmtyDAL import EmtyDAL
from typing import Optional, List

class EmtyBLL:
    def __init__(self):
        self.__EmtyDAL = EmtyDAL()
    
    def insertEmty(self, emty_dto: EmtyDTO) -> bool:
        try:
            return self.__EmtyDAL.insertEmty(emty_dto)
        except Exception as e:
            print(f"Error inserting Emty: {e}")

    def deleteEmtyByLink_emty(self, emty_link: str) -> bool:
        try:
            return self.__EmtyDAL.deleteEmtyByLink_emty(emty_link)
        except Exception as e:
            print(f"Error deleting Emty: {e}")
            
    def deleteAllEmty(self) -> bool:
        try:
            return self.__EmtyDAL.deleteAllEmty()
        except Exception as e:
            print(f"Error deleting Emty: {e}")

    def updateEmtyByLink_emty(self, emty_link: str, emty_dto: EmtyDTO) -> bool:
        try:
            return self.__EmtyDAL.updateEmtyByLink_emty(emty_link, emty_dto)
        except Exception as e:
            print(f"Error updating Emty: {e}")
            
    def getEmtyByLink_emty(self, emty_link: str) -> Optional[EmtyDTO]:
        try:
            return self.__EmtyDAL.getEmtyByLink_emty(emty_link)
        except Exception as e:
            print(f"Error fetching Emty: {e}")

    def getAllEmty(self) -> List[EmtyDTO]:
        try:
            return self.__EmtyDAL.getAllEmty()
        except Exception as e:
            print(f"Error fetching Emty: {e}")
    