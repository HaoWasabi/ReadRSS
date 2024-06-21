from bot.DAL.ChannelEmtyDAL import ChannelEmtyDAL

class ChannelEmtyBLL:
    def __init__(self):
        self.__channelEmtyDAL = ChannelEmtyDAL()
        
    def insertChannelEmty(self, channel_emty_dto):
        try:
            return self.__channelEmtyDAL.insertChannelEmty(channel_emty_dto)
        except Exception as e:
            print(f"Error inserting ChannelEmty: {e}")
    
    def deleteChannelEmtyById_channelAndLink_emty(self, id_channel, link_emty):
        try:
            return self.__channelEmtyDAL.deleteChannelEmtyById_channelAndLink_emty(id_channel, link_emty)
        except Exception as e:
            print(f"Error deleting ChannelEmty: {e}")
            
    def deleteAllChannelEmty(self):
        try:
            return self.__channelEmtyDAL.deleteAllChannelEmty()
        except Exception as e:
            print(f"Error deleting ChannelEmty: {e}")
            
    def updateChannelEmtyById_channelAndLink_emty(self, id_channel,link_emty, channel_emty_dto):
        try:
            return self.__channelEmtyDAL.updateChannelEmtyById_channelAndLink_emty(id_channel, link_emty, channel_emty_dto)
        except Exception as e:
            print(f"Error updating ChannelEmty: {e}")
    
    def getChannelEmtyById_channelAndLink_emty(self, id_channel, link_emty):
        try:
            return self.__channelEmtyDAL.getChannelEmtyById_channelAndLink_emty(id_channel, link_emty)
        except Exception as e:
            print(f"Error fetching ChannelEmty: {e}")
            
    def getAllChannelEmty(self):
        try:
            return self.__channelEmtyDAL.getAllChannelEmty()
        except Exception as e:
            print(f"Error fetchting ChannelEmty: {e}")