from asyncio.log import logger
from datetime import timedelta, datetime

from ..DTO.premium_dto import PremiumDTO
from ..DTO.user_dto import UserDTO
from ..utils.datetime_format import datetime_from_string, datetime_to_string


class UserPremiumDTO:
    def __init__(self, user: UserDTO, premium: PremiumDTO, date_registered: datetime):
        self.__user = user
        self.__premium = premium
        self.__date_registered = date_registered
        
    def __str__(self) -> str:
        return f"UserPremiumDTO(user={self.__user}, premium={self.__premium}, date_registered={self.__date_registered})"
        
    def get_user(self) -> UserDTO:
        return self.__user

    def get_premium(self) -> PremiumDTO:
        return self.__premium
    
    def get_date_registered(self) -> datetime:
        return self.__date_registered
    
    def get_date_expired(self) -> datetime:
        duration = self.__premium.get_duration()
        
        if duration is None:
            logger.error("Duration is None, returning current date.")
            return datetime.now()  # Hoặc bạn có thể xử lý theo cách khác.

        try:
            duration_days = float(duration)
            if duration_days < 0:
                logger.error("Duration is negative, returning current date.")
                return datetime.now()  # Hoặc xử lý theo cách khác.

            return self.__date_registered + timedelta(days=duration_days)
        except ValueError as e:
            logger.error(f"Invalid duration value: {duration}, error: {e}")
            return datetime.now()  # Hoặc xử lý theo cách khác.
