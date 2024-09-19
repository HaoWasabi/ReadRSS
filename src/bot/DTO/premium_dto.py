from datetime import datetime
from tokenize import Double
from typing import Optional


class PremiumDTO:
    def __init__(self, premium_id: str, price: float, date_created: str, duration: int, is_active=True):
        self.__premium_id = premium_id
        self.__price = price
        self.__date_created = date_created
        self.__duration = duration
        self.__is_active = is_active
        
    def __str__(self) -> str:
        return f"PremiumDTO(premium_id={self.__premium_id}, price={self.__price}, date_created={self.__date_created}, duration={self.__duration}, is_active={self.__is_active})"

    def set_duration(self, duration: int) -> None:
        self.__duration = duration
        
    def set_price(self, price: float) -> None:
        self.__price = price
        
    def set_state(self, is_active: bool) -> None:
        self.__is_active = is_active
        
    def get_premium_id(self) -> str:
        return self.__premium_id
    
    def get_duration(self) -> int:
        return self.__duration
    
    def get_date_created(self) -> str:
        return self.__date_created
    
    def get_price(self) -> float:
        return self.__price
    
    def get_state(self) -> bool:
        return self.__is_active
    