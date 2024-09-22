

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
                        `qr_code` TEXT PRIMARY KEY,
                        `user_id` TEXT,
                        `channel_id` TEXT,
                        `premium_id` TEXT,
                        `message_id` TEXT,
                        `date_created` DATETIME,
                        `is_success` bool
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
        self.cursor.execute('SELECT * WHERE transaction_id=?;', (transaction_id,))
        c = self.cursor.fetchone()
        self.close_connection()
        if c:
            return TransactionHistoryDTO(*c)
    
        return None
    
    def insert_transaction_history(self, transaction: TransactionHistoryDTO):
        self.open_connection()
        self.cursor.execute(
            'INSERT INTO transaction_history(`id_transaction`, `qr_code`, `transaction_date`, `content`, `currency`, `credit_amount`,) VALUES (?,?,?,?,?,?)',
            (transaction.id_transaction,
             transaction.qr_code,
             datetime_to_string(transaction.transaction_date),
             transaction.content,
             transaction.currency,
             transaction.credit_amount)
        )  
        
        self.connection.commit()
        self.close_connection()
