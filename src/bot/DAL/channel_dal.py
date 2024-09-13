import os, sqlite3, sys
from typing import Optional, List
from ..DTO.channel_dto import ChannelDTO

from .base_dal import BaseDAL, logger

class ChannelDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        try:
            self.cursor.execute('''
            CREATE TABLE tbl_channel(
                id_channel TEXT PRIMARY KEY,
                name_channel TEXT
            )
            ''')
            self.connection.commit()
            logger.info(f"Table 'tbl_channel' created successfully.")
        except sqlite3.Error as e:
            if len(e.args) and e.args[0].count('already exists'):
                return
            logger.error(f"Error creating table 'tbl_channel': {e}")
            
    def insert_channel(self, channel_dto: ChannelDTO) -> bool: 
        try:
            with self.connection:
                self.cursor.execute('''
                    INSERT INTO tbl_channel (id_channel, name_channel)
                    VALUES (?, ?)
                    ''', (channel_dto.get_id_channel(), channel_dto.get_name_channel()))
                self.connection.commit()
                logger.info(f"Data inserted into 'tbl_channel' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error inserting data into 'tbl_channel': {e}")
            return False

    def delete_channel_by_id_channel(self, id_channel: str) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_channel WHERE id_channel = ?
                ''', (id_channel,))
                self.connection.commit()
                logger.info(f"Data deleted from 'tbl_channel' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting data from 'tbl_channel': {e}")
            return False
            
    def delete_all_channel(self) -> bool:
        try:
            with self.connection:
                self.connection.execute('''
                DELETE FROM tbl_channel
                ''')
                self.connection.commit()
                logger.info(f"Data deleted from 'tbl_channel' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting from data 'tbl_channel': {e}")
            return False

    def update_channel_by_id_channel(self,id_channel: str, channel_dto: ChannelDTO) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                UPDATE tbl_channel
                SET id_channel = ?, name_channel = ?
                WHERE id_channel = ?
                ''', (channel_dto.get_id_channel(), channel_dto.get_name_channel(), id_channel))
                self.connection.commit()
                logger.info(f"Data updated in 'tbl_channel' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error updating data in 'tbl_channel': {e}")
            return False
            
    def get_channel_by_id_channel(self, id_channel: str) -> Optional[ChannelDTO]:
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_channel WHERE id_channel = ?
            ''', (id_channel,))
            row = self.cursor.fetchone()
            if row:
                return ChannelDTO(row[0], row[1])
            else:
                return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching data from 'tbl_channel' by link_channel: {e}")
            return None
 
    def get_all_channel(self) -> List[ChannelDTO]:
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_channel
            ''')
            rows = self.cursor.fetchall()
            if rows:
                return [ChannelDTO(row[0], row[1]) for row in rows]
            else:
                return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching all data from 'tbl_channel': {e}")
            return []


