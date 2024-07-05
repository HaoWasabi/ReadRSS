class ServerDTO:
    def __init__(self, id_server, name_server):
        self.__id_server = id_server
        self.__name_server = name_server
        
    def __str__(self):
        return f"ServerDTO(id_server={self.__id_server}, name_server={self.__name_server})"
    
    def setId_server(self, id_server):
        self.__id_server = id_server
        
    def setName_server(self, name_server):
        self.__name_server = name_server
        
    def getId_server(self):
        return self.__id_server
    
    def getName_server(self):
        return self.__name_server
    