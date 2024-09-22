from ..BLL.singleton import Singleton
from ..DAL.transaction_history_dal import TransactionHistoryDAL
from ..DTO.transaction_history_dto import TransactionHistoryDTO

class TransactionHistoryBLL(Singleton):
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self.__TransactionHistoryDAL = TransactionHistoryDAL()
            self._initialized = True
            
    
    def get_transaction_history_by_id(self, transaction_id: str):
        return self.__TransactionHistoryDAL.get_transaction_history_by_id(transaction_id)
    
    def insert_transaction_history(self, transaction: TransactionHistoryDTO):
        return self.__TransactionHistoryDAL.insert_transaction_history(transaction)
    
    def get_all_transaction_history(self):
        return self.__TransactionHistoryDAL.get_all_transaction_history()