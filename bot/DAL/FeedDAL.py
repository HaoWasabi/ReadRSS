import sys
import os
import sqlite3
from bot.DTO.FeedDTO import FeedDTO

# Thêm đường dẫn gốc của dự án vào sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)
    
class FeedDAL:
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
            CREATE TABLE IF NOT EXISTS tbl_feed(
                link_feed TEXT PRIMARY KEY,
                linkAtom_feed TEXT,
                title_feed TEXT,
                description_feed TEXT,
                logo_feed TEXT,
                pubDate_feed TEXT
            )
            ''')
            self.__connection.commit()
            print(f"Table 'tbl_feed' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            
    def drop_table(self):
        try:
            table_name = "tbl_feed"
            self.__cursor.execute(f'''
            DROP TABLE IF EXISTS {table_name}
            ''')
            self.__connection.commit()
            print(f"Table '{table_name}' dropped successfully.")
        except sqlite3.Error as e:
            print(f"Error dropping table: {e}")
            
    def insertFeed(self, feed_dto):
        try:
            with self.__connection:
                self.__cursor.execute('''
                    INSERT INTO tbl_feed (link_feed, linkAtom_feed, title_feed, description_feed, logo_feed, pubDate_feed)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (feed_dto.getLink_feed(), feed_dto.getLinkAtom_feed(), feed_dto.getTitle_feed(), feed_dto.getDescription_feed(), feed_dto.getLogo_feed(), feed_dto.getPubDate_feed()))
                self.__connection.commit()
                print(f"Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
     
    def deleteFeedByLink_feed(self, link_feed):
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_feed WHERE link_feed = ?
                ''', (link_feed,))
                self.__connection.commit()
                print(f"Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            
    def deleteFeedByLinkAtom_feed(self, linkAtom_feed):
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_feed WHERE linkAtom_feed = ?
                ''', (linkAtom_feed,))
                self.__connection.commit()
                print(f"Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            
    def deleteFeedByTitle_feed(self, title_feed):
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_feed WHERE title_feed = ?
                ''', (title_feed,))
                self.__connection.commit()
                print(f"Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
        
    def deleteAllFeed(self):
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_feed
                ''')
                self.__connection.commit()
                print(f"All data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            
    def updateFeedByLink_feed(self, link_feed, feed_dto):
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_feed SET link_feed = ?, linkAtom_feed = ?, title_feed = ?, description_feed = ?, logo_feed = ?, pubDate_feed = ?
                WHERE link_feed = ?
                ''', (feed_dto.getLink_feed(), feed_dto.getLinkAtom_feed(), feed_dto.getTitle_feed(), feed_dto.getDescription_feed(), feed_dto.getLogo_feed(), feed_dto.getPubDate_feed(), link_feed))
                self.__connection.commit()
                print(f"Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
            
    def updateFeedByLinkAtom_feed(self, linkAtom_feed, feed_dto):
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_feed SET linkAtom_feed = ?, title_feed = ?, description_feed = ?, logo_feed = ?, pubDate_feed = ?
                WHERE linkAtom_feed = ?
                ''', (feed_dto.getLinkAtom_feed(), feed_dto.getTitle_feed(), feed_dto.getDescription_feed(), feed_dto.getLogo_feed(), feed_dto.getPubDate_feed(), linkAtom_feed))
                self.__connection.commit()
                print(f"Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
            
    def updateFeedByTitle_feed(self, title_feed, feed_dto):
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_feed SET link_feed = ?, linkAtom_feed = ?, description_feed = ?, logo_feed = ?, pubDate_feed = ?
                WHERE title_feed = ?
                ''', (feed_dto.getLink_feed(), feed_dto.getLinkAtom_feed(), feed_dto.getDescription_feed(), feed_dto.getLogo_feed(), feed_dto.getPubDate_feed(), title_feed))
                self.__connection.commit()
                print(f"Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
            
    def getFeedByLink_feed(self, link_feed):
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT * FROM tbl_feed WHERE link_feed = ?
                ''', (link_feed,))
                row = self.__cursor.fetchone()
                if row:
                    return FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5])
                return None
        except sqlite3.Error as e:
            print(f"Error fetching data by link_feed: {e}")
            return None
        
    def getFeedByLinkAtom_feed(self, linkAtom_feed):
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT * FROM tbl_feed WHERE linkAtom_feed = ?
                ''', (linkAtom_feed,))
                row = self.__cursor.fetchone()
                if row:
                    return FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5])
                return None
        except sqlite3.Error as e:
            print(f"Error fetching data by linkAtom_feed: {e}")
            return None
        
    def getFeedByTitle_feed(self, title_feed):
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT * FROM tbl_feed WHERE title_feed = ?
                ''', (title_feed,))
                row = self.__cursor.fetchone()
                if row:
                    return FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5])
                return None
        except sqlite3.Error as e:
            print(f"Error fetching data by title_feed: {e}")
            return None
        
    def getAllFeed(self):
        try:
            with self.__connection:
                self.__cursor.execute('''
                SELECT * FROM tbl_feed
                ''')
                rows = self.__cursor.fetchall()
                return [FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching all data: {e}")
            return []
    
    def __del__(self):
        self.__connection.close()

