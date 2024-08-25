from ..DTO.feed_emty_dto import FeedEmtyDTO
from ..GUI.custom_embed import CustomEmbed

class TestEmbed:
    def __init__(self, feed_emty_dto: FeedEmtyDTO, color = None):
        self.__feed_emty_dto = feed_emty_dto
        self.__link = self.__feed_emty_dto.get_feed().get_link_feed()
        self.__logo = self.__feed_emty_dto.get_feed().get_logo_feed()
        self.__footer_text = self.__feed_emty_dto.get_feed().get_description_feed()
        self.__title = self.__feed_emty_dto.get_feed().get_title_feed()
        self.__description = f'''
            [**Xem bài viết**]({self.__feed_emty_dto.get_emty().get_link_emty()})
            {self.__feed_emty_dto.get_emty().get_description_emty()}
            '''
        self.__image = self.__feed_emty_dto.get_emty().get_image_emty()
        self.__color = color
        
    def get_embed(self) -> CustomEmbed:
        embed = CustomEmbed(
            description = self.__description
        )
        if self.__image != "": 
            embed.set_image(url=self.__image)
        if self.__color is not None:
            embed.set_color(self.__color)
        embed.set_author(name=self.__title, url=self.__link, icon_url=self.__logo)
        embed.set_footer(text=self.__footer_text)
        return embed
    
    