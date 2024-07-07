from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.FeedDTO import FeedDTO

class ChannelFeedDTO:
    def __init__(self, channel_dto: ChannelDTO, feed_dto: FeedDTO):
        self.__channel_dto = channel_dto
        self.__feed_dto = feed_dto

    def __str__(self) -> str:
        return f"ChannelFeedDTO(channel={self.__channel_dto}, feed={self.__feed_dto})"

    def setChannel(self, channel_dto: ChannelDTO) -> None:
        self.__channel_dto=channel_dto

    def setFeed(self, feed_dto: FeedDTO) -> None:
        self.__feed_dto=feed_dto

    def getChannel(self) -> ChannelDTO:
        return self.__channel_dto

    def getFeed(self) -> FeedDTO:
        return self.__feed_dto