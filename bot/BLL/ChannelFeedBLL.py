from bot.DAL.ChannelFeedDAL import ChannelFeedDAL

class ChannelFeedBLL:
    def __init__(self):
        self.__channelFeedDAL = ChannelFeedDAL()
        
    def insertChannelFeed(self, channel_feed_dto):
        try:
            return self.__channelFeedDAL.insertChannelFeed(channel_feed_dto)
        except Exception as e:
            print(f"Error inserting ChannelFeed: {e}")
    
    def deleteChannelFeedById_channelAndLink_feed(self, id_channel, link_feed):
        try:
            return self.__channelFeedDAL.deleteChannelFeedById_channelAndLink_feed(id_channel, link_feed)
        except Exception as e:
            print(f"Error deleting ChannelFeed: {e}")
            
    def deleteAllChannelFeed(self):
        try:
            return self.__channelFeedDAL.deleteAllChannelFeed()
        except Exception as e:
            print(f"Error deleting all ChannelFeed: {e}")
            
    def updateChannelFeedById_channelAndLink_feed(self, id_channel, link_feed, channel_feed_dto):
        try:
            return self.__channelFeedDAL.updateChannelFeedById_channelAndLink_feed(id_channel, link_feed, channel_feed_dto)
        except Exception as e:
            print(f"Error updating ChannelFeed: {e}")
    
    def getChannelFeedById_channelAndLink_feed(self, id_channel, link_feed):
        try:
            return self.__channelFeedDAL.getChannelFeedById_channelAndLink_feed(id_channel, link_feed)
        except Exception as e:
            print(f"Error fetching ChannelFeed: {e}")
            
    def getAllChannelFeed(self):
        try:
            return self.__channelFeedDAL.getAllChannelFeed()
        except Exception as e:
            print(f"Error fetching all ChannelFeed: {e}")