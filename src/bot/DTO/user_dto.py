class UserDTO:
    def __init__(self, id_user: str, name_user: str):
        self.__user_id = id_user
        self.__user_name = name_user
        
    def __str__(self) -> str:
        return f"UserDTO(id_user={self.__user_id}, name_user={self.__user_name})"
        
    def set_user_name(self, user_name: str) -> None:
        self.__user_name = user_name
    
    def get_user_id(self) -> str:
        return self.__user_id
    
    def get_user_name(self) -> str:
        return self.__user_name
    