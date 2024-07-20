from bot.DTO.EmtyDTO import EmtyDTO
from typing import Optional, List
import sqlite3
import os

class EmtyDAL:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, "db.sqlite3")
        self.__connection = sqlite3.connect(db_path)
        self.__cursor = self.__connection.cursor()
        self.create_table()

    def create_table(self):
        try:
            self.__cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_emty(
                    link_emty TEXT PRIMARY KEY,
                    title_emty TEXT,
                    description_emty TEXT,
                    image_emty TEXT,
                    pubDate_emty TEXT
                )
            ''')
            self.__connection.commit()
            print(f"Table 'tbl_emty' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table 'tbl_emty': {e}")

    def insertEmty(self, emty_dto: EmtyDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                INSERT INTO tbl_emty (link_emty, title_emty, description_emty, image_emty, pubDate_emty)
                VALUES (?, ?, ?, ?, ?)
                ''', (str(emty_dto.getLink_emty()), str(emty_dto.getTitle_emty()), str(emty_dto.getDescription_emty()), str(emty_dto.getImage_emty()), str(emty_dto.getPubDate_emty())))
                self.__connection.commit()
                print(f"Data inserted into 'tbl_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error inserting data into 'tbl_emty': {e}")
            return False

    def deleteEmtyByLink_emty(self, emty_link: str) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_emty WHERE link_emty = ?
                ''', (emty_link,))
                self.__connection.commit()
                print(f"Data deleted from 'tbl_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting data from 'tbl_emty': {e}")
            return False

    def deleteAllEmty(self) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                DELETE FROM tbl_emty
                ''')
                self.__connection.commit()
                print(f"All data deleted from 'tbl_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error deleting all data from 'tbl_emty': {e}")
            return False

    def updateEmtyByLink_emty(self, emty_link: str, emty_dto: EmtyDTO) -> bool:
        try:
            with self.__connection:
                self.__cursor.execute('''
                UPDATE tbl_emty
                SET link_emty = ?, title_emty = ?, description_emty = ?, image_emty = ?, pubDate_emty = ?
                WHERE link_emty = ?
                ''', (str(emty_dto.getLink_emty()), str(emty_dto.getTitle_emty()), str(emty_dto.getDescription_emty()), str(emty_dto.getImage_emty()), str(emty_dto.getPubDate_emty()), emty_link))
                self.__connection.commit()
                print(f"Data updated in 'tbl_emty' successfully.")
                return True
        except sqlite3.Error as e:
            print(f"Error updating in 'tbl_emty' data: {e}")
            return False

    def getEmtyByLink_emty(self, emty_link: str) -> Optional[EmtyDTO]:
        try:
            self.__cursor.execute('''
            SELECT * FROM tbl_emty WHERE link_emty = ?
            ''', (emty_link,))
            row = self.__cursor.fetchone()
            if row:
                return EmtyDTO(row[0], row[1], row[2], row[3], row[4])
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error fetching data from 'tbl_emty' by link_emty: {e}")
            return None

    def getAllEmty(self) -> List[EmtyDTO]:
        try:
            self.__cursor.execute('''
            SELECT * FROM tbl_emty
            ''')
            rows = self.__cursor.fetchall()
            if rows:
                return [EmtyDTO(row[0], row[1], row[2], row[3], row[4]) for row in rows]
            else:
                return []
        except sqlite3.Error as e:
            print(f"Error fetching all data from 'tbl_emty': {e}")
            return []

    def __del__(self):
        self.__connection.close()
