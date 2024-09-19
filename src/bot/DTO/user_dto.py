class UserDTO:
    def __init__(self, user_id: str, user_name: str):
        self.__user_id = user_id
        self.__user_name = user_name
        
    def __str__(self) -> str:
        return f"UserDTO(user_id={self.__user_id}, user_name={self.__user_name})"
        
    def set_user_name(self, user_name: str) -> None:
        self.__user_name = user_name
    
    def get_user_id(self) -> str:
        return self.__user_id
    
    def get_user_name(self) -> str:
        return self.__user_name
    