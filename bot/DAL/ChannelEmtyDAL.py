import sys
import os
import sqlite3
from bot.DTO.ChannelEmtyDTO import ChannelEmtyDTO
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.EmtyDTO import EmtyDTO

class ChannelEmtyDAL:
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
            CREATE TABLE IF NOT EXISTS tbl_channel_emty(
                id_channel TEXT,
                link_emty TEXT,
                PRIMARY KEY (id_channel, link_emty),
                FOREIGN KEY (id_channel) REFERENCES tbl_channel(id_channel),
                FOREIGN KEY (link_emty) REFERENCES tbl_emty(link_emty)
            )
            ''')
            self.__connection.commit()
            print(f"Table 'tbl_channel_emty' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
    
    def insertChannelEmty(self, channel_emty_dto):
        try:
            with self.__connection:
                self.__cursor.execute('''
                    INSERT INTO tbl_channel_emty (id_channel, link_emty)
                    VALUES (?, ?)
                ''', (channel_emty_dto.getChannel().getId_channel(), channel_emty_dto.getEmty().getLink_emty()))
                self.__connection.commit()
                print(f"Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            
    def deleteChannelEmtyById_channelAndLink_emty(self, id_channel, link_emty):
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_channel_emty 
                WHERE id_channel = ? AND link_emty = ?
                ''', (id_channel, link_emty))
                self.__connection.commit()
                print(f"Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            
    def deleteAllChannelEmty(self):
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_channel_emty
                ''')
                self.__connection.commit()
                print(f"Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting all data: {e}")
            
    def updateChannelEmtyById_channelAndLink_emty(self, id_channel, link_emty, channel_emty_dto):
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_channel_emty SET link_emty = ?, id_channel = ?
                WHERE id_channel = ? AND link_emty = ?
                ''', (channel_emty_dto.getEmty().getLink_emty(), channel_emty_dto.getChannel().getId_channel(), id_channel, link_emty))
                self.__connection.commit()
                print(f"Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")  
            
    def getChannelEmtyById_channelAndLink_emty(self, id_channel, link_emty):
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT f.id_channel, f.name_channel, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_channel_emty fe
                JOIN tbl_channel f ON fe.id_channel = f.id_channel
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                WHERE fe.id_channel = ? AND fe.link_emty = ? 
                ''', (id_channel, link_emty))
                row = self.__cursor.fetchone()
                return ChannelEmtyDTO(ChannelDTO(row[0], row[1]), 
                                    EmtyDTO(row[2], row[3], row[4], row[5], row[6]))
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None
        
    def getAllChannelEmty(self):
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT f.id_channel, f.name_channel, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_channel_emty fe
                JOIN tbl_channel f ON fe.id_channel = f.id_channel
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                ''')
                rows = self.__cursor.fetchall()
                if not rows:
                    print("No data found in tbl_channel_emty.")
                    return []
                return [ChannelEmtyDTO(ChannelDTO(row[0], row[1]), 
                                    EmtyDTO(row[2], row[3], row[4], row[5], row[6])) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return []
        
    def __del__(self):
        self.__connection.close()
