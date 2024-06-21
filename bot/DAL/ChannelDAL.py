import sys
import os
import sqlite3
from bot.DTO.ChannelDTO import ChannelDTO

class ChannelDAL:
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
            CREATE TABLE IF NOT EXISTS tbl_channel(
                id_channel TEXT PRIMARY KEY,
                name_channel TEXT
            )
            ''')
            self.__connection.commit()
            print(f"Table 'tbl_channel' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            
    def insertChannel(self, channel_dto):
        try:
            with self.__connection:
                self.__cursor.execute('''
                    INSERT INTO tbl_channel (id_channel, name_channel)
                    VALUES (?, ?)
                    ''', (channel_dto.getId_channel(), channel_dto.getName_channel()))
                self.__connection.commit()
                print(f"Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def deleteChannelById_channel(self, id_channel):
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_channel WHERE id_channel = ?
                ''', (id_channel,))
                self.__connection.commit()
                print(f"Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            
    def deleteAllChannel(self):
        try:
            with self.__connection:
                self.__connection.execute('''
                DELETE FROM tbl_channel
                ''')
                self.__connection.commit()
                print(f"Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")

    def updateChannelById_channel(self,id_channel, channel_dto):
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_channel
                SET id_channel = ?, name_channel = ?
                WHERE id_channel = ?
                ''', (channel_dto.getId_channel(), channel_dto.getName_channel(), id_channel))
                self.__connection.commit()
                print(f"Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
            
    def getChannelById_channel(self, id_channel):
        try:
            self.__cursor.execute('''
            SELECT * FROM tbl_channel WHERE id_channel = ?
            ''', (id_channel,))
            row = self.__cursor.fetchone()
            if row:
                return ChannelDTO(row[0], row[1])
            return None
        except sqlite3.Error as e:
            print(f"Error fetching data by link_channel: {e}")
            return None

        
    def getAllEmty(self):
        try:
            self.__cursor.execute('''
            SELECT * FROM tbl_channel
            ''')
            rows = self.__cursor.fetchall()
            if rows:
                return [ChannelDTO(row[0], row[1]) for row in rows]
            return []
        except sqlite3.Error as e:
            print(f"Error fetching all data: {e}")
            return []


    def __del__(self):
        self.__connection.close()
