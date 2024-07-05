import sys
import os
import sqlite3
from bot.DTO.ChannelEmtyDTO import ChannelEmtyDTO
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.EmtyDTO import EmtyDTO
from typing import Optional, List

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
            print(f"Error creating table 'tbl_channel_emty': {e}")
    
    def insertChannelEmty(self, channel_emty_dto: ChannelEmtyDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                    INSERT INTO tbl_channel_emty (id_channel, link_emty)
                    VALUES (?, ?)
                ''', (channel_emty_dto.getChannel().getId_channel(), channel_emty_dto.getEmty().getLink_emty()))
                self.__connection.commit()
                print(f"Data inserted into 'tbl_channel_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error inserting data into 'tbl_channel_emty': {e}")
            return False
            
    def deleteChannelEmtyById_channel(self, id_channel: str) -> bool:   
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_channel_emty 
                WHERE id_channel = ? ''', (id_channel))
                self.__connection.commit()
                print(f"Data deleted from 'tbl_channel_emty' by id_channel successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from 'tbl_channel_emty' {e}")
            return False
        
    def deleteChannelEmtyById_channelAndLink_emty(self, id_channel: str, link_emty: str) -> bool:   
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_channel_emty 
                WHERE id_channel = ? AND link_emty = ?
                ''', (id_channel, link_emty))
                self.__connection.commit()
                print(f"Data deleted from 'tbl_channel_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from 'tbl_channel_emty' {e}")
            return False
            
    def deleteAllChannelEmty(self) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_channel_emty
                ''')
                self.__connection.commit()
                print(f"Data deleted from 'tbl_channel_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting all data from 'tbl_channel_emty': {e}")
            return False
            
    def updateChannelEmtyById_channelAndLink_emty(self, id_channel, link_emty: str, channel_emty_dto: ChannelEmtyDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_channel_emty SET link_emty = ?, id_channel = ?
                WHERE id_channel = ? AND link_emty = ?
                ''', (channel_emty_dto.getEmty().getLink_emty(), channel_emty_dto.getChannel().getId_channel(), id_channel, link_emty))
                self.__connection.commit()
                print(f"Data updated in 'tbl_channel_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error updating data in 'tbl_channel_emty': {e}")  
            return False
            
    def getChannelEmtyById_channelAndLink_emty(self, id_channel: str, link_emty: str) -> Optional[ChannelEmtyDTO]:
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
                if row:
                    return ChannelEmtyDTO(ChannelDTO(row[0], row[1]), 
                                    EmtyDTO(row[2], row[3], row[4], row[5], row[6]))
                else:
                    return None
        except sqlite3.Error as e:
            print(f"Error fetching data from 'tbl_channel_emty': {e}")
            return None
        
    def getAllChannelEmty(self) -> List[ChannelEmtyDTO]:
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
                if rows:
                    return [ChannelEmtyDTO(ChannelDTO(row[0], row[1]), 
                                    EmtyDTO(row[2], row[3], row[4], row[5], row[6])) for row in rows]
                else: 
                    return []
        except sqlite3.Error as e:
            print(f"Error fetching data from 'tbl_channel_emty': {e}")
            return []
        
    def __del__(self):
        self.__connection.close()
