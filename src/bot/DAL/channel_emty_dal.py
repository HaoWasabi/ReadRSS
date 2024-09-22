# import sqlite3
# from typing import List, Optional
# from ..DTO.channel_dto import ChannelDTO
# from ..DTO.emty_dto import EmtyDTO
# from ..DTO.emty_dto import ChannelEmtyDTO
# from ..DTO.channel_emty_dto import ChannelEmtyDTO
# from .base_dal import BaseDAL, logger

# class ChannelEmtyDAL(BaseDAL):
#     def __init__(self):
#         super().__init__()
        
#     def create_table(self):
#         self.open_connection()
#         try:
#             self.cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS tbl_channel_emty(
#                     channel_id TEXT,
#                     link_emty TEXT,
#                     PRIMARY KEY (channel_id, link_emty, link_atom_feed, link_feed),
#                     FOREIGN KEY (channel_id) REFERENCES tbl_channel(channel_id),
#                     FOREIGN KEY (link_emty) REFERENCES tbl_emty(link_emty)
#                 )
#             ''')
#             self.connection.commit()
#             logger.info("Create tbl_channel_emty success")
#         except sqlite3.Error as e:
#             logger.error(f"Error creating table `tbl_channel_emty`: {e}")
#         finally:
#             self.close_connection()
            
#     def insert_channel_emty(self, channel_emty_dto: ChannelEmtyDTO):
#         self.open_connection()
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 INSERT INTO tbl_channel_emty (channel_id, link_emty)
#                 VALUES (?, ?, ?, ?)
#                 ''', (channel_emty_dto.get_channel().get_channel_id(), 
#                       channel_emty_dto.get_emty().get_link_emty()))
#                 self.connection.commit()
#                 return True
#         except sqlite3.IntegrityError as e:
#             logger.error(f"ChannelFeed with 'channel={channel_emty_dto.get_channel()} and 'emty={channel_emty_dto.get_emty()}' already exists in `tbl_channel_emty`")
#             return False
#         except sqlite3.Error as e:
#             logger.error(f"Error inserting data into `tbl_channel_emty`: {e}")
#             return False
#         finally:
#             self.close_connection()
            
#     def delete_channel_emty_by_channel_id(self, channel_id: str) -> bool:
#         self.open_connection()
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_channel_emty WHERE channel_id = ?
#                 ''', (channel_id,))
#                 self.connection.commit()
#                 logger.info(f"Data deleted from 'tbl_channel_emty' successfully.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting data from `tbl_channel_emty`: {e}")
#             return False
#         finally:
#             self.close_connection()
            
#     def delete_channel_emty_by_channel_id_and_link_atom_feed(self, channel_id: str, link_atom_feed: str) -> bool:
#         self.open_connection()
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_channel_emty WHERE channel_id = ? AND link_atom_feed = ?
#                 ''', (channel_id, link_atom_feed))
#                 self.connection.commit()
#                 logger.info(f"Data deleted from 'tbl_channel_emty' successfully.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting data from `tbl_channel_emty`: {e}")
#             return False
#         finally:
#             self.close_connection()
            
#     def delete_channel_emty_by_channel_id_and_link_feed(self, channel_id: str, link_feed: str) -> bool:
#         self.open_connection()
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_channel_emty WHERE channel_id = ? AND link_feed = ?
#                 ''', (channel_id, link_feed))
#                 self.connection.commit()
#                 logger.info(f"Data deleted from 'tbl_channel_emty' successfully.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting data from `tbl_channel_emty`: {e}")
#             return False
#         finally:
#             self.close_connection()
            
#     def delete_all_channel_emty(self) -> bool:
#         self.open_connection()
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_channel_emty
#                 ''')
#                 self.connection.commit()
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting all data from `tbl_channel_emty`: {e}")
#             return False
#         finally:
#             self.close_connection()
            
#     def get_all_channel_emty(self) -> List[ChannelEmtyDTO]:
#         self.open_connection()
#         try:
#             self.cursor.execute('''
#             SELECT c.channel_id, c.server_id, c.channel_name, c.is_active,
#                 f.link_emty, f.title_emty, f.description_emty, f.image_emty, f.pubdate_emty 
#             FROM tbl_channel_emty cf
#             JOIN tbl_channel c ON cf.channel_id = c.channel_id
#             JOIN tbl_emty f ON cf.link_emty = f.link_emty
#             ''')
#             rows = self.cursor.fetchall()
#             return [ChannelEmtyDTO(ChannelDTO(row[0], row[1], row[2], bool(row[3])),
#                                     EmtyDTO(row[4], row[5], row[6], row[7], row[8])) for row in rows]
#         except sqlite3.Error as e:
#             logger.error(f"Error fetching all data from `tbl_channel_emty`: {e}")
#             return []
#         finally:
#             self.close_connection()
            
#     def get_all_channel_emty_by_channel_id(self, channel_id: str) -> List[ChannelEmtyDTO]:
#         self.open_connection()
#         try:
#             self.cursor.execute('''
#             SELECT c.channel_id, c.server_id, c.channel_name, c.is_active,
#                 f.link_emty, f.title_emty, f.description_emty, f.image_emty, f.pubdate_emty 
#             FROM tbl_channel_emty cf
#             JOIN tbl_channel c ON cf.channel_id = c.channel_id
#             JOIN tbl_emty f ON cf.link_emty = f.link_emty
#             WHERE cf.channel_id = ?
#             ''', (channel_id,))
#             rows = self.cursor.fetchall()
#             return [ChannelEmtyDTO(ChannelDTO(row[0], row[1], row[2], bool(row[3])),
#                                     EmtyDTO(row[4], row[5], row[6], row[7], row[8])) for row in rows]
#         except sqlite3.Error as e:
#             logger.error(f"Error fetching all data from `tbl_channel_emty`: {e}")
#             return []
#         finally:
#             self.close_connection()
            
#     def get_channel_emty_by_channel_id_and_link_emty(self, channel_id: str, link_emty: str) -> Optional[ChannelEmtyDTO]:
#         self.open_connection()
#         try:
#             self.cursor.execute('''
#             SELECT c.channel_id, c.server_id, c.channel_name, c.is_active,
#                 f.link_emty, f.title_emty, f.description_emty, f.image_emty, f.pubdate_emty 
#             FROM tbl_channel_emty cf
#             JOIN tbl_channel c ON cf.channel_id = c.channel_id
#             JOIN tbl_emty f ON cf.link_emty = f.link_emty
#             WHERE cf.channel_id = ? and cf.link_emty = ?
#             ''', (channel_id, link_emty))
#             row = self.cursor.fetchone()
#             return ChannelEmtyDTO(ChannelDTO(row[0], row[1], row[2], bool(row[3])),
#                                     EmtyDTO(row[4], row[5], row[6], row[7], row[8]))
#         except sqlite3.Error as e:
#             logger.error(f"Error fetching all data from `tbl_channel_emty`: {e}")
#             return None
#         finally:
#             self.close_connection()
            