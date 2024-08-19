import os, sqlite3, sys
from typing import List, Optional
from bot.dto.feed_dto import FeedDTO
from bot.dto.emty_dto import EmtyDTO
from bot.dto.feed_emty_dto import FeedEmtyDTO
    
class FeedEmtyDAL:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # Lấy thư mục gốc của dự án
        db_path = os.path.join(base_dir, "db.sqlite3")
        self.__connection = sqlite3.connect(db_path)
        self.__cursor = self.__connection.cursor()
        self.create_table()

    def create_table(self):
        try:
            self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_feed_emty(
                link_atom_feed TEXT,
                link_emty TEXT,
                PRIMARY KEY (link_atom_feed, link_emty),
                FOREIGN KEY (link_atom_feed) REFERENCES tbl_feed(link_atom_feed),
                FOREIGN KEY (link_emty) REFERENCES tbl_emty(link_emty)
            )
            ''')
            self.__connection.commit()
            print(f"Table 'tbl_feed_emty' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table 'tbl_feed_emty': {e}")

    def insert_feed_emty(self, feed_emty_dto: FeedEmtyDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                    INSERT INTO tbl_feed_emty (link_atom_feed, link_emty)
                    VALUES (?, ?)
                ''', (feed_emty_dto.get_feed().get_link_atom_feed(), feed_emty_dto.get_emty().get_link_emty()))
                self.__connection.commit()
                print(f"Data inserted into 'tbl_feed_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error inserting into 'tbl_feed_emty' data: {e}")
            return False

    def delete_feed_emty_by_link_atom_feed_and_link_emty(self, link_atom_feed: str, link_emty: str) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_feed_emty WHERE link_atom_feed = ? AND link_emty = ?
                ''', (link_atom_feed, link_emty))
                self.__connection.commit()
                print(f"Data deleted from 'tbl_feed_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from 'tbl_feed_emty': {e}")
            return False

    def delete_all_feed_emty(self) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''DELETE FROM tbl_feed_emty''')
                self.__connection.commit()
            print(f"All data deleted from 'tbl_feed_emty' successfully.")
            return True
        except sqlite3.Error as e:
            print(f"Error deleting all data from 'tbl_feed_emty': {e}")
            return False
        
    def get_feed_emty_by_link_atom_feed_and_link_emty(self, link_atom_feed: str, link_emty: str) -> Optional[FeedEmtyDTO]:
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_atom_feed = f.link_atom_feed
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                WHERE fe.link_atom_feed = ? AND fe.link_emty = ?
                ''', (link_atom_feed, link_emty))
                row = self.__cursor.fetchone()
                if row: 
                    return FeedEmtyDTO(FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]), 
                                       EmtyDTO(row[6], row[7], row[8], row[9], row[10]))
                else: 
                    return None
        except sqlite3.Error as e:
            print(f"Error fetching data from 'tbl_feed_emty': {e}")
            return None

    def get_all_feed_emty(self) -> List[FeedEmtyDTO]:
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_atom_feed = f.link_atom_feed
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                ''')
                rows = self.__cursor.fetchall()
                if rows:
                    return [FeedEmtyDTO(FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]), 
                                        EmtyDTO(row[6], row[7], row[8], row[9], row[10])) for row in rows]
                return []
        except sqlite3.Error as e:
            print(f"Error fetching all data from 'tbl_feed_emty': {e}")
            return []

    def __del__(self):
        self.__connection.close()
