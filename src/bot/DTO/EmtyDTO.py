class EmtyDTO:
    def __init__(self, link_emty: str, title_emty: str, description_emty: str, image_emty: str, pubDate_emty: str):
        self.__link_emty = link_emty
        self.__title_emty = title_emty
        self.__description_emty = description_emty
        self.__image_emty = image_emty
        self.__pubDate_emty = pubDate_emty
        
    def __str__(self) -> str:
        return f"EmtyDTO(link_emty={self.__link_emty}, title_emty={self.__title_emty}, description_emty={self.__description_emty}, image_emty={self.__image_emty}, pubDate_emty={self.__pubDate_emty})"
        
    def setLink_emty(self, link_emty: str) -> None:
        self.__link_emty = link_emty
    
    def setTitle_emty(self, title_emty: str) -> None:
        self.__title_emty = title_emty
    
    def setDescription_emty(self, description_emty: str) -> None:
        self.__description_emty = description_emty
    
    def setImage_emty(self, image_emty: str) -> None:
        self.__image_emty = image_emty
    
    def setPubDate_emty(self, pubDate_emty: str) -> None:
        self.__pubDate_emty = pubDate_emty
    
    def getLink_emty(self) -> str:
        return self.__link_emty
    
    def getTitle_emty(self) -> str:
        return self.__title_emty
    
    def getDescription_emty(self) -> str:
        return self.__description_emty
    
    def getImage_emty(self) -> str:
        return self.__image_emty
    
    def getPubDate_emty(self) -> str:
        return self.__pubDate_emty