import sys
import os
import sqlite3
from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.EmtyDTO import EmtyDTO
from typing import List, Optional
    
class FeedEmtyDAL:
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
            CREATE TABLE IF NOT EXISTS tbl_feed_emty(
                link_feed TEXT,
                link_emty TEXT,
                PRIMARY KEY (link_feed, link_emty),
                FOREIGN KEY (link_feed) REFERENCES tbl_feed(link_feed),
                FOREIGN KEY (link_emty) REFERENCES tbl_emty(link_emty)
            )
            ''')
            self.__connection.commit()
            print(f"Table 'tbl_feed_emty' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table 'tbl_feed_emty': {e}")

    def insertFeedEmty(self, feed_emty_dto: FeedEmtyDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                    INSERT INTO tbl_feed_emty (link_feed, link_emty)
                    VALUES (?, ?)
                ''', (feed_emty_dto.getFeed().getLink_feed(), feed_emty_dto.getEmty().getLink_emty()))
                self.__connection.commit()
                print(f"Data inserted into 'tbl_feed_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error inserting into 'tbl_feed_emty' data: {e}")
            return False
        
    def deleteFeedEmtyByLink_feedAndLink_emty(self, link_feed: str, link_emty: str) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_feed_emty WHERE link_feed = ? AND link_emty = ?
                ''', (link_feed, link_emty))
                self.__connection.commit()
                print(f"Data deleted from 'tbl_feed_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from 'tbl_feed_emty': {e}")
            return False

    def deleteAllFeedEmty(self) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''DELETE FROM tbl_feed_emty''')
                self.__connection.commit()
            print(f"All data deleted from 'tbl_feed_emty' successfully.")
            return True
        except sqlite3.Error as e:
            print(f"Error deleting all data from 'tbl_feed_emty': {e}")
            return False
        
    def updateFeedEmtyByLink_feedAndLink_emty(self, link_feed: str, link_emty: str, feed_emty_dto: FeedEmtyDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_feed_emty SET link_emty = ?, link_feed = ?
                WHERE link_emty = ? AND link_feed = ?
                ''', (feed_emty_dto.getEmty().getLink_emty(), feed_emty_dto.getFeed().getLink_feed(), link_feed, link_emty))
                self.__connection.commit()
                print(f"Data updated in 'tbl_feed_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error updating data in 'tbl_feed_emty' by link_emty: {e}")
            return False
        
    def getFeedEmtyByLink_feedAndLink_emty(self, link_feed: str, link_emty: str) -> Optional[FeedEmtyDTO]:
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT f.link_feed, f.linkAtom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_feed = f.link_feed
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                WHERE fe.link_feed = ? AND fe.link_emty = ?
                ''', (link_feed, link_emty))
                row = self.__cursor.fetchone()
                if row: 
                    return FeedEmtyDTO(FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]), 
                                   EmtyDTO(row[6], row[7], row[8], row[9], row[10]))
                else: 
                    return None
        except sqlite3.Error as e:
            print(f"Error fetching data from 'tbl_feed_emty' by link_feed: {e}")
            return None

    def getAllFeedEmty(self) -> List[FeedEmtyDTO]:
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT f.link_feed, f.linkAtom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_feed = f.link_feed
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

