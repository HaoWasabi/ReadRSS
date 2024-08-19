from bot.dto.channel_feed_dto import ChannelFeedDTO 
from bot.dal.channel_feed_dal import ChannelFeedDAL
from typing import Optional, List

class ChannelFeedBLL:
    def __init__(self):
        self.__channelFeedDAL = ChannelFeedDAL()
        
    def insert_channel_feed(self, channel_feed_dto: ChannelFeedDTO) -> bool:
        try:
            return self.__channelFeedDAL.insert_channel_feed(channel_feed_dto)
        except Exception as e:
            print(f"Error inserting ChannelFeed: {e}")
            
    def delete_channel_feed_by_id_channel(self, id_channel: str) -> bool:
        try:
            return self.__channelFeedDAL.delete_channel_feed_by_id_channel(id_channel)
        except Exception as e:
            print(f"Error deleting ChannelFeed: {e}")
            
    def delete_channel_feed_by_id_channel_and_link_atom_feed(self, id_channel: str, linkAtom_feed: str) -> bool:
        try:
            return self.__channelFeedDAL.delete_channel_feed_by_id_channel_and_link_atom_feed(id_channel, linkAtom_feed)
        except Exception as e:
            print(f"Error deleting ChannelFeed: {e}")
            
    def delete_all_channel_feed(self) -> bool:
        try:
            return self.__channelFeedDAL.delete_all_channel_feed()
        except Exception as e:
            print(f"Error deleting all ChannelFeed: {e}")
    
    def get_channel_feed_by_id_channel_and_link_atom_feed(self, id_channel: str, linkAtom_feed: str) -> Optional[ChannelFeedDTO]:
        try:
            return self.__channelFeedDAL.get_channel_feed_by_id_channel_and_link_atom_feed(id_channel, linkAtom_feed)
        except Exception as e:
            print(f"Error fetching ChannelFeed: {e}")
            
    def get_all_channel_feed(self) -> List[ChannelFeedDTO]:
        try:
            return self.__channelFeedDAL.get_all_channel_feed()
        except Exception as e:
            print(f"Error fetching all ChannelFeed: {e}")