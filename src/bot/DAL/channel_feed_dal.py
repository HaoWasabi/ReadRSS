# import sqlite3
# from typing import List, Optional
# from ..DTO.channel_dto import ChannelDTO
# from ..DTO.feed_dto import FeedDTO
# from ..DTO.channel_feed_dto import ChannelFeedDTO
# from .base_dal import BaseDAL, logger

# class ChannelFeedDAL(BaseDAL):
#     def __init__(self):
#         super().__init__()

#     def create_table(self):
#         self.open_connection()
#         try:
#             self.cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS tbl_channel_feed(
#                     link_atom_feed TEXT,
#                     link_feed TEXT,
#                     channel_id TEXT,
#                     PRIMARY KEY (channel_id, link_atom_feed, link_feed),
#                     FOREIGN KEY (channel_id) REFERENCES tbl_channel(channel_id),
#                     FOREIGN KEY (link_atom_feed) REFERENCES tbl_feed(link_atom_feed),
#                     FOREIGN KEY (link_feed) REFERENCES tbl_feed(link_feed)
#                 )
#             ''')
#             self.connection.commit()
#             logger.info("Create tbl_channel_feed success")
#         except sqlite3.Error as e:
#             logger.error(f"Error creating table `tbl_channel_feed`: {e}")
#         finally:
#             self.close_connection()

#     def insert_channel_feed(self, channel_feed_dto: ChannelFeedDTO) -> bool:
#         self.open_connection()
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 INSERT INTO tbl_channel_feed (channel_id, link_feed, link_atom_feed)
#                 VALUES (?, ?, ?)
#                 ''', (channel_feed_dto.get_channel().get_channel_id(), channel_feed_dto.get_feed().get_link_feed(), channel_feed_dto.get_feed().get_link_atom_feed()))
#                 self.connection.commit()
#                 return True
#         except sqlite3.IntegrityError as e:
#             logger.error(f"ChannelFeed with 'channel={channel_feed_dto.get_channel()} and 'feed={channel_feed_dto.get_feed()}' already exists in `tbl_channel_feed`")
#             return False
#         except sqlite3.Error as e:
#             logger.error(f"Error inserting data into `tbl_channel_feed`: {e}")
#             return False
#         finally:
#             self.close_connection()
        
#     def delete_channel_feed_by_channel_id(self, channel_id: str) -> bool:
#         self.open_connection()
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_channel_feed WHERE channel_id = ?
#                 ''', (channel_id,))
#                 self.connection.commit()
#                 logger.info(f"Data deleted from 'tbl_channel_feed' successfully.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting data from `tbl_channel_feed`: {e}")
#             return False
#         finally:
#             self.close_connection()
        
#     def delete_channel_feed_by_channel_id_and_link_atom_feed(self, channel_id: str, link_atom_feed: str) -> bool:
#         self.open_connection()
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_channel_feed WHERE channel_id = ? AND link_atom_feed = ?
#                 ''', (channel_id, link_atom_feed))
#                 self.connection.commit()
#                 logger.info(f"Data deleted from 'tbl_channel_feed' successfully.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting data from `tbl_channel_feed`: {e}")
#             return False
#         finally:
#             self.close_connection()
        
#     def delete_channel_feed_by_channel_id_and_link_feed(self, channel_id: str, link_feed: str) -> bool:
#         self.open_connection()
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                     DELETE FROM tbl_channel_feed 
#                     WHERE channel_id = ? AND link_atom_feed IN (
#                         SELECT link_atom_feed FROM tbl_feed WHERE link_feed = ?
#                     )
#                 ''', (channel_id, link_feed))
#                 self.connection.commit()
#                 logger.info(f"Data deleted from 'tbl_channel_feed' successfully.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting data from `tbl_channel_feed`: {e}")
#             return False
#         finally:
#             self.close_connection()

#     def delete_all_channel_feed(self) -> bool:
#         self.open_connection()
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_channel_feed
#                 ''')
#                 self.connection.commit()
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting all data from `tbl_channel_feed`: {e}")
#             return False
#         finally:
#             self.close_connection()

#     def get_channel_feed_by_channel_id_and_link_atom_feed(self, channel_id: str, link_atom_feed: str) -> Optional[ChannelFeedDTO]:
#         self.open_connection()
#         try:
#             self.cursor.execute('''
#             SELECT c.channel_id, c.server_id, c.channel_name, c.is_active,
#                 f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubdate_feed
#             FROM tbl_channel_feed cf
#             JOIN tbl_channel c ON cf.channel_id = c.channel_id
#             JOIN tbl_feed f ON cf.link_atom_feed = f.link_atom_feed
#             WHERE cf.link_atom_feed = ? AND cf.channel_id = ?
#             ''', (link_atom_feed, channel_id))
#             row = self.cursor.fetchone()
#             if row:
#                 return ChannelFeedDTO(ChannelDTO(row[0], row[1], row[2], bool(row[3])),
#                                         FeedDTO(row[4], row[5], row[6], row[7], row[8], row[9]))
#             return None
#         except sqlite3.Error as e:
#             logger.error(f"Error fetching data from `tbl_channel_feed`: {e}")
#             return None
#         finally:
#             self.close_connection()

#     def get_all_channel_feed(self) -> List[ChannelFeedDTO]:
#         self.open_connection()
#         try:
#             self.cursor.execute('''
#             SELECT c.channel_id, c.server_id, c.channel_name, c.is_active,
#                 f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubdate_feed
#             FROM tbl_channel_feed cf
#             JOIN tbl_channel c ON cf.channel_id = c.channel_id
#             JOIN tbl_feed f ON cf.link_atom_feed = f.link_atom_feed
#             ''')
#             rows = self.cursor.fetchall()
#             return [ChannelFeedDTO(ChannelDTO(row[0], row[1], row[2], bool(row[3])),
#                                     FeedDTO(row[4], row[5], row[6], row[7], row[8], row[9])) for row in rows]
#         except sqlite3.Error as e:
#             logger.error(f"Error fetching all data from `tbl_channel_feed`: {e}")
#             return []
#         finally:
#             self.close_connection()

#     def get_all_channel_feed_by_channel_id(self, channel_id: str) -> List[ChannelFeedDTO]:
#         self.open_connection()
#         try:
#             self.cursor.execute('''
#             SELECT c.channel_id, c.server_id, c.channel_name, c.is_active,
#                 f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubdate_feed
#             FROM tbl_channel_feed cf
#             JOIN tbl_channel c ON cf.channel_id = c.channel_id
#             JOIN tbl_feed f ON cf.link_atom_feed = f.link_atom_feed
#             WHERE cf.channel_id = ?
#             ''', (channel_id,))
#             rows = self.cursor.fetchall()
#             return [ChannelFeedDTO(ChannelDTO(row[0], row[1], row[2], bool(row[3])),
#                                     FeedDTO(row[4], row[5], row[6], row[7], row[8], row[9])) for row in rows]
#         except sqlite3.Error as e:
#             logger.error(f"Error fetching all data from `tbl_channel_feed`: {e}")
#             return []
#         finally:
#             self.close_connection()
        
    