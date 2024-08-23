from types import NotImplementedType

class EmtyDTO:
    def __init__(self, link_emty: str, title_emty: str, description_emty: str, image_emty: str, pubdate_emty: str):
        self.__link_emty = link_emty
        self.__title_emty = title_emty
        self.__description_emty = description_emty
        self.__image_emty = image_emty
        self.__pubdate_emty = pubdate_emty
        
    def __str__(self) -> str:
        return f"EmtyDTO(link_emty={self.__link_emty}, title_emty={self.__title_emty}, description_emty={self.__description_emty}, image_emty={self.__image_emty}, pubdate_emty={self.__pubdate_emty})"
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EmtyDTO):
            return NotImplementedType
        return self.__link_emty == other.__link_emty and self.__title_emty == other.__title_emty and self.__description_emty == other.__description_emty and self.__image_emty == other.__image_emty and self.__pubdate_emty == other.__pubdate_emty
    
    def set_link_emty(self, link_emty: str) -> None:
        self.__link_emty = link_emty
    
    def set_title_emty(self, title_emty: str) -> None:
        self.__title_emty = title_emty
    
    def set_description_emty(self, description_emty: str) -> None:
        self.__description_emty = description_emty
    
    def set_image_emty(self, image_emty: str) -> None:
        self.__image_emty = image_emty
    
    def set_pubdate_emty(self, pubdate_emty: str) -> None:
        self.__pubdate_emty = pubdate_emty
    
    def get_link_emty(self) -> str:
        return self.__link_emty
    
    def get_title_emty(self) -> str:
        return self.__title_emty
    
    def get_description_emty(self) -> str:
        return self.__description_emty
    
    def get_image_emty(self) -> str:
        return self.__image_emty
    
    def get_pubdate_emty(self) -> str:
        return self.__pubdate_emty