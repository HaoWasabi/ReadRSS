from types import NotImplementedType

class ServerDTO:
    def __init__(self, id_server: str, name_server: str, is_active=True):
        self.__id_server = id_server
        self.__name_server = name_server
        self.__is_active = is_active
        
    def __str__(self) -> str:
        return f"ServerDTO(id_server={self.__id_server}, name_server={self.__name_server}, is_active={self.__is_active})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ServerDTO):
            return NotImplementedType
        return self.__id_server == other.__id_server and self.__name_server == other.__name_server
    
    def set_id_server(self, id_server: str) -> None:
        self.__id_server = id_server
        
    def set_name_server(self, name_server: str) -> None:
        self.__name_server = name_server
        
    def set_state(self, is_active: bool) -> None:
        self.__is_active = is_active
        
    def get_id_server(self) -> str:
        return self.__id_server
    
    def get_name_server(self) -> str:
        return self.__name_server
    
    def get_state(self) -> bool:
        return self.__is_active
    