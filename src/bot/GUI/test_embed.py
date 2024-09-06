from ..DTO.feed_emty_dto import FeedEmtyDTO
from ..GUI.custom_embed import CustomEmbed
from ..utils.text_processor import TextProcessor

class TestEmbed:
    def __init__(self, id_server: str, feed_emty_dto: FeedEmtyDTO):
        self.__feed_emty_dto = feed_emty_dto
        self.__id_server = id_server
        self.__link = self.__feed_emty_dto.get_feed().get_link_feed()
        self.__logo = self.__feed_emty_dto.get_feed().get_logo_feed()
        self.__footer_text = self.__feed_emty_dto.get_feed().get_description_feed()
        self.__title = self.__feed_emty_dto.get_feed().get_title_feed()
        self.__description = f'''
            [**Xem bài viết**]({self.__feed_emty_dto.get_emty().get_link_emty()})
            {self.__feed_emty_dto.get_emty().get_description_emty()}
            '''
        self.__description = TextProcessor.clean_feed_text(self.__description)
        self.__image = self.__feed_emty_dto.get_emty().get_image_emty()
        
    def get_embed(self) -> CustomEmbed:
        embed = CustomEmbed(
            id_server = self.__id_server,
            description = self.__description
        )
        if self.__image != "": 
            embed.set_image(url=self.__image)
        embed.set_author(name=self.__title, url=self.__link, icon_url=self.__logo)
        embed.set_footer(text=self.__footer_text)
        return embed
    
    