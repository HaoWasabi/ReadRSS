from types import NotImplementedType

class ServerDTO:
    def __init__(self, server_id: str, server_name: str, is_active=True):
        self.__server_id = server_id
        self.__server_name = server_name
        self.__is_active = is_active
        
    def __str__(self) -> str:
        return f"ServerDTO(server_id={self.__server_id}, server_name={self.__server_name}, is_active={self.__is_active})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ServerDTO):
            return NotImplementedType
        return self.__server_id == other.__server_id and self.__server_name == other.__server_name
    
    def set_server_id(self, server_id: str) -> None:
        self.__server_id = server_id
        
    def set_server_name(self, server_name: str) -> None:
        self.__server_name = server_name
        
    def set_state(self, is_active: bool) -> None:
        self.__is_active = is_active
        
    def get_server_id(self) -> str:
        return self.__server_id
    
    def get_server_name(self) -> str:
        return self.__server_name
    
    def get_state(self) -> bool:
        return self.__is_active
    