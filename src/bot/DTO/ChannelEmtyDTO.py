class ChannelEmtyDTO:
    def __init__(self, channel_dto, emty_dto):
        self.__channel_dto = channel_dto
        self.__emty_dto = emty_dto
    
    def __str__(self):
        return f"ChannelEmtyDTO(channel={self.__channel_dto}, emty={self.__emty_dto})"
    
    def setChannel(self, channel_dto):
        self.__channel_dto = channel_dto
        
    def setEmty(self, emty_dto):
        self.__emty_dto = emty_dto
        
    def getChannel(self):
        return self.__channel_dto
    
    def getEmty(self):
        return self.__emty_dto
    