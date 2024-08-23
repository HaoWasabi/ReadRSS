import os, sqlite3, sys
from typing import Optional, List
from ..DTO.server_dto import ServerDTO
    
class ServerDAL:
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
            CREATE TABLE IF NOT EXISTS tbl_server(
                id_server TEXT PRIMARY KEY,
                name_server TEXT
            )
            ''')
            self.__connection.commit()
            print(f"Table 'tbl_server' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table 'tbl_server': {e}")
            
    def insert_server(self, server_dto: ServerDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                    INSERT INTO tbl_server (id_server, name_server)
                    VALUES (?, ?)
                    ''', (server_dto.get_id_server(), server_dto.get_name_server()))
                self.__connection.commit()
                print(f"Data inserted successfully into 'tbl_server'.")
            return True
        except sqlite3.Error as e:
            print(f"Error inserting data into 'tbl_server': {e}")
            return False
            
    def delete_server_by_id_server(self, id_server: str) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_server
                WHERE id_server = ?
                ''', (id_server,))
                self.__connection.commit()
                print(f"Data deleted successfully from 'tbl_server'.")
            return True
        except sqlite3.Error as e:
            print(f"Error deleting data from 'tbl_server': {e}")
            return False
            
    def delete_all_server(self) -> bool:
        try:
            with self.__connection:
                self.__connection.execute('''
                DELETE FROM tbl_server
                ''')
                self.__connection.commit()
                print(f"All data deleted successfully from 'tbl_server'.")
            return True
        except sqlite3.Error as e:
            print(f"Error deleting all data from 'tbl_server': {e}")
            return False
        
    def update_server_by_id_server(self, id_server: str, server_dto: ServerDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_server
                SET id_server = ?, name_server = ?
                WHERE id_server = ?
                ''', (server_dto.get_id_server(), server_dto.get_name_server(), id_server))
                self.__connection.commit()
                print(f"Data updated successfully in 'tbl_server'.")
            return True
        except sqlite3.Error as e:
            print(f"Error updating data by id_server in 'tbl_server': {e}")
            return False
            
    def get_server_by_id_server(self, id_server: str) -> Optional[ServerDTO]:
        try:
            self.__cursor.execute('''
            SELECT * FROM tbl_server
            WHERE id_server = ?
            ''', (id_server,))
            row = self.__cursor.fetchone()
            if row:
                return ServerDTO(row[0], row[1])
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error fetching data by id_server from 'tbl_server': {e}")
            return None
        
    def get_all_server(self) -> List[ServerDTO]:
        try:
            self.__cursor.execute('''
            SELECT * FROM tbl_server
            ''')
            rows = self.__cursor.fetchall()
            if rows:
                return [ServerDTO(row[0], row[1]) for row in rows]
            else:
                return []
        except sqlite3.Error as e:
            print(f"Error fetching all data from 'tbl_server': {e}")
            return []
            
    def __del__(self):
        self.__connection.close()
