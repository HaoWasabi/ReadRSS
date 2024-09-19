import sqlite3
from typing import Optional, List
from ..DTO.channel_dto import ChannelDTO

from .base_dal import BaseDAL, logger

class ChannelDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        self.open_connection()
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_channel (
                id_channel TEXT PRIMARY KEY,
                id_server TEXT,
                name_channel TEXT,
                hex_color TEXT,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (id_server) REFERENCES tbl_server (id_server)
            )
            ''')
            self.connection.commit()
            logger.info(f"Table 'tbl_channel' created successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error creating table 'tbl_channel': {e}")
        finally:
            self.close_connection()
            
    def insert_channel(self, channel_dto: ChannelDTO) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                    INSERT INTO tbl_channel (id_channel, id_server, name_channel, hex_color)
                    VALUES (?, ?, ?, ?)
                    ''', (channel_dto.get_id_channel(), channel_dto.get_id_server(), channel_dto.get_name_channel(), channel_dto.get_hex_color()))
                self.connection.commit()
                logger.info(f"Data inserted into 'tbl_channel' successfully.")
                return True
        except sqlite3.IntegrityError as e:
            logger.error(f"Channel with id_channel={channel_dto.get_id_channel()} already exists in 'tbl_channel'")
            return False
        except sqlite3.Error as e:
            logger.error(f"Error inserting data into 'tbl_channel': {e}")
            return False
        finally:
            self.close_connection()

    def delete_channel_by_id_channel(self, id_channel: str) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                UPDATE tbl_channel
                SET ís_active = 0
                WHERE id_channel = ?
                ''', (id_channel,))
                self.connection.commit()
                logger.info(f"Data deleted from 'tbl_channel' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting data from 'tbl_channel': {e}")
            return False
        finally:
            self.close_connection()
            
    def delete_all_channel(self) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.connection.execute('''
                UPDATE tbl_channel
                SET is_active = 0
                ''')
                self.connection.commit()
                logger.info(f"All data deleted from 'tbl_channel' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting from data 'tbl_channel': {e}")
            return False
        finally:
            self.close_connection()

    def update_channel(self, channel_dto: ChannelDTO) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                UPDATE tbl_channel
                SET name_channel = ? , hex_color = ?, is_active = ?
                WHERE id_channel = ?
                ''', (channel_dto.get_name_channel(), channel_dto.get_hex_color(), channel_dto.get_state(), channel_dto.get_id_server()))
                self.connection.commit()
                logger.info(f"Data updated in 'tbl_channel' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error updating data in 'tbl_channel': {e}")
            return False
        finally:
            self.close_connection()
            
    def get_channel_by_id_channel(self, id_channel: str) -> Optional[ChannelDTO]:
        self.open_connection()
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_channel WHERE id_channel = ?
            ''', (id_channel,))
            row = self.cursor.fetchone()
            if row:
                return ChannelDTO(row[0], row[1], row[2], row[3], bool(row[4]))
            else:
                return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching data from 'tbl_channel' by link_channel: {e}")
            return None
        finally:
            self.close_connection()

    def get_all_channel(self, ignore_state=False, is_active=True) -> List[ChannelDTO]:
        self.open_connection()
        try:
            if ignore_state:
                self.cursor.execute('''
                SELECT * FROM tbl_channel
                ''')
            else:
                self.cursor.execute('''
                SELECT * FROM tbl_channel
                WHERE is_active = ?
                ''', (is_active,))
                
            rows = self.cursor.fetchall()
            if rows:
                return [ChannelDTO(row[0], row[1], row[2], row[3], bool(row[4])) for row in rows]
            else:
                return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching all data from 'tbl_channel': {e}")
            return []
        finally:
            self.close_connection()

