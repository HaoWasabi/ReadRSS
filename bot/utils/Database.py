import sys
import os
import sqlite3

# Thêm đường dẫn gốc của dự án vào sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

class Database:
    def __init__(self):
        # Sử dụng đường dẫn tuyệt đối đến tệp cơ sở dữ liệu
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, "db.sqlite3")
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        
    def create_table(self, table_name, columns):
        try:
            # Xây dựng câu truy vấn SQL từ từ điển columns
            columns_with_types = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
            query = f"CREATE TABLE {table_name} ({columns_with_types})"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Bảng '{table_name}' đã được tạo thành công.")
        except sqlite3.Error as e:
            print(f"Lỗi khi tạo bảng: {e}")
            
    def drop_table(self, table_name):
        try:
            self.cursor.execute(f'''
            DROP TABLE IF EXISTS {table_name}
            ''')
            self.connection.commit()
            print(f"Table '{table_name}' dropped successfully.")
        except sqlite3.Error as e:
            print(f"Error dropping table: {e}")
            
    def delete_all(self, table_name):
        try:
            query = f"DELETE FROM {table_name}"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"All data in table '{table_name}' deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting all data: {e}")
            
    def close_connection(self):
        self.connection.close()