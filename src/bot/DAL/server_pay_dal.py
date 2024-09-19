import sqlite3
from .base_dal import BaseDAL, logger
from ..DTO.server_pay_dto import ServerPayDTO

class ServerPayDAL(BaseDAL):
    def __init__(self):
        super().__init__()
        
    def create_table(self):
        self.open_connection()
        try:
            self.cursor.execute('''
            CREATE Table server_pay (
                server_id TEXT PRIMARY KEY,
                is_pay BOOLEAN DEFAULT 0
            )
            ''')
            self.connection.commit()
            logger.info(f"Table 'server_pay' created successfully.")
        except sqlite3.Error as e:
            if len(e.args) and e.args[0].count('already exists'):
                return
            logger.error(f"Error creating table 'server_pay': {e}")
        finally:
            self.close_connection()
    
    
    def insert_server_pay(self, server_pay: ServerPayDTO):
        self.open_connection()
        self.cursor.execute("""
                INSERT INTO server_pay(server_id, is_pay) VALUES (?, ?) 
                ON CONFLICT(server_id) DO UPDATE SET is_pay = excluded.is_pay;
            """, 
            (
                server_pay.get_server(), 
                server_pay.get_pay()
            )
        )
        self.connection.commit()
        self.close_connection()
        return True

    def update_server_pay(self, server_pay: ServerPayDTO):
        self.open_connection()
        self.cursor.execute("UPDATE server_pay SET is_pay=? WHERE server_id=?;", (server_pay.get_server(), server_pay.get_pay()))
        self.connection.commit()
        self.close_connection()
        return True
    
    def get_all_server_pay(self):
        self.open_connection()
        self.cursor.execute("SELECT server_id, is_pay FROM server_pay;")
        rows = self.cursor.fetchall()
        self.close_connection()
        return [ServerPayDTO(server_id, is_pay) for server_id, is_pay in rows]
    
    def get_server_pay_by_server_id(self, server_id: str):
        self.open_connection()
        self.cursor.execute("SELECT server_id, is_pay FROM server_pay Where server_id=?", (server_id,))
        rows = self.cursor.fetchone()
        self.close_connection()
        if rows:
            return ServerPayDTO(rows[0], rows[1])
        return None
    
    def delete_server_pay_by_server_id(self, server_id: str):
        self.open_connection()
        self.cursor.execute("DELETE FROM server_pay WHERE server_id=?;", (server_id,))
        self.connection.commit()
        self.close_connection()
        return True