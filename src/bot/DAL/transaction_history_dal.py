

import sqlite3
from ..DTO.transaction_history_dto import TransactionHistoryDTO
from ..utils.datetime_format import datetime_from_string, datetime_to_string
from .base_dal import BaseDAL, logger


class TransactionHistoryDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        try:
        
            self.cursor.execute("""
                CREATE TABLE transaction_history (
                    transaction_id TEXT PRIMARY KEY,
                    `time` datetime,
                    `content` TEXT,
                    credit_amount INT,
                    `currency` TEXT
                )
            """)
            self.connection.commit()
            logger.info(f"Table 'transaction_history' created successfully.")
        except sqlite3.Error as e:
            if len(e.args) and e.args[0].count('already exists'):
                return
            logger.error(f"Error creating table 'tbl_server': {e}")
        
    def get_transaction_history_by_id(self, transaction_id: str):
        self.cursor.execute('SELECT transaction_id , `time`, `content`, credit_amount , `currency` FROM transaction_history WHERE transaction_id=?;', (transaction_id,))
        c = self.cursor.fetchone()
        if c:
            return TransactionHistoryDTO(c[0], datetime_from_string(c[1]), c[2], c[3], c[4])
    
        return None
    
    def insert_transaction_history(self, transaction: TransactionHistoryDTO):
        self.cursor.execute('INSERT INTO transaction_history(transaction_id , `time`, `content`, credit_amount , `currency`) VALUES (?, ?, ?, ?, ?)', 
                            (
                                transaction.get_transaction_id(),
                                datetime_to_string(transaction.get_time()),
                                transaction.get_content(),
                                transaction.get_credit_amount(),
                                transaction.get_currency(),
                            ))
        
        self.connection.commit()
        
