from datetime import timedelta

from ..DTO.premium_dto import PremiumDTO
from ..DTO.user_dto import UserDTO
from ..utils.datetime_format import datetime_from_string, datetime_to_string


class UserPremiumDTO:
    def __init__(self, user: UserDTO, premium: PremiumDTO, date_registered: str):
        self.__user = user
        self.__premium = premium
        self.__date_registered = date_registered
        
    def __str__(self) -> str:
        return f"UserPremiumDTO(user={self.__user}, premium={self.__premium}, date_registered={self.__date_registered})"
        
    def get_user(self) -> UserDTO:
        return self.__user

    def get_premium(self) -> PremiumDTO:
        return self.__premium
    
    def get_date_registered(self) -> str:
        return self.__date_registered
    
    def get_date_expired(self) -> str:
        return datetime_to_string((datetime_from_string(self.__date_registered) + timedelta(days=self.__premium.get_duration())))