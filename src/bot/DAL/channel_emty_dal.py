# import os, sqlite3, sys
# from typing import Optional, List
# from ..DTO.channel_dto import ChannelDTO
# from ..DTO.emty_dto import EmtyDTO
# from ..DTO.channel_emty_dto import ChannelEmtyDTO
# from .base_dal import BaseDAL, logger
    
# class ChannelEmtyDAL(BaseDAL):
#     def __init__(self):
#         super().__init__()
        
#     def create_table(self):
#         try:
#             self.cursor.execute('''
#             CREATE TABLE tbl_channel_emty(
#                 id_channel TEXT,
#                 link_emty TEXT,
#                 PRIMARY KEY (id_channel, link_emty),
#                 FOREIGN KEY (id_channel) REFERENCES tbl_channel(id_channel),
#                 FOREIGN KEY (link_emty) REFERENCES tbl_emty(link_emty)
#             )
#             ''')
#             self.connection.commit()
#             logger.info(f"Table 'tbl_channel_emty' created successfully.")
#         except sqlite3.Error as e:
#             if len(e.args) and e.args[0].count('already exists'):
#                 return
#             logger.error(f"Error creating table 'tbl_channel_emty': {e}")
    
#     def insert_channel_emty(self, channel_emty_dto: ChannelEmtyDTO) -> bool:
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                     INSERT INTO tbl_channel_emty (id_channel, link_emty)
#                     VALUES (?, ?)
#                 ''', (channel_emty_dto.get_channel().get_id_channel(), channel_emty_dto.get_emty().get_link_emty()))
#                 self.connection.commit()
#                 logger.info(f"Data inserted into 'tbl_channel_emty' successfully.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error inserting data into 'tbl_channel_emty': {e}")
#             return False
        
#     def delete_channel_emty_by_id_channel(self, id_channel: str) -> bool:   
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_channel_emty 
#                 WHERE id_channel = ? 
#                 ''', (id_channel,))
#                 self.connection.commit()
#                 logger.info(f"Data deleted from 'tbl_channel_emty' successfully.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting data from 'tbl_channel_emty' {e}")
#             return False
        
#     def delete_channel_emty_by_id_channel_and_link_emty(self, id_channel: str, link_emty: str) -> bool:   
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_channel_emty 
#                 WHERE id_channel = ? AND link_emty = ?
#                 ''', (id_channel, link_emty))
#                 self.connection.commit()
#                 logger.info(f"Data deleted from 'tbl_channel_emty' successfully.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting data from 'tbl_channel_emty' {e}")
#             return False
            
#     def delete_all_channel_emty(self) -> bool:
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_channel_emty
#                 ''')
#                 self.connection.commit()
#                 logger.info(f"Data deleted from 'tbl_channel_emty' successfully.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting all data from 'tbl_channel_emty': {e}")
#             return False
            
#     def get_channel_emty_by_id_channel_and_link_emty(self, id_channel: str, link_emty: str) -> Optional[ChannelEmtyDTO]:
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 SELECT f.id_channel, f.name_channel, 
#                        e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubdate_emty
#                 FROM tbl_channel_emty fe
#                 JOIN tbl_channel f ON fe.id_channel = f.id_channel
#                 JOIN tbl_emty e ON fe.link_emty = e.link_emty
#                 WHERE fe.id_channel = ? AND fe.link_emty = ? 
#                 ''', (id_channel, link_emty))
#                 row = self.cursor.fetchone()
#                 if row:
#                     return ChannelEmtyDTO(ChannelDTO(row[0], row[1]), 
#                                     EmtyDTO(row[2], row[3], row[4], row[5], row[6]))
#                 else:
#                     return None
#         except sqlite3.Error as e:
#             logger.error(f"Error fetching data from 'tbl_channel_emty': {e}")
#             return None
        
#     def get_all_channel_emty(self) -> List[ChannelEmtyDTO]:
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 SELECT f.id_channel, f.name_channel, 
#                        e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubdate_emty
#                 FROM tbl_channel_emty fe
#                 JOIN tbl_channel f ON fe.id_channel = f.id_channel
#                 JOIN tbl_emty e ON fe.link_emty = e.link_emty
#                 ''')
#                 rows = self.cursor.fetchall()
#                 if rows:
#                     return [ChannelEmtyDTO(ChannelDTO(row[0], row[1]), 
#                                     EmtyDTO(row[2], row[3], row[4], row[5], row[6])) for row in rows]
#                 else: 
#                     return []
#         except sqlite3.Error as e:
#             logger.error(f"Error fetching data from 'tbl_channel_emty': {e}")
#             return []
        
#     def get_all_channel_emty_by_id_channel(self, id_channel: str) -> List[ChannelEmtyDTO]:
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 SELECT f.id_channel, f.name_channel, 
#                        e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubdate_emty
#                 FROM tbl_channel_emty fe
#                 JOIN tbl_channel f ON fe.id_channel = f.id_channel
#                 JOIN tbl_emty e ON fe.link_emty = e.link_emty
#                 WHERE fe.id_channel = ?
#                 ''', (id_channel,))
#                 rows = self.cursor.fetchall()
#                 if rows:
#                     return [ChannelEmtyDTO(ChannelDTO(row[0], row[1]), 
#                                     EmtyDTO(row[2], row[3], row[4], row[5], row[6])) for row in rows]
#                 else: 
#                     return []
#         except sqlite3.Error as e:
#             logger.error(f"Error fetching data from 'tbl_channel_emty': {e}")
#             return []
        
    
