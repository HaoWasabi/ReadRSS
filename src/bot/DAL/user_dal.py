import sqlite3
from typing import List, Optional
from ..DAL.base_dal import BaseDAL
from ..DTO.user_dto import UserDTO
from .base_dal import BaseDAL, logger

class UserDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        self.open_connection()
        try:
            self.cursor.execute('''
            CREATE TABLE tbl_user(
                user_id TEXT PRIMARY KEY,
                user_name TEXT
            )
            ''')
            self.connection.commit()
            logger.info(f"Table 'tbl_user' created successfully.")
        except sqlite3.Error as e:
            if "already exists" in str(e):
                logger.error(f"Table 'tbl_user' already exists")
            else:
                logger.error(f"Error creating table 'tbl_user': {e}")
        finally:
            self.close_connection()
            
    def insert_user(self, user_dto: UserDTO) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                    INSERT INTO tbl_user (user_id, user_name)
                    VALUES (?, ?)
                    ''', (user_dto.get_user_id(), user_dto.get_user_name()))
                self.connection.commit()
                logger.info(f"Data inserted into 'tbl_channel' successfully.")
                return True
        except sqlite3.IntegrityError as e:
            logger.error(f"User with user_id={user_dto.get_user_id()} already exists in 'tbl_user'")
            return False
        except sqlite3.Error as e:
            logger.error(f"Error inserting data into 'tbl_user': {e}")
            return False
        finally:
            self.close_connection()
            
    def update_user(self, user_dto: UserDTO) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                    UPDATE tbl_user
                    SET user_name = ?
                    WHERE user_id = ?
                    ''', (user_dto.get_user_name(), user_dto.get_user_id()))
                self.connection.commit()
                logger.info(f"Data updated in 'tbl_user' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error updating data in 'tbl_user': {e}")
            return False
        finally:
            self.close_connection()
            
    def get_all_user(self) -> List[UserDTO]:
        self.open_connection()
        try:
            self.cursor.execute('''SELECT * FROM tbl_server''')
            rows = self.cursor.fetchall()
            if rows:
                return [UserDTO(row[0], row[1]) for row in rows]
            else:
                return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching all data from 'tbl_user': {e}")
            return []
        finally:
            self.close_connection()
            
    def get_user_by_user_id(self, user_id: str) -> Optional[UserDTO]:
        self.open_connection()
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_user WHERE user_id = ?
            ''', (user_id,))
            row = self.cursor.fetchone()
            if row:
                return UserDTO(row[0], row[1])
            else:
                return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching data from 'tbl_user': {e}")
            return None
        finally:
            self.close_connection()