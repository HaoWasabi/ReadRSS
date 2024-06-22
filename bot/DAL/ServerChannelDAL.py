import os
import sqlite3
from typing import Optional, List
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.ServerChannelDTO import ServerChannelDTO
from bot.DTO.ServerDTO import ServerDTO

class ServerChannelDAL:
    def __init__(self):
        # Sử dụng đường dẫn tuyệt đối đến tệp cơ sở dữ liệu
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, "db.sqlite3")
                
        self.__connection = sqlite3.connect(db_path)
        self.__cursor = self.__connection.cursor()
        self.create_table()
        
    def create_table(self):
        try:
            self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_server_channel(
                id_server TEXT,
                id_channel TEXT,
                PRIMARY KEY (id_server, id_channel),
                FOREIGN KEY (id_server) REFERENCES tbl_server(id_server),
                FOREIGN KEY (id_channel) REFERENCES tbl_channel(id_channel)
            )
            ''')
            self.__connection.commit()
            print(f"Table 'tbl_server_channel' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table 'tbl_server_channel': {e}")
            
    def insert_server_channel(self, server_channel_dto: ServerChannelDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                    INSERT INTO tbl_server_channel (id_server, id_channel)
                    VALUES (?, ?)
                    ''', (server_channel_dto.getServer().getId_server(), server_channel_dto.getChannel().getId_channel()))
                self.__connection.commit()
                print(f"Data inserted successfully into 'tbl_server_channel'.")
                return True
        except sqlite3.Error as e:
            print(f"Error inserting data into 'tbl_server_channel': {e}")
            return False
            
    def delete_server_channel_by_id_server_and_id_channel(
        self, id_server: str, id_channel: str
    ) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_server_channel
                WHERE id_server = ? AND id_channel = ?
                ''', (id_server, id_channel))
                self.__connection.commit()
                print(f"Data deleted successfully from 'tbl_server_channel'.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data by id_server and id_channel from 'tbl_server_channel': {e}")
            return False
            
    def delete_all_server_channel(self) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_server_channel
                ''')
                self.__connection.commit()
                print(f"All data deleted successfully from 'tbl_server_channel'.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting all data from 'tbl_server_channel': {e}")
            return False
            
    def update_server_channel_by_id_server_and_id_channel(
        self, id_server: str, id_channel: str, server_channel_dto: ServerChannelDTO
    ) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_server_channel
                SET id_server = ?, id_channel = ?
                WHERE id_server = ? AND id_channel = ?
                ''', (server_channel_dto.getServer().getId_server(), server_channel_dto.getChannel().getId_channel(), id_server, id_channel))
                self.__connection.commit()
                print(f"Data updated successfully in 'tbl_server_channel'.")
                return True
        except sqlite3.Error as e:
            print(f"Error updating data by id_server and id_channel in 'tbl_server_channel': {e}")
            return False
    
    def get_server_channel_by_id_server_and_id_channel(
        self, id_server: str, id_channel: str
    ) -> Optional[ServerChannelDTO]:
        try:
            self.__cursor.execute('''
            SELECT s.id_server, s.name_server,
                    c.id_channel, c.name_channel
            FROM tbl_server_channel sc
            JOIN tbl_server s ON sc.id_server = s.id_server
            JOIN tbl_channel c ON sc.id_channel = c.id_channel
            WHERE sc.id_server = ? AND sc.id_channel = ?
            ''', (id_server, id_channel))
            row = self.__cursor.fetchone()
            if row:
                return ServerChannelDTO(ServerDTO(row[0], row[1]), ChannelDTO(row[2], row[3]))
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error getting data by id_server and id_channel from 'tbl_server_channel': {e}")
            return None
    
    def get_all_server_channel(self) -> Optional[List[ServerChannelDTO]]:
        try:
            self.__cursor.execute('''
            SELECT s.id_server, s.name_server,
                    c.id_channel, c.name_channel
            FROM tbl_server_channel sc
            JOIN tbl_server s ON sc.id_server = s.id_server
            JOIN tbl_channel c ON sc.id_channel = c.id_channel
            ''')
            rows = self.__cursor.fetchall()
            if rows:
                return [ServerChannelDTO(ServerDTO(row[0], row[1]), ChannelDTO(row[2], row[3])) for row in rows]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error getting all data from 'tbl_server_channel': {e}")
            return None
            
    def __del__(self):
        self.__connection.close()
