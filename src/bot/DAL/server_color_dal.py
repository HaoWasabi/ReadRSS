import os, sqlite3, sys
from typing import Optional, List
from ..DTO.server_dto import ServerDTO
from ..DTO.color_dto import ColorDTO
from ..DTO.server_color_dto import ServerColorDTO

class ServerColorDAL:
    def __init__(self):
        # Sử dụng đường dẫn tuyệt đối đến tệp cơ sở dữ liệu
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # Lấy thư mục gốc của dự án
        db_path = os.path.join(base_dir, "db.sqlite3")
        
        self.__connection = sqlite3.connect(db_path)
        self.__cursor = self.__connection.cursor()
        self.create_table()
        
    def create_table(self):
        try:
            self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS tbl_server_color(
                id_server TEXT PRIMARY KEY,
                hex_color TEXT,
                name_color TEXT,
                FOREIGN KEY (id_server) REFERENCES tbl_server(id_server)
            )
            ''')
            self.__connection.commit()
            print(f"Table 'tbl_server_color' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table 'tbl_server_color': {e}")
    
    def insert_server_color(self, server_color_dto: ServerColorDTO) -> bool:
        try:
            with self.__connection:
                color_dto = server_color_dto.get_color()
                self.__cursor.execute('''
                    INSERT INTO tbl_server_color (id_server, hex_color, name_color)
                    VALUES (?, ?, ?)
                    ''', (server_color_dto.get_server().get_id_server(), color_dto.get_hex_color(), color_dto.get_name_color()))
                self.__connection.commit()
                print(f"Data inserted successfully into 'tbl_server_color'.")
                return True
        except sqlite3.Error as e:
            print(f"Error inserting data into 'tbl_server_color': {e}")
            return False    
        
    def delete_server_color_by_id_server(self, id_server: str) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_server_color
                WHERE id_server = ?
                ''', (id_server,))
                self.__connection.commit()
                print(f"Data deleted successfully from 'tbl_server_color'.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from 'tbl_server_color': {e}")
            return False
    
    def delete_all_server_color(self) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_server_color
                ''')
                self.__connection.commit()
                print(f"Data deleted successfully from 'tbl_server_color'.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from 'tbl_server_color': {e}")
            return False
        
    def update_server_color_by_id_server(self, id_server: str, server_color_dto: ServerColorDTO) -> bool:
        try:
            with self.__connection:
                color_dto = server_color_dto.get_color()
                self.__cursor.execute('''
                UPDATE tbl_server_color
                SET hex_color = ?, name_color = ?
                WHERE id_server = ?
                ''', (color_dto.get_hex_color(), color_dto.get_name_color(), id_server))
                self.__connection.commit()
                print(f"Data updated successfully in 'tbl_server_color'.")
                return True
        except sqlite3.Error as e:
            print(f"Error updating data in 'tbl_server_color': {e}")
            return False
        
    def get_server_color_by_id_server(self, id_server: str) -> Optional[ServerColorDTO]:
        try:
            self.__cursor.execute('''
            SELECT s.id_server, s.name_server, sc.name_color
            FROM tbl_server_color sc
            JOIN tbl_server s ON sc.id_server = s.id_server
            WHERE sc.id_server = ?
            ''', (id_server,))
            row = self.__cursor.fetchone()
            if row:
                server_color_dto = ServerColorDTO(ServerDTO(row[0], row[1]), ColorDTO(row[2]))
                return server_color_dto
            return None
        except sqlite3.Error as e:
            print(f"Error selecting data from 'tbl_server_color': {e}")
            return None
        
    def get_all_server_color(self) -> List[ServerColorDTO]:
        try:
            self.__cursor.execute('''
            SELECT s.id_server, s.name_server, sc.name_color
            FROM tbl_server_color sc
            JOIN tbl_server s ON sc.id_server = s.id_server
            ''')
            rows = self.__cursor.fetchall()
            server_color_dtos = []
            for row in rows:
                server_color_dto = ServerColorDTO(ServerDTO(row[0], row[1]), ColorDTO(row[2]))
                server_color_dtos.append(server_color_dto)
            return server_color_dtos
        except sqlite3.Error as e:
            print(f"Error selecting data from 'tbl_server_color': {e}")
            return []
        
    def __del__(self):
        self.__connection.close()
