import sqlite3
from typing import Optional, List
from ..DTO.emty_dto import EmtyDTO

from .base_dal import BaseDAL, logger


class EmtyDAL(BaseDAL):
    def __init__(self):
        super().__init__()

    def create_table(self):
        self.open_connection()
        try:
            self.cursor.execute('''
                CREATE TABLE tbl_emty(
                    link_emty TEXT PRIMARY KEY,
                    link_feed TEXT,
                    link_atom_feed,
                    title_emty TEXT,
                    description_emty TEXT,
                    image_emty TEXT,
                    pubdate_emty TEXT,
                    FOREIGN KEY (link_feed) REFERENCES tbl_feed(link_feed),
                    FOREIGN KEY (link_atom_feed) REFERENCES tbl_feed(link_atom_feed)
                )
            ''')
            self.connection.commit()
            logger.info(f"Table 'tbl_emty' created successfully.")
        except sqlite3.Error as e:
            if len(e.args) and e.args[0].count('already exists'):
                logger.error(f"Table 'tbl_emty' already exists")
            else:
                logger.error(f"Error creating table 'tbl_emty': {e}")
        finally:
            self.close_connection()

    def insert_emty(self, emty_dto: EmtyDTO) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                INSERT INTO tbl_emty (link_emty, link_feed, link_atom_feed, title_emty, description_emty, image_emty, pubdate_emty)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (emty_dto.get_link_emty(), emty_dto.get_link_feed(), emty_dto.get_link_atom_feed(),
                        emty_dto.get_title_emty(), emty_dto.get_description_emty(),emty_dto.get_image_emty(), emty_dto.get_pubdate_emty()))
                self.connection.commit()
                logger.info(f"Data inserted into 'tbl_emty' successfully.")
                return True
        except sqlite3.IntegrityError as e:
            logger.error(f"Emty with link_emty={emty_dto.get_link_emty()} already exists in 'tbl_emty'")
            return False
        except sqlite3.Error as e:
            logger.error(f"Error inserting data into 'tbl_emty': {e}")
            return False
        finally:
            self.close_connection()

    def delete_emty_by_link_emty(self, emty_link: str) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_emty WHERE link_emty = ?
                ''', (emty_link,))
                self.connection.commit()
                logger.info(f"Data deleted from 'tbl_emty' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting data from 'tbl_emty': {e}")
            return False
        finally:
            self.close_connection()
            
    def delete_all_emty(self) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_emty
                ''')
                self.connection.commit()
                logger.info(f"All data deleted from 'tbl_emty' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting all data from 'tbl_emty': {e}")
            return False
        self.close_connection()

    def update_emty_by_link_emty(self, emty_link: str, emty_dto: EmtyDTO) -> bool:
        self.open_connection()
        try:
            with self.connection:
                self.cursor.execute('''
                UPDATE tbl_emty
                SET link_emty = ?, link_feed = ?, link_atom_feed = ?,  title_emty = ?, description_emty = ?, image_emty = ?, pubdate_emty = ?
                WHERE link_emty = ?
                ''', (emty_dto.get_link_emty(), emty_dto.get_link_feed(), emty_dto.get_link_atom_feed(), emty_dto.get_title_emty(),
                        emty_dto.get_description_emty(), emty_dto.get_image_emty(), emty_dto.get_pubdate_emty()))
                self.connection.commit()
                logger.info(f"Data updated in 'tbl_emty' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error updating in 'tbl_emty' data: {e}")
            return False
        self.close_connection()

    def get_emty_by_link_emty(self, emty_link: str) -> Optional[EmtyDTO]:
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_emty WHERE link_emty = ?
            ''', (emty_link,))
            row = self.cursor.fetchone()
            if row:
                return EmtyDTO(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            else:
                return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching data from 'tbl_emty': {e}")
            return None

    def get_all_emty(self) -> List[EmtyDTO]:
        try:
            self.cursor.execute('''
            SELECT * FROM tbl_emty
            ''')
            rows = self.cursor.fetchall()
            if rows:
                return [EmtyDTO(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
            else:
                return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching all data from 'tbl_emty': {e}")
            return []

    
