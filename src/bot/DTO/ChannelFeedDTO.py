class ChannelFeedDTO:
    def __init__(self, channel_dto, feed_dto):
        self.__channel_dto = channel_dto
        self.__feed_dto = feed_dto

    def __str__(self):
        return f"ChannelFeedDTO(channel={self.__channel_dto}, feed={self.__feed_dto})"

    def setChannel(self, channel_dto):
        self.__channel_dto=channel_dto

    def setFeed(self, feed_dto):
        self.__feed_dto=feed_dto

    def getChannel(self):
        return self.__channel_dto

    def getFeed(self):
        return self.__feed_dto