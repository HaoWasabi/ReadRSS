import sys
import os
import sqlite3
from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.ChannelFeedDTO import ChannelFeedDTO
from typing import List, Optional

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
                CREATE TABLE IF NOT EXISTS tbl_channel_feed(
                    linkAtom_feed TEXT,
                    id_channel TEXT,
                    PRIMARY KEY (id_channel, linkAtom_feed),
                    FOREIGN KEY (id_channel) REFERENCES tbl_channel(id_channel),
                    FOREIGN KEY (linkAtom_feed) REFERENCES tbl_feed(linkAtom_feed)
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table `tbl_channel_feed`: {e}")

    def insertChannelFeed(self, channel_feed_dto: ChannelFeedDTO) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                INSERT INTO tbl_channel_feed (id_channel, linkAtom_feed)
                VALUES (?, ?)
                ''', (channel_feed_dto.getChannel().getId_channel(), channel_feed_dto.getFeed().getLinkAtom_feed()))
                self.connection.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error inserting data into `tbl_channel_feed`: {e}")
            return False

    def deleteChannelFeedById_channelAndLinkAtom_feed(self, id_channel: str, linkAtom_feed: str) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_channel_feed WHERE id_channel = ? AND linkAtom_feed = ?
                ''', (id_channel, linkAtom_feed))
                self.connection.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from `tbl_channel_feed`: {e}")
            return False

    def deleteAllChannelFeed(self) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_channel_feed
                ''')
                self.connection.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error deleting all data from `tbl_channel_feed`: {e}")
            return False
        
    def updateChannelFeedById_channelAndLinkAtom_feed(self, id_channel: str, linkAtom_feed: str, channel_feed_dto: ChannelFeedDTO) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                UPDATE tbl_channel_feed SET linkAtom_feed = ?, id_channel = ?
                WHERE linkAtom_feed = ? AND id_channel= ?
                ''', (channel_feed_dto.getFeed().getLinkAtom_feed(), channel_feed_dto.getChannel().getId_channel(), linkAtom_feed, id_channel))
                self.connection.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error updating data in `tbl_channel_feed`: {e}")
            return False

    def getChannelFeedById_channelAndLinkAtom_feed(self, id_channel: str, linkAtom_feed: str) -> Optional[ChannelFeedDTO]:
        try:
            self.cursor.execute('''
            SELECT c.id_channel, c.name_channel, 
                f.link_feed, f.linkAtom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed
            FROM tbl_channel_feed cf
            JOIN tbl_channel c ON cf.id_channel = c.id_channel
            JOIN tbl_feed f ON cf.linkAtom_feed = f.linkAtom_feed
            WHERE cf.linkAtom_feed = ? AND cf.id_channel = ?
            ''', (linkAtom_feed, id_channel))
            row = self.cursor.fetchone()
            if row:
                return ChannelFeedDTO(ChannelDTO(row[0], row[1]), 
                                   FeedDTO(row[2], row[3], row[4], row[5], row[6], row[7]))
            return None
        except sqlite3.Error as e:
            print(f"Error fetching data from `tbl_channel_feed` by link_emty: {e}")
            return None

    def getAllChannelFeed(self) -> List[ChannelFeedDTO]:
        try:
            self.cursor.execute('''
            SELECT c.id_channel, c.name_channel, 
                f.link_feed, f.linkAtom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed
            FROM tbl_channel_feed cf
            JOIN tbl_channel c ON cf.id_channel = c.id_channel
            JOIN tbl_feed f ON cf.linkAtom_feed = f.linkAtom_feed
            ''')
            rows = self.cursor.fetchall()
            return [ChannelFeedDTO(ChannelDTO(row[0], row[1]), 
                                   FeedDTO(row[2], row[3], row[4], row[5], row[6], row[7])) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching all data from `tbl_channel_feed`: {e}")
            return []

    def __del__(self):
        self.connection.close()