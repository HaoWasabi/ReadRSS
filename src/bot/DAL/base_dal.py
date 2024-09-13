import  os, sqlite3
import logging

logger = logging.getLogger('dal')

class BaseDAL:
    def __init__(self):
        # Sử dụng đường dẫn tuyệt đối đến tệp cơ sở dữ liệu
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # Lấy thư mục gốc của dự án
        db_path = os.path.join(base_dir, "db.sqlite3")

        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        
    def create_table(self):
        pass
    
    
    def __del__(self):
        self.connection.close()
    