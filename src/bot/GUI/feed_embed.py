import nextcord
from ..BLL.feed_emty_bll import FeedEmtyBLL

class FeedEmbed:
    def __init__(self, linkAtom_feed: str, link_emty: str):
        feed_emty_bll = FeedEmtyBLL()
        feed_emty_dto = feed_emty_bll.get_feed_emty_by_link_atom_feed_and_link_emty(linkAtom_feed, link_emty)
        print(f"feed_emty_dto: {feed_emty_dto}")
        
        
        # NOTE: cái này em không biết sử lý sao nữa
        if feed_emty_dto is None:
            return
        
        self.__link = feed_emty_dto.get_feed().get_link_feed()
        self.__logo = feed_emty_dto.get_feed().get_logo_feed()
        self.__footer_text = feed_emty_dto.get_feed().get_description_feed()
        self.__title = feed_emty_dto.get_feed().get_title_feed()
        self.__description = f'''
            [**Xem bài viết**]({feed_emty_dto.get_emty().get_link_emty()})
            {feed_emty_dto.get_emty().get_description_emty()}
            '''
        self.__image = feed_emty_dto.get_emty().get_image_emty()

    def get_embed(self) -> nextcord.Embed:
        embed = nextcord.Embed(
            description = self.__description
        )
        if self.__image != "": 
            embed.set_image(url=self.__image)
        embed.set_image(url=self.__image)
        embed.set_author(name=self.__title, url=self.__link, icon_url=self.__logo)
        embed.set_footer(text=self.__footer_text)
        return embed

