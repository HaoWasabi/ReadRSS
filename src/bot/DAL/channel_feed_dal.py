import os, sqlite3, sys
from typing import List, Optional
from ..DTO.channel_dto import ChannelDTO
from ..DTO.feed_dto import FeedDTO
from ..DTO.channel_feed_dto import ChannelFeedDTO

class ChannelFeedDAL:
    def __init__(self):
        # Sử dụng đường dẫn tuyệt đối đến tệp cơ sở dữ liệu
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # Lấy thư mục gốc của dự án
        db_path = os.path.join(base_dir, "db.sqlite3")
        
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_channel_feed(
                    link_atom_feed TEXT,
                    id_channel TEXT,
                    PRIMARY KEY (id_channel, link_atom_feed),
                    FOREIGN KEY (id_channel) REFERENCES tbl_channel(id_channel),
                    FOREIGN KEY (link_atom_feed) REFERENCES tbl_feed(link_atom_feed)
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table `tbl_channel_feed`: {e}")

    def insert_channel_feed(self, channel_feed_dto: ChannelFeedDTO) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                INSERT INTO tbl_channel_feed (id_channel, link_atom_feed)
                VALUES (?, ?)
                ''', (channel_feed_dto.get_channel().get_id_channel(), channel_feed_dto.get_feed().get_link_atom_feed()))
                self.connection.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error inserting data into `tbl_channel_feed`: {e}")
            return False
        
    def delete_channel_feed_by_id_channel(self, id_channel: str) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_channel_feed WHERE id_channel = ?
                ''', (id_channel,))
                self.connection.commit()
                print(f"Data deleted from 'tbl_channel_feed' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from `tbl_channel_feed`: {e}")
            return False
        
    def delete_channel_feed_by_id_channel_and_link_atom_feed(self, id_channel: str, link_atom_feed: str) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_channel_feed WHERE id_channel = ? AND link_atom_feed = ?
                ''', (id_channel, link_atom_feed))
                self.connection.commit()
                print(f"Data deleted from 'tbl_channel_feed' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from `tbl_channel_feed`: {e}")
            return False
        
    def delete_channel_feed_by_id_channel_and_link_feed(self, id_channel: str, link_feed: str) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                    DELETE FROM tbl_channel_feed 
                    WHERE id_channel = ? AND link_atom_feed IN (
                        SELECT link_atom_feed FROM tbl_feed WHERE link_feed = ?
                    )
                ''', (id_channel, link_feed))
                self.connection.commit()
                print(f"Data deleted from 'tbl_channel_feed' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from `tbl_channel_feed`: {e}")
            return False

    def delete_all_channel_feed(self) -> bool:
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

    def get_channel_feed_by_id_channel_and_link_atom_feed(self, id_channel: str, link_atom_feed: str) -> Optional[ChannelFeedDTO]:
        try:
            self.cursor.execute('''
            SELECT c.id_channel, c.name_channel, 
                f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubdate_feed
            FROM tbl_channel_feed cf
            JOIN tbl_channel c ON cf.id_channel = c.id_channel
            JOIN tbl_feed f ON cf.link_atom_feed = f.link_atom_feed
            WHERE cf.link_atom_feed = ? AND cf.id_channel = ?
            ''', (link_atom_feed, id_channel))
            row = self.cursor.fetchone()
            if row:
                return ChannelFeedDTO(ChannelDTO(row[0], row[1]), 
                                   FeedDTO(row[2], row[3], row[4], row[5], row[6], row[7]))
            return None
        except sqlite3.Error as e:
            print(f"Error fetching data from `tbl_channel_feed`: {e}")
            return None

    def get_all_channel_feed(self) -> List[ChannelFeedDTO]:
        try:
            self.cursor.execute('''
            SELECT c.id_channel, c.name_channel, 
                f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubdate_feed
            FROM tbl_channel_feed cf
            JOIN tbl_channel c ON cf.id_channel = c.id_channel
            JOIN tbl_feed f ON cf.link_atom_feed = f.link_atom_feed
            ''')
            rows = self.cursor.fetchall()
            return [ChannelFeedDTO(ChannelDTO(row[0], row[1]), 
                                   FeedDTO(row[2], row[3], row[4], row[5], row[6], row[7])) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching all data from `tbl_channel_feed`: {e}")
            return []

    def __del__(self):
        self.connection.close()