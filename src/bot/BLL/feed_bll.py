from ..BLL.singleton import Singleton
from ..DTO.feed_dto import FeedDTO
from ..DAL.feed_dal import FeedDAL
from typing import Optional, List


class FeedBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__feedDAL = FeedDAL()
            self._initialized = True

    def insert_feed(self, feed_dto: FeedDTO) -> bool:
        return self.__feedDAL.insert_feed(feed_dto)

    def delete_feed_by_link_atom_feed(self, linkAtom_feed: str) -> bool:
        return self.__feedDAL.delete_feed_by_link_atom_feed(linkAtom_feed)

    def delete_all_feed(self) -> bool:
        return self.__feedDAL.delete_all_feed()

    def update_feed_by_link_atom_feed(self, linkAtom_feed: str, feed_dto: FeedDTO) -> bool:
        return self.__feedDAL.update_feed_by_link_atom_feed(linkAtom_feed, feed_dto)

    def get_feed_by_link_atom_feed(self, linkAtom_feed: str) -> Optional[FeedDTO]:
        return self.__feedDAL.get_feed_by_link_atom_feed(linkAtom_feed)

    def get_all_feed(self) -> List[FeedDTO]:
        return self.__feedDAL.get_all_feed()
