from bot.DAL.ChannelDAL import ChannelDAL

class ChannelBLL:
    def __init__(self):
        self.__channelDAL = ChannelDAL()
    
    def insertChannel(self, channel_dto):
        try:
            return self.__channelDAL.insertChannel(channel_dto)
        except Exception as e:
            print(f"Error inserting channel: {e}")

    def deleteChannelById_channel(self, channel_link):
        try:
            return self.__channelDAL.deleteChannelById_channel(channel_link)
        except Exception as e:
            print(f"Error deleting channel: {e}")
            
    def deleteAllChannel(self):
        try:
            return self.__channelDAL.deleteAllChannel()
        except Exception as e:
            print(f"Error deleting channel: {e}")

    def updateChannelById_channel(self, Channel_link, Channel_dto):
        try:
            return self.__channelDAL.updateChannelById_channel(Channel_link, Channel_dto)
        except Exception as e:
            print(f"Error updating Channel: {e}")
            
    def getChannelById_channel(self, Channel_link):
        try:
            return self.__channelDAL.getChannelById_channel(Channel_link)
        except Exception as e:
            print(f"Error fetching Channel: {e}")

    def getAllChannel(self):
        try:
            return self.__channelDAL.getAllChannel()
        except Exception as e:
            print(f"Error fetching Channel: {e}")
    