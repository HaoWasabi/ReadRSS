class ChannelFeedDTO:
    def __init__(self, channel_dto, feed_dto):
        self.channel_dto= channel_dto
        self.feed_dto = feed_dto
        
    def __str__(self):
        return f"ChannelFeedDTO(channel={self.channel_dto}, feed={self.feed_dto})"
    
    def setChannel(self, channel_dto):
        self.channel_dto = channel_dto
        
    def setFeed(self, feed_dto):
        self.feed_dto = feed_dto
        
    def getChannel(self):
        return self.channel_dto
    
    def getFeed(self):
        return self.feed_dto