class ChannelDTO:
    def __init__(self, id_channel, name__channel):
        self.__id_channel = id_channel
        self.__name_channel = name__channel
        
    def __str__(self):
        return f"ChannelDTO(id_channel={self.__id_channel}, name_channel={self.__name_channel})"
    
    def setId_channel(self, id_channel):
        self.__id_channel = id_channel
    
    def setName_channel(self, name_channel):
        self.__name_channel = name_channel
        
    def getId_channel(self):
        return self.__id_channel
    
    def getName_channel(self):
        return self.__name_channel  