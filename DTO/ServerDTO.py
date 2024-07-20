class ServerDTO:
    def __init__(self, id_server: str, name_server: str):
        self.__id_server = id_server
        self.__name_server = name_server
        
    def __str__(self) -> str:
        return f"ServerDTO(id_server={self.__id_server}, name_server={self.__name_server})"
    
    def setId_server(self, id_server: str) -> None:
        self.__id_server = id_server
        
    def setName_server(self, name_server: str) -> None:
        self.__name_server = name_server
        
    def getId_server(self) -> str:
        return self.__id_server
    
    def getName_server(self) -> str:
        return self.__name_server
    