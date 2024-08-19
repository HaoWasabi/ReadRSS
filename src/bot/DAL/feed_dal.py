import os, sqlite3, sys
from typing import List, Optional
from bot.dto.feed_dto import FeedDTO
    
class FeedDAL:
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
            CREATE TABLE IF NOT EXISTS tbl_feed(
                link_feed TEXT,
                link_atom_feed TEXT PRIMARY KEY,
                title_feed TEXT,
                description_feed TEXT,
                logo_feed TEXT,
                pubdate_feed TEXT
            )
            ''')
            self.__connection.commit()
            print(f"Table 'tbl_feed' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table 'tbl_feed': {e}")
            
    def insert_feed(self, feed_dto: FeedDTO) -> bool: 
        try:
            with self.__connection:
                self.__cursor.execute('''
                    INSERT INTO tbl_feed (link_feed, link_atom_feed, title_feed, description_feed, logo_feed, pubdate_feed)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (feed_dto.get_link_feed(), feed_dto.get_link_atom_feed(), feed_dto.get_title_feed(), feed_dto.get_description_feed(), feed_dto.get_logo_feed(), feed_dto.get_pubdate_feed()))
                self.__connection.commit()
                print(f"Data inserted into 'tbl_feed' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error inserting data into 'tbl_feed': {e}")
            return False
            
    def delete_feed_by_link_atom_feed(self, link_atom_feed: str) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_feed WHERE link_atom_feed = ?
                ''', (link_atom_feed,))
                self.__connection.commit()
                print(f"Data deleted from 'tbl_feed' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from 'tbl_feed': {e}")
            return False
        
    def delete_all_feed(self) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_feed
                ''')
                self.__connection.commit()
                print(f"All data deleted into 'tbl_feed' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data into 'tbl_feed': {e}")
            return False
            
    def update_feed_by_link_atom_feed(self, link_atom_feed: str, feed_dto: FeedDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_feed SET link_feed = ?, link_atom_feed = ?, title_feed = ?, description_feed = ?, logo_feed = ?, pubdate_feed = ?
                WHERE link_atom_feed = ?
                ''', (feed_dto.get_link_feed(), feed_dto.get_link_atom_feed(), feed_dto.get_title_feed(), feed_dto.get_description_feed(), feed_dto.get_logo_feed(), feed_dto.get_pubdate_feed(), link_atom_feed))
                self.__connection.commit()
                print(f"Data updated in 'tbl_feed' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error updating data in 'tbl_feed': {e}")
            return False
            
    def get_feed_by_link_atom_feed(self, link_atom_feed: str) -> Optional[FeedDTO]:
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT * FROM tbl_feed WHERE link_atom_feed = ?
                ''', (link_atom_feed,))
                row = self.__cursor.fetchone()
                if row:
                    return FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5])
                return None
        except sqlite3.Error as e:
            print(f"Error fetching data from 'tbl_feed': {e}")
            return None
        
    def get_all_feed(self) -> List[FeedDTO]:
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT * FROM tbl_feed
                ''')
                rows = self.__cursor.fetchall()
                if rows:
                    return [FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
                else:
                    return []
        except sqlite3.Error as e:
            print(f"Error fetching all data from 'tbl_feed': {e}")
            return []
    
    def __del__(self):
        self.__connection.close()
