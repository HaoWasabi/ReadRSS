class ServerChannelDTO:
    def __init__(self, server_dto, channel_dto):
        self.__server_dto = server_dto
        self.__channel_dto = channel_dto
        
    def __str__(self):
        return f"ServerChannelDTO(server_dto={self.__server_dto}, channel_dto={self.__channel_dto})"
    
    def setServer_dto(self, server_dto):
        self.__server_dto = server_dto
        
    def setChannel_dto(self, channel_dto):
        self.__channel_dto = channel_dto
    
    def getServer_dto(self):
        return self.__server_dto
    
    def getChannel_dto(self):
        return self.__channel_dto