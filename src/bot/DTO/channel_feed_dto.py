from bot.dto.channel_dto import ChannelDTO
from bot.dto.feed_dto import FeedDTO

class ChannelFeedDTO:
    def __init__(self, channel_dto: ChannelDTO, feed_dto: FeedDTO):
        self.__channel_dto = channel_dto
        self.__feed_dto = feed_dto

    def __str__(self) -> str:
        return f"ChannelFeedDTO(channel={self.__channel_dto}, feed={self.__feed_dto})"

    def __eq__(self, other: object) -> bool:
        return self.__channel_dto == other.__channel_dto and self.__feed_dto == other.__feed_dto
    
    def set_channel(self, channel_dto: ChannelDTO) -> None:
        self.__channel_dto=channel_dto

    def set_feed(self, feed_dto: FeedDTO) -> None:
        self.__feed_dto=feed_dto

    def get_channel(self) -> ChannelDTO:
        return self.__channel_dto

    def get_feed(self) -> FeedDTO:
        return self.__feed_dto