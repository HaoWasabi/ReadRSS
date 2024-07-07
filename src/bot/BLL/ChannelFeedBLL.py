from bot.DTO.ChannelFeedDTO import ChannelFeedDTO 
from bot.DAL.ChannelFeedDAL import ChannelFeedDAL
from typing import Optional, List

class ChannelFeedBLL:
    def __init__(self):
        self.__channelFeedDAL = ChannelFeedDAL()
        
    def insertChannelFeed(self, channel_feed_dto: ChannelFeedDTO) -> bool:
        try:
            return self.__channelFeedDAL.insertChannelFeed(channel_feed_dto)
        except Exception as e:
            print(f"Error inserting ChannelFeed: {e}")
    
    def deleteChannelFeedById_channelAndLinkAtom_feed(self, id_channel: str, linkAtom_feed: str) -> bool:
        try:
            return self.__channelFeedDAL.deleteChannelFeedById_channelAndLinkAtom_feed(id_channel, linkAtom_feed)
        except Exception as e:
            print(f"Error deleting ChannelFeed: {e}")
            
    def deleteAllChannelFeed(self) -> bool:
        try:
            return self.__channelFeedDAL.deleteAllChannelFeed()
        except Exception as e:
            print(f"Error deleting all ChannelFeed: {e}")
            
    def updateChannelFeedById_channelAndLinkAtom_feed(self, id_channel: str, linkAtom_feed: str, channel_feed_dto: ChannelFeedDTO) -> bool:
        try:
            return self.__channelFeedDAL.updateChannelFeedById_channelAndLinkAtom_feed(id_channel, linkAtom_feed, channel_feed_dto)
        except Exception as e:
            print(f"Error updating ChannelFeed: {e}")
    
    def getChannelFeedById_channelAndLinkAtom_feed(self, id_channel: str, linkAtom_feed: str) -> Optional[ChannelFeedDTO]:
        try:
            return self.__channelFeedDAL.getChannelFeedById_channelAndLinkAtom_feed(id_channel, linkAtom_feed)
        except Exception as e:
            print(f"Error fetching ChannelFeed: {e}")
            
    def getAllChannelFeed(self) -> List[ChannelFeedDTO]:
        try:
            return self.__channelFeedDAL.getAllChannelFeed()
        except Exception as e:
            print(f"Error fetching all ChannelFeed: {e}")