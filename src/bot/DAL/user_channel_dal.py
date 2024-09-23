import sqlite3
from typing import List

from ..DTO import ChannelDTO, UserDTO, UserChannelDTO
from .base_dal import BaseDAL, logger


class UserChannelDAL(BaseDAL):
    def __init__(self):
        super().__init__()

    def create_table(self):
        self.open_connection()
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_user_channel(
                user_id TEXT,
                channel_id TEXT,
                date DATETIME,
                PRIMARY KEY (user_id, channel_id),
                FOREIGN KEY (user_id) REFERENCES tbl_user(user_id),
                FOREIGN KEY (channel_id) REFERENCES tbl_channel(channel_id)
            )
            ''')
            self.connection.commit()
            logger.info(f"Table 'tbl_user_channel' created successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error creating table 'tbl_user_channel': {e}")
        finally:
            self.close_connection()

    def insert_user_channel(self, userchannel_dto: UserChannelDTO) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                    INSERT INTO tbl_user_channel (user_id, channel_id, date)
                    VALUES (?, ?, ?)
                    ''', (userchannel_dto.user.user_id, userchannel_dto.channel.channel_id, userchannel_dto.date))
                self.connection.commit()
                logger.info(
                    f"Data inserted into 'tbl_user_channel' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error inserting data into 'tbl_user_channel': {e}")
            return False
        finally:
            self.close_connection()

    def get_all_user_channel(self) -> List[UserChannelDTO]:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT u.user_id, u.user_name,
                    c.channel_id, c.server_id, c.channel_name, c.is_active,
                    uc.date
                FROM tbl_user_channel uc
                JOIN tbl_user u on u.user_id = uc.user_id
                JOIN tbl_channel c on c.channel_id = uc.channel_id
                ''')
                rows = self.cursor.fetchall()
                if rows:
                    return [UserChannelDTO(UserDTO(row[0], row[1]),
                            ChannelDTO(row[2], row[3], row[4], bool(row[5])), row[6]) for row in rows]
                else:
                    return []
        except sqlite3.Error as e:
            logger.error(
                f"Error fetching all data from 'tbl_user_channel': {e}")
            return []
        finally:
            self.close_connection()

    def get_all_user_channel_by_user_id(self, user_id: str) -> List[UserChannelDTO]:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT u.user_id, u.user_name,
                    c.channel_id, c.server_id, c.channel_name, c.is_active,
                    uc.date
                FROM tbl_user_channel uc
                JOIN tbl_user u on u.user_id = uc.user_id
                JOIN tbl_channel c on c.channel_id = uc.channel_id
                WHERE uc.user_id = ?
                ''', (user_id,))
                rows = self.cursor.fetchall()
                if rows:
                    return [UserChannelDTO(UserDTO(row[0], row[1]),
                            ChannelDTO(row[2], row[3], row[4], bool(row[5])), row[6]) for row in rows]
                else:
                    return []
        except sqlite3.Error as e:
            logger.error(
                f"Error fetching all data from 'tbl_user_channel': {e}")
            return []
        finally:
            self.close_connection()

    def get_all_user_channel_by_channel_id(self, channel_id: str) -> List[UserChannelDTO]:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT u.user_id, u.user_name,
                    c.channel_id, c.server_id, c.channel_name, c.is_active,
                    uc.date
                FROM tbl_user_channel uc
                JOIN tbl_user u on u.user_id = uc.user_id
                JOIN tbl_channel c on c.channel_id = uc.channel_id
                WHERE uc.channel_id = ?
                ''', (channel_id,))
                rows = self.cursor.fetchall()
                if rows:
                    return [UserChannelDTO(UserDTO(row[0], row[1]),
                            ChannelDTO(row[2], row[3], row[4], bool(row[5])), row[6]) for row in rows]
                else:
                    return []
        except sqlite3.Error as e:
            logger.error(
                f"Error fetching all data from 'tbl_user_channel': {e}")
            return []
        finally:
            self.close_connection()

    def delete_user_channel_by_user_id_and_channel_id(self, user_id: str, channel_id: str) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_user_channel
                WHERE user_id = ? AND channel_id = ?
                ''', (user_id, channel_id))
                self.connection.commit()
                logger.info(
                    f"Data deleted from 'tbl_user_channel' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting data from 'tbl_user_channel': {e}")
            return False
        finally:
            self.close_connection()
