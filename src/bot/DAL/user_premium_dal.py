from datetime import datetime
import sqlite3
from typing import List
from ..DAL.base_dal import BaseDAL, logger
from ..DTO.premium_dto import PremiumDTO
from ..DTO.user_dto import UserDTO
from ..DTO.user_premium_dto import UserPremiumDTO


class UserPremiumDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        self.create_table()
        
    def create_table(self):
        self.open_connection()
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_user_premium(
                user_id TEXT,
                premium_id INTEGER,
                date_registered DATETIME,
                PRIMARY KEY (user_id, premium_id, date_registered)
            )
            ''')
            self.connection.commit()
            logger.info(f"Table 'tbl_user_premium' created successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error creating table 'tbl_user_premium': {e}")
        finally:
            self.close_connection()
            
    def insert_user_premium(self, userpremium: UserPremiumDTO) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                    INSERT INTO tbl_user_premium (user_id, premium_id, date_registered)
                    VALUES (?, ?, ?)
                    ''', (userpremium.get_user().get_user_id(), userpremium.get_premium().get_premium_id(),
                            userpremium.get_date_registered()))
                self.connection.commit()
                logger.info(f"Data inserted into 'tbl_user_premium' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error inserting data into 'tbl_user_premium': {e}")
            return False
        finally:
            self.close_connection()

    def delete_user_premium_by_user_id_and_premium_id(self, user_id: str, premium_id: int) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                    DELETE FROM tbl_user_premium WHERE user_id = ? AND premium_id = ?
                ''', (user_id, premium_id))
                self.connection.commit()
                logger.info(f"Successfully deleted premium for User ID: {user_id}, Premium ID: {premium_id}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting data from 'tbl_user_premium': {e}")
            return False
        finally:
            self.close_connection()

    def get_all_userpremium(self) -> List[UserPremiumDTO]:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT u.user_id, u.user_name,
                    p.premium_id, p.name, p.description, p.price, p.date_created, p.duration, p.is_active,
                    up.date_registered
                FROM tbl_user_premium up
                JOIN tbl_user u on u.user_id = up.user_id
                JOIN tbl_premium p on p.premium_id = up.premium_id
                ''')
                rows = self.cursor.fetchall()
                if rows:
                    return [UserPremiumDTO(UserDTO(row[0], row[1]),
                            PremiumDTO(row[2], row[3], row[4], row[5], row[6], row[7], row[8]),
                                row[9]) for row in rows]
                else:
                    return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching all data from 'tbl_user_premium': {e}")
            return []
        finally:
            self.close_connection()
            
    def get_all_userpremium_by_user_id(self, user_id: str) -> List[UserPremiumDTO]:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT u.user_id, u.user_name,
                    p.premium_id, p.name, p.description, p.price, p.date_created, p.duration, p.is_active,
                    up.date_registered
                FROM tbl_user_premium up
                JOIN tbl_user u on u.user_id = up.user_id
                JOIN tbl_premium p on p.premium_id = up.premium_id
                WHERE up.user_id = ?
                ''', (user_id,))
                rows = self.cursor.fetchall()
                if rows:
                    return [UserPremiumDTO(UserDTO(row[0], row[1]),
                            PremiumDTO(row[2], row[3], row[4], row[5], row[6], row[7], row[8]),
                                row[9]) for row in rows]
                else:
                    return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching all data from 'tbl_user_premium': {e}")
            return []
        finally:
            self.close_connection()
            