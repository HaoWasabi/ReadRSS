from typing import List, Optional
import sqlite3

from ..DTO.premium_dto import PremiumDTO
from ..DAL.base_dal import BaseDAL, logger


class PremiumDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        self.open_connection()
        try:
            self.cursor.execute('''
            CREATE TABLE tbl_premium(
                id_premium INTEGER PRIMARY KEY AUTOINCREMENT,
                price REAL,
                date_created TEXT,
                duration INTEGER,
                is_active INTEGER DEFAULT 1
            )
            ''')
            self.connection.commit()
            logger.info("Table 'tbl_premium' created successfully.")
        except sqlite3.Error as e:
            if "already exists" in str(e):
                logger.error(f"Table 'tbl_premium' already exists")
            else:
                logger.error(f"Error creating table 'tbl_premium': {e}")
        finally:
            self.close_connection()
            
    def insert_premium(self, premium: PremiumDTO) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                    INSERT INTO tbl_premium (price, date_created, duration)
                    VALUES (?, ?, ?)
                    ''', (premium.get_price(), premium.get_date_created(), premium.get_duration()))
                self.connection.commit()
                logger.info(f"Data inserted into 'tbl_premium' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error inserting data into 'tbl_premium': {e}")
            return False
        finally:
            self.close_connection()
        
    def delete_premium_by_id(self, premium_id) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                UPDATE tbl_premium
                SET is_active = 0
                WHERE id_premium = ?
                ''', (premium_id,))
                self.connection.commit()
                logger.info(f"Data deleted from 'tbl_premium' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting data from 'tbl_premium': {e}")
            return False
        finally:
            self.close_connection()
            
    def get_premium_by_id(self, premium_id) -> Optional[PremiumDTO]:
        self.open_connection()
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_premium WHERE id_premium = ?
            ''', (premium_id,))
            row = self.cursor.fetchone()
            if row:
                return PremiumDTO(row[0], row[1], row[2], row[3], bool(row[4]))
            else:
                return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching data from 'tbl_premium': {e}")
            return None
        finally:
            self.close_connection
            
    def get_all_premium(self, ignore_state=False, is_active=True) -> List[PremiumDTO]:
        self.open_connection()
        try:
            if ignore_state:
                self.cursor.execute('''
                SELECT * FROM tbl_premium
                ''')
            else:
                self.cursor.execute('''
                SELECT * FROM tbl_premium WHERE is_active = ?
                ''', (is_active,))
            rows = self.cursor.fetchall()
            if rows:
                return [PremiumDTO(row[0], row[1], row[2], row[3], bool(row[4])) for row in rows]
            else:
                return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching all data from 'tbl_premium': {e}")
            return []
        finally:
            self.close_connection()
        
            