import sys, os, sqlite3
    
class Database:
    def __init__(self):
        # Sử dụng đường dẫn tuyệt đối đến tệp cơ sở dữ liệu
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # Lấy thư mục gốc của dự án
        db_path = os.path.join(base_dir, "db.sqlite3")
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        
    def drop_table(self, table_name):
        try:
            self.cursor.execute(f'''
            DROP TABLE IF EXISTS {table_name}
            ''')
            self.connection.commit()
            print(f"Table '{table_name}' dropped successfully.")
        except sqlite3.Error as e:
            print(f"Error dropping table: {e}")
            
    def delete_table(self, table_name):
        try:
            query = f"DELETE FROM {table_name}"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"All data in table '{table_name}' deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting all data: {e}")
            
    def clear(self):
        try: 
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            self.cursor.execute(query)
            tables = self.cursor.fetchall()

            # Xóa dữ liệu từ tất cả các bảng
            for table in tables:
                self.cursor.execute(f"DELETE FROM {table[0]};")
                print(f"Deleted all data from table {table[0]}")
            self.connection.commit()
            print("All data has been deleted.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")            

    def close_connection(self):
        self.connection.close()
        