import sys
import os
import sqlite3
from bot.DTO.ChannelFeedDTO import ChannelFeedDTO

# Thêm đường dẫn gốc của dự án vào sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)


class ChannelFeedDAL:
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
                CREATE TABLE IF NOT EXISTS tbl_channelfeed(
                    link_feed TEXT,
                    id_server TEXT,
                    PRIMARY KEY (link_feed, id_server)
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insertChannelFeed(self, channelfeed_dto):
        try:
            with self.connection:
                self.cursor.execute('''
                INSERT INTO tbl_channelfeed (link_feed,id_server)
                VALUES (?, ?)
                ''', (channelfeed_dto.getLink_feed(), channelfeed_dto.getId_server()))
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def deleteChannelFeedByLink_feedAndId_server(self, link_feed,id_server):
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_channelfeed WHERE link_feed = ? AND id_server = ?
                ''', (link_feed,id_server,))
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")

    def deleteAllChannelFeed(self):
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_channelfeed
                ''')
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting all data: {e}")

    def updateChannelFeedByLink_feedAndId_server(self, link_feed,id_server, channelfeed_dto):
        try:
            with self.connection:
                self.cursor.execute('''
                UPDATE tbl_channelfeed
                SET link_feed = ?, id_server = ?
                WHERE link_feed = ? AND id_server= ?
                ''', (channelfeed_dto.getLink_feed(), channelfeed_dto.getId_server()))
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")

    def getChannelFeedByLink_feedAndId_server(self, link_feed,id_server):
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_channelfeed WHERE link_feed = ? AND id_server = ?
            ''', (link_feed,id_server,))
            row = self.cursor.fetchone()
            if row:
                return ChannelFeedDTO(row[0], row[1])
            return None
        except sqlite3.Error as e:
            print(f"Error fetching data by link_emty: {e}")
            return None

    def getAllChannelFeed(self):
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_channelfeed
            ''')
            rows = self.cursor.fetchall()
            return [ChannelFeedDTO(row[0], row[1]) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching all data: {e}")
            return []

    def __del__(self):
        self.connection.close()
