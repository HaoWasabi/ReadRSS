
from operator import truediv
import sqlite3

from ..utils.datetime_format import datetime_from_string, datetime_to_string
from ..DTO.qr_code_pay_dto import QrPayCodeDTO
from ..DAL.base_dal import BaseDAL, logger


class QrPayCodeDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    
    def create_table(self):
        try:
            self.cursor.execute('''
            CREATE TABLE qr_pay_code (
                qr_code TEXT PRIMARY KEY,
                id_server TEXT,
                channel_id TEXT,
                message_id TEXT,
                ngay_tao DATETIME
            )
            ''')
            self.connection.commit()
            logger.info(f"Table 'tbl_server' created successfully.")
        except sqlite3.Error as e:
            if len(e.args) and e.args[0].count('already exists'):
                return
            logger.error(f"Error creating table 'tbl_server': {e}")
            
    
    def get_qr_pay_code_by_qr_code(self, qr_code: str):
        self.cursor.execute("SELECT qr_code, id_server, channel_id, message_id, ngay_tao FROM qr_pay_code WHERE qr_code=?; ", (qr_code,))
        rows=self.cursor.fetchone()
        
        if rows:
            return QrPayCodeDTO(rows[0], rows[1], rows[2], rows[3], datetime_from_string(rows[4]))
        
        return None
        
    
    def get_all_qr_pay_code(self):
        self.cursor.execute("SELECT qr_code, id_server, channel_id, message_id, ngay_tao FROM qr_pay_code;")
        rows = self.cursor.fetchall()
        return [QrPayCodeDTO(qr_code, id_server, channel_id, message_id, datetime_from_string(ngay_tao)) for qr_code, id_server, channel_id, message_id, ngay_tao in rows]
    
    def insert_qr_pay_code(self, qr_pay: QrPayCodeDTO):
        self.cursor.execute("INSERT INTO qr_pay_code(qr_code, id_server, channel_id, message_id, ngay_tao) VALUES (?, ?, ?, ?, ?);", 
                            [
                                qr_pay.get_qr_code(),
                                qr_pay.get_id_server(),
                                qr_pay.get_channel_id(),
                                qr_pay.get_message_id(),
                                datetime_to_string(qr_pay.get_ngay_tao())
                            ])
        self.connection.commit()
        return True
    
    def delete_qr_pay_by_id(self, qr_code: str):
        self.cursor.execute('DELETE FROM qr_pay_code WHERE qr_code=?;', (qr_code,))
        self.connection.commit()
        return True
    