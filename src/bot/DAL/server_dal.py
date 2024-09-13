import os, sqlite3, sys
from typing import Optional, List
from ..DTO.server_dto import ServerDTO
from .base_dal import BaseDAL, logger

class ServerDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        try:
            self.cursor.execute('''
            CREATE TABLE tbl_server(
                id_server TEXT PRIMARY KEY,
                name_server TEXT
            )
            ''')
            self.connection.commit()
            logger.info(f"Table 'tbl_server' created successfully.")
        except sqlite3.Error as e:
            if len(e.args) and e.args[0].count('already exists'):
                return
            logger.error(f"Error creating table 'tbl_server': {e}")
            
    def insert_server(self, server_dto: ServerDTO) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO tbl_server (id_server, name_server)
                    VALUES (?, ?)
                    ''', (server_dto.get_id_server(), server_dto.get_name_server()))
                self.connection.commit()
                logger.info(f"Data inserted successfully into 'tbl_server'.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error inserting data into 'tbl_server': {e}")
            return False
            
    def delete_server_by_id_server(self, id_server: str) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_server
                WHERE id_server = ?
                ''', (id_server,))
                self.connection.commit()
                logger.info(f"Data deleted successfully from 'tbl_server'.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting data from 'tbl_server': {e}")
            return False
            
    def delete_all_server(self) -> bool:
        try:
            with self.connection:
                self.connection.execute('''
                DELETE FROM tbl_server
                ''')
                self.connection.commit()
                logger.info(f"All data deleted successfully from 'tbl_server'.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting all data from 'tbl_server': {e}")
            return False
        
    def update_server_by_id_server(self, id_server: str, server_dto: ServerDTO) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                UPDATE tbl_server
                SET id_server = ?, name_server = ?
                WHERE id_server = ?
                ''', (server_dto.get_id_server(), server_dto.get_name_server(), id_server))
                self.connection.commit()
                logger.info(f"Data updated successfully in 'tbl_server'.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error updating data by id_server in 'tbl_server': {e}")
            return False
            
    def get_server_by_id_server(self, id_server: str) -> Optional[ServerDTO]:
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_server
            WHERE id_server = ?
            ''', (id_server,))
            row = self.cursor.fetchone()
            if row:
                return ServerDTO(row[0], row[1])
            else:
                return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching data by id_server from 'tbl_server': {e}")
            return None
        
    def get_all_server(self) -> List[ServerDTO]:
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_server
            ''')
            rows = self.cursor.fetchall()
            if rows:
                return [ServerDTO(row[0], row[1]) for row in rows]
            else:
                return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching all data from 'tbl_server': {e}")
            return []
            
    
