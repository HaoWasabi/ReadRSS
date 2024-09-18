
from ..BLL.Singleton import Singleton
from ..DTO.channel_feed_dto import ChannelFeedDTO
from ..DAL.channel_feed_dal import ChannelFeedDAL
from typing import Optional, List


class ChannelFeedBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__channelFeedDAL = ChannelFeedDAL()
            self._initialized = True

    def insert_channel_feed(self, channel_feed_dto: ChannelFeedDTO) -> bool:
        return self.__channelFeedDAL.insert_channel_feed(channel_feed_dto)

    def delete_channel_feed_by_id_channel(self, id_channel: str) -> bool:
        return self.__channelFeedDAL.delete_channel_feed_by_id_channel(id_channel)

    def delete_channel_feed_by_id_channel_and_link_atom_feed(self, id_channel: str, linkAtom_feed: str) -> bool:
        return self.__channelFeedDAL.delete_channel_feed_by_id_channel_and_link_atom_feed(id_channel, linkAtom_feed)

    def delete_channel_feed_by_id_channel_and_link_feed(self, id_channel: str, link_feed: str) -> bool:
        return self.__channelFeedDAL.delete_channel_feed_by_id_channel_and_link_feed(id_channel, link_feed)

    def delete_all_channel_feed(self) -> bool:
        return self.__channelFeedDAL.delete_all_channel_feed()

    def get_channel_feed_by_id_channel_and_link_atom_feed(self, id_channel: str, linkAtom_feed: str) -> Optional[ChannelFeedDTO]:
        return self.__channelFeedDAL.get_channel_feed_by_id_channel_and_link_atom_feed(id_channel, linkAtom_feed)

    def get_all_channel_feed(self) -> List[ChannelFeedDTO]:
        return self.__channelFeedDAL.get_all_channel_feed()

    def get_all_channel_feed_by_id_channel(self, id_channel: str) -> List[ChannelFeedDTO]:
        return self.__channelFeedDAL.get_all_channel_feed_by_id_channel(id_channel)
