

import sqlite3
from ..DTO.transaction_history_dto import TransactionHistoryDTO
from ..utils.datetime_format import datetime_from_string, datetime_to_string
from .base_dal import BaseDAL, logger


class TransactionHistoryDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        self.open_connection()
        try:
        
            self.cursor.execute("""
                CREATE TABLE `transaction_history` (
                    `id_transaction` TEXT PRIMARY KEY,
                    `qr_code` TEXT,
                    `transaction_date` timestamp ,
                    `content` TEXT,
                    `currency` INT,
                    `credit_amount` TEXT      
                );
            """)
            self.connection.commit()
            logger.info(f"Table 'transaction_history' created successfully.")
        except sqlite3.Error as e:
            if len(e.args) and e.args[0].count('already exists'):
                return
            logger.error(f"Error creating table 'tbl_server': {e}")
        finally:
            self.close_connection()
        
    def get_transaction_history_by_id(self, transaction_id: str):
        self.open_connection()
        self.cursor.execute('SELECT * FROM transaction_history WHERE id_transaction=?;', (transaction_id,))
        c = self.cursor.fetchone()
        self.close_connection()
        if c:
            return TransactionHistoryDTO(*c)
    
        return None
    
    def insert_transaction_history(self, transaction: TransactionHistoryDTO):
        self.open_connection()
        self.cursor.execute(
            'INSERT INTO transaction_history VALUES (?,?,?,?,?,?)',
            (transaction.id_transaction,
             transaction.qr_code,
             transaction.transaction_date,
             transaction.content,
             transaction.currency,
             transaction.credit_amount)
        )  
        
        self.connection.commit()
        self.close_connection()
