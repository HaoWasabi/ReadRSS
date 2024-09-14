

from datetime import datetime
from types import NotImplementedType


class TransactionHistoryDTO:

    def __init__(self, transaction_id:str, created: datetime, content:str, credit_amount:int, currency:str) -> None:
        self.__transaction_id = transaction_id
        self.__created = created
        self.__content = content
        self.__credit_amount = credit_amount
        self.__currency = currency
    
    def __str__(self) -> str:
        return f"TransactionHistoryDTO(transaction_id={self.__transaction_id} created={self.__created} content={self.__content} credit_amount={self.__credit_amount} currency={self.__currency})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TransactionHistoryDTO):
            return NotImplementedType
        return \
            self.__transaction_id == other.__transaction_id and \
            self.__created == other.__created and \
            self.__content == other.__content and \
            self.__credit_amount == other.__credit_amount and \
            self.__currency == other.__currency
            
    
    def get_transaction_id(self):
        return self.__transaction_id
    def get_time(self) -> datetime:
        return self.__created
    def get_content(self):
        return self.__content
    def get_credit_amount(self):
        return self.__credit_amount
    def get_currency(self):
        return self.__currency
    
    
    def set_transaction_id(self, value: str):
        self.__transaction_id = value
    def set_time(self, value: datetime):
        self.__created = value
    def set_content(self, value: str):
        self.__content = value
    def set_credit_amount(self, value: int):
        self.__credit_amount = value
    def set_currency(self, value: str):
        self.__currency = value