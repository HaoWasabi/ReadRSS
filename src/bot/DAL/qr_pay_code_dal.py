
from operator import truediv
import sqlite3

from ..utils.datetime_format import datetime_from_string, datetime_to_string
from ..DTO.qr_code_pay_dto import QrPayCodeDTO
from ..DAL.base_dal import BaseDAL, logger



class QrPayCodeDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    
    def create_table(self):
        self.open_connection()
        try:
            self.cursor.execute('''
            CREATE TABLE qr_pay_code (
                    `qr_code` TEXT PRIMARY KEY,
                    `user_id` TEXT,
                    `channel_id` TEXT,
                    `premium_id` TEXT,
                    `message_id` TEXT,
                    `date_created` timestamp,
                    `is_success` bool
            )
            ''')
            self.connection.commit()
            logger.info(f"Table 'tbl_server' created successfully.")
        except sqlite3.Error as e:
            if len(e.args) and e.args[0].count('already exists'):
                return
            logger.error(f"Error creating table 'tbl_server': {e}")
        finally:
            self.close_connection()
            
    
    def get_qr_pay_code_by_qr_code(self, qr_code: str):
        self.open_connection()
        self.cursor.execute("SELECT * WHERE qr_code=?; ", (qr_code,))
        rows=self.cursor.fetchone()
        self.close_connection()
        if rows:
            rows[-1] = datetime_from_string(rows[-1])
            return QrPayCodeDTO(*rows)
        
        return None
        
    def get_all_qr_pay_code(self):
        self.open_connection()
        self.cursor.execute("SELECT * FROM qr_pay_code;")
        rows = self.cursor.fetchall()
        self.close_connection()
        return [QrPayCodeDTO(*a) for a in rows]
    
    def insert_qr_pay_code(self, qr_pay: QrPayCodeDTO):
        self.open_connection()
        self.cursor.execute(
            "INSERT OR REPLACE INTO qr_pay_code VALUES (?, ?, ?, ?, ?, ?, ?);", 
            (
                qr_pay.qr_code,
                qr_pay.user_id,
                qr_pay.channel_id,
                qr_pay.premium_id,
                qr_pay.message_id,
                qr_pay.date_created,
                qr_pay.is_success
            )
        )
        self.connection.commit()
        self.close_connection()
        return True
    
    def delete_qr_pay_by_id(self, qr_code: str):
        self.open_connection()
        self.cursor.execute('DELETE FROM qr_pay_code WHERE qr_code=?;', (qr_code,))
        self.connection.commit()
        self.close_connection()
        return True
    