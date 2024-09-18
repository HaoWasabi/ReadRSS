# import os, sqlite3, sys
# from typing import Optional, List
# from ..DTO.server_dto import ServerDTO
# from ..DTO.color_dto import ColorDTO
# from ..DTO.server_color_dto import ServerColorDTO
# from .base_dal import BaseDAL, logger

# class ServerColorDAL(BaseDAL):
#     def __init__(self):
#         super().__init__()
        
#     def create_table(self):
#         try:
#             self.cursor.execute('''
#             CREATE TABLE tbl_server_color(
#                 id_server TEXT PRIMARY KEY,
#                 hex_color TEXT,
#                 name_color TEXT,
#                 FOREIGN KEY (id_server) REFERENCES tbl_server(id_server)
#             )
#             ''')
#             self.connection.commit()
#             logger.info(f"Table 'tbl_server_color' created successfully.")
#         except sqlite3.Error as e:
#             if len(e.args) and e.args[0].count('already exists'):
#                 return
#             logger.error(f"Error creating table 'tbl_server_color': {e}")
    
#     def insert_server_color(self, server_color_dto: ServerColorDTO) -> bool:
#         try:
#             with self.connection:
#                 color_dto = server_color_dto.get_color()
#                 self.cursor.execute('''
#                     INSERT OR IGNORE INTO tbl_server_color (id_server, hex_color, name_color)
#                     VALUES (?, ?, ?)
#                     ''', (server_color_dto.get_server().get_id_server(), color_dto.get_hex_color(), color_dto.get_name_color()))
#                 self.connection.commit()
#                 logger.info(f"Data inserted successfully into 'tbl_server_color'.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error inserting data into 'tbl_server_color': {e}")
#             return False    
        
#     def delete_server_color_by_id_server(self, id_server: str) -> bool:
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_server_color
#                 WHERE id_server = ?
#                 ''', (id_server,))
#                 self.connection.commit()
#                 logger.info(f"Data deleted successfully from 'tbl_server_color'.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting data from 'tbl_server_color': {e}")
#             return False
    
#     def delete_all_server_color(self) -> bool:
#         try:
#             with self.connection:
#                 self.cursor.execute('''
#                 DELETE FROM tbl_server_color
#                 ''')
#                 self.connection.commit()
#                 logger.info(f"Data deleted successfully from 'tbl_server_color'.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error deleting data from 'tbl_server_color': {e}")
#             return False
        
#     def update_server_color_by_id_server(self, id_server: str, server_color_dto: ServerColorDTO) -> bool:
#         try:
#             with self.connection:
#                 color_dto = server_color_dto.get_color()
#                 self.cursor.execute('''
#                 UPDATE tbl_server_color
#                 SET hex_color = ?, name_color = ?
#                 WHERE id_server = ?
#                 ''', (color_dto.get_hex_color(), color_dto.get_name_color(), id_server))
#                 self.connection.commit()
#                 logger.info(f"Data updated successfully in 'tbl_server_color'.")
#                 return True
#         except sqlite3.Error as e:
#             logger.error(f"Error updating data in 'tbl_server_color': {e}")
#             return False
        
#     def get_server_color_by_id_server(self, id_server: str) -> Optional[ServerColorDTO]:
#         try:
#             self.cursor.execute('''
#             SELECT s.id_server, s.name_server, sc.name_color
#             FROM tbl_server_color sc
#             JOIN tbl_server s ON sc.id_server = s.id_server
#             WHERE s.id_server=?;
#             ''', (id_server,))
#             row = self.cursor.fetchone()
#             if row:
#                 server_color_dto = ServerColorDTO(ServerDTO(row[0], row[1]), ColorDTO(row[2]))
#                 return server_color_dto
#             return None

#         except sqlite3.Error as e:
#             logger.error(f"Error selecting data from 'tbl_server_color': {e}")
#             return None
        
#     def get_all_server_color(self) -> List[ServerColorDTO]:
#         try:
#             self.cursor.execute('''
#             SELECT s.id_server, s.name_server, sc.name_color
#             FROM tbl_server_color sc
#             JOIN tbl_server s ON sc.id_server = s.id_server
#             ''')
#             rows = self.cursor.fetchall()
#             server_color_dtos = []
#             for row in rows:
#                 server_color_dto = ServerColorDTO(ServerDTO(row[0], row[1]), ColorDTO(row[2]))
#                 server_color_dtos.append(server_color_dto)
#             return server_color_dtos
#         except sqlite3.Error as e:
#             logger.error(f"Error selecting data from 'tbl_server_color': {e}")
#             return []
        
    
