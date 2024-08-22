import os, sqlite3, sys
from typing import Optional, List
from ..DTO.channel_dto import ChannelDTO
from ..DTO.emty_dto import EmtyDTO
from ..DTO.channel_emty_dto import ChannelEmtyDTO
    
class ChannelEmtyDAL:
    def __init__(self):
        # Sử dụng đường dẫn tuyệt đối đến tệp cơ sở dữ liệu
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # Lấy thư mục gốc của dự án
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
    
    def insert_channel_emty(self, channel_emty_dto: ChannelEmtyDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                    INSERT INTO tbl_channel_emty (id_channel, link_emty)
                    VALUES (?, ?)
                ''', (channel_emty_dto.get_channel().get_id_channel(), channel_emty_dto.get_emty().get_link_emty()))
                self.__connection.commit()
                print(f"Data inserted into 'tbl_channel_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error inserting data into 'tbl_channel_emty': {e}")
            return False
        
    def delete_channel_emty_by_id_channel(self, id_channel: str) -> bool:   
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_channel_emty 
                WHERE id_channel = ? 
                ''', (id_channel,))
                self.__connection.commit()
                print(f"Data deleted from 'tbl_channel_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from 'tbl_channel_emty' {e}")
            return False
        
    def delete_channel_emty_by_id_channel_and_link_emty(self, id_channel: str, link_emty: str) -> bool:   
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
            
    def delete_all_channel_emty(self) -> bool:
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
            
    def get_channel_emty_by_id_channel_and_link_emty(self, id_channel: str, link_emty: str) -> Optional[ChannelEmtyDTO]:
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT f.id_channel, f.name_channel, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubdate_emty
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
        
    def get_all_channel_emty(self) -> List[ChannelEmtyDTO]:
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT f.id_channel, f.name_channel, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubdate_emty
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
