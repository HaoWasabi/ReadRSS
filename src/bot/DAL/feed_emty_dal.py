import os, sqlite3, sys
from typing import List, Optional
from ..DTO.feed_dto import FeedDTO
from ..DTO.emty_dto import EmtyDTO
from ..DTO.feed_emty_dto import FeedEmtyDTO
from .base_dal import BaseDAL, logger

class FeedEmtyDAL(BaseDAL):
    def __init__(self):
        super().__init__()

    def create_table(self):
        try:
            self.cursor.execute('''
            CREATE TABLE tbl_feed_emty(
                link_atom_feed TEXT,
                link_emty TEXT,
                PRIMARY KEY (link_atom_feed, link_emty),
                FOREIGN KEY (link_atom_feed) REFERENCES tbl_feed(link_atom_feed),
                FOREIGN KEY (link_emty) REFERENCES tbl_emty(link_emty)
            )
            ''')
            self.connection.commit()
            logger.info(f"Table 'tbl_feed_emty' created successfully.")
        except sqlite3.Error as e:
            if len(e.args) and e.args[0].count('already exists'):
                return
            logger.error(f"Error creating table 'tbl_feed_emty': {e}")

    def insert_feed_emty(self, feed_emty_dto: FeedEmtyDTO) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO tbl_feed_emty (link_atom_feed, link_emty)
                    VALUES (?, ?) 
                ''', (feed_emty_dto.get_feed().get_link_atom_feed(), feed_emty_dto.get_emty().get_link_emty()))
                self.connection.commit()
                logger.info(f"Data inserted into 'tbl_feed_emty' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error inserting into 'tbl_feed_emty' data: {e}")
            return False

    def delete_feed_emty_by_link_atom_feed_and_link_emty(self, link_atom_feed: str, link_emty: str) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_feed_emty WHERE link_atom_feed = ? AND link_emty = ?
                ''', (link_atom_feed, link_emty))
                self.connection.commit()
                logger.info(f"Data deleted from 'tbl_feed_emty' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting data from 'tbl_feed_emty': {e}")
            return False
    
    def delete_feed_emty_by_link_feed_and_link_emty(self, link_feed: str, link_emty: str) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_feed_emty WHERE link_atom_feed IN (
                    SELECT link_atom_feed FROM tbl_feed WHERE link_feed = ?
                ) AND link_emty = ?
                ''', (link_feed, link_emty))
                self.connection.commit()
                logger.info(f"Data deleted from 'tbl_feed_emty' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting data from 'tbl_feed_emty': {e}")
            return False
    
    def delete_feed_emty_by_link_feed(self, link_feed: str) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''
                DELETE FROM tbl_feed_emty WHERE link_atom_feed IN (
                    SELECT link_atom_feed FROM tbl_feed WHERE link_feed = ?
                )''', (link_feed,))
                self.connection.commit()
                logger.info(f"Data deleted from 'tbl_feed_emty' successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting data from 'tbl_feed_emty': {e}")
            return False

    def delete_all_feed_emty(self) -> bool:
        try:
            with self.connection:
                self.cursor.execute('''DELETE FROM tbl_feed_emty''')
                self.connection.commit()
            logger.info(f"All data deleted from 'tbl_feed_emty' successfully.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting all data from 'tbl_feed_emty': {e}")
            return False
        
    def get_feed_emty_by_link_atom_feed_and_link_emty(self, link_atom_feed: str, link_emty: str) -> Optional[FeedEmtyDTO]:
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_atom_feed = f.link_atom_feed
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                WHERE fe.link_atom_feed = ? AND fe.link_emty = ?
                ''', (link_atom_feed, link_emty))
                row = self.cursor.fetchone()
                if row: 
                    return FeedEmtyDTO(FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]), 
                                       EmtyDTO(row[6], row[7], row[8], row[9], row[10]))
                else: 
                    return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching data from 'tbl_feed_emty': {e}")
            return None

    def get_all_feed_emty_by_link_atom_feed(self, link_atom_feed: str) -> List[FeedEmtyDTO]:
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_atom_feed = f.link_atom_feed
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                WHERE fe.link_atom_feed = ? 
                ''', (link_atom_feed,))
                rows = self.cursor.fetchall()
                if rows:
                    return [FeedEmtyDTO(FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]), 
                                        EmtyDTO(row[6], row[7], row[8], row[9], row[10])) for row in rows]
                return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching data from 'tbl_feed_emty': {e}")
            return []
        
    def get_all_feed_emty_by_link_feed(self, link_feed: str) -> List[FeedEmtyDTO]:
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_atom_feed = f.link_atom_feed
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                WHERE f.link_feed = ? 
                ''', (link_feed,))
                rows = self.cursor.fetchall()
                if rows:
                    return [FeedEmtyDTO(FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]), 
                                        EmtyDTO(row[6], row[7], row[8], row[9], row[10])) for row in rows]
                return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching data from 'tbl_feed_emty': {e}")
            return []
        
    def get_all_feed_emty(self) -> List[FeedEmtyDTO]:
        try:
            with self.connection:
                self.cursor.execute('''
                SELECT f.link_feed, f.link_atom_feed, f.title_feed, f.description_feed, f.logo_feed, f.pubDate_feed, 
                       e.link_emty, e.title_emty, e.description_emty, e.image_emty, e.pubDate_emty
                FROM tbl_feed_emty fe
                JOIN tbl_feed f ON fe.link_atom_feed = f.link_atom_feed
                JOIN tbl_emty e ON fe.link_emty = e.link_emty
                ''')
                rows = self.cursor.fetchall()
                if rows:
                    return [FeedEmtyDTO(FeedDTO(row[0], row[1], row[2], row[3], row[4], row[5]), 
                                        EmtyDTO(row[6], row[7], row[8], row[9], row[10])) for row in rows]
                return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching all data from 'tbl_feed_emty': {e}")
            return []

    
