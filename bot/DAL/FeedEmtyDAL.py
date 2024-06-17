import sys
import os
import sqlite3
from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.EmtyDTO import EmtyDTO

# Thêm đường dẫn gốc của dự án vào sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)
    
class FeedEmtyDAL:
    def __init__(self):
        # Sử dụng đường dẫn tuyệt đối đến tệp cơ sở dữ liệu
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, "db.sqlite3")
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_feed_emty(
                link_feed TEXT,
                link_emty TEXT,
                PRIMARY KEY (link_feed, link_emty),
                FOREIGN KEY (link_feed) REFERENCES tbl_feed(link_feed),
                FOREIGN KEY (link_emty) REFERENCES tbl_emty(link_emty)
            )
            ''')
            self.connection.commit()
            print(f"Table 'tbl_feed_emty' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def drop_table(self):
        try:
            table_name = "tbl_feed_emty"
            self.cursor.execute(f'''
            DROP TABLE IF EXISTS {table_name}
            ''')
            self.connection.commit()
            print(f"Table '{table_name}' dropped successfully.")
        except sqlite3.Error as e:
            print(f"Error dropping table: {e}")

    def insertFeedEmty(self, feed_emty_dto):
        try:
            with self.connection:
                self.cursor.execute('''
                    INSERT INTO tbl_feed_emty (link_feed, link_emty)
                    VALUES (?, ?)
                ''', (feed_emty_dto.getFeed().getLink_feed(), feed_emty_dto.getEmty().getLink_emty()))
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def deleteFeedEmtyByLink_feed(self, link_feed):
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_feed_emty WHERE link_feed = ?
                ''', (link_feed,))
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting data by link_feed: {e}")

    def deleteFeedEmtyByLink_emty(self, link_emty):
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_feed_emty WHERE link_emty = ?
                ''', (link_emty,))
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting data by link_emty: {e}")

    def deleteAllFeedEmty(self):
        try:
            with self.connection:
                self.cursor.execute('''DELETE FROM tbl_feed_emty''')
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting all data: {e}")
            
    def updateFeedEmtyByLink_feed(self, link_feed, feed_emty_dto):
        try:
            with self.connection:
                self.cursor.execute('''
                UPDATE tbl_feed_emty SET link_emty = ?, link_feed = ?
                WHERE link_feed = ?
                ''', (feed_emty_dto.getEmty().getLink_emty(), feed_emty_dto.getFeed().getLink_feed(), link_feed))
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating data by link_feed: {e}")

    def updateFeedEmtyByLink_emty(self, link_emty, feed_emty_dto):
        try:
            with self.connection:
                self.cursor.execute('''
                UPDATE tbl_feed_emty SET link_emty = ?, link_feed = ?
                WHERE link_emty = ?
                ''', (feed_emty_dto.getEmty().getLink_emty(), feed_emty_dto.getFeed().getLink_feed(), link_emty))
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating data by link_emty: {e}")

    def getFeedEmtyByLink_feed(self, link_feed):
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT f.link_feed, f.linkAtom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_feed = f.link_feed
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                WHERE fe.link_feed = ?
                ''', (link_feed,))
                rows = self.cursor.fetchall()
                return [FeedEmtyDTO(FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]), 
                                    EmtyDTO(row[6], row[7], row[8], row[9], row[10])) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching data by link_feed: {e}")
            return None

    def getFeedEmtyByLink_emty(self, link_emty):
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT f.link_feed, f.linkAtom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_feed = f.link_feed
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                WHERE fe.link_emty = ?
                ''', (link_emty,))
                rows = self.cursor.fetchall()
                return [FeedEmtyDTO(FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]), 
                                    EmtyDTO(row[6], row[7], row[8], row[9], row[10])) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching data by link_emty: {e}")
            return None

    def getAllFeedEmty(self):
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT f.link_feed, f.linkAtom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_feed = f.link_feed
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                ''')
                rows = self.cursor.fetchall()
                return [FeedEmtyDTO(FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]), 
                                    EmtyDTO(row[6], row[7], row[8], row[9], row[10])) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching all data: {e}")
            return []

    def __del__(self):
        self.connection.close()

