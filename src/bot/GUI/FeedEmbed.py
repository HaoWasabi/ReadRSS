import nextcord
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL

class FeedEmbed:
    def __init__(self, linkAtom_feed: str, link_emty: str):
        feed_emty_bll = FeedEmtyBLL()
        feed_emty_dto = feed_emty_bll.getFeedEmtyByLinkAtom_feedAndLink_emty(linkAtom_feed, link_emty)
        print(f"feed_emty_dto: {feed_emty_dto}")
        
        self.__link = feed_emty_dto.getFeed().getLink_feed()
        self.__logo = feed_emty_dto.getFeed().getLogo_feed()
        self.__footer_text = feed_emty_dto.getFeed().getDescription_feed()
        self.__title = feed_emty_dto.getFeed().getTitle_feed()
        self.__description = f'''
            [**Xem bài viết**]({feed_emty_dto.getEmty().getLink_emty()})
            {feed_emty_dto.getEmty().getDescription_emty()}
            '''
        self.__image = feed_emty_dto.getEmty().getImage_emty()

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

    # def __str__(self) -> str:
    #     return (f'''
    #         __ str __
    #         Title (title_feed): {embed.title}
    #         Description (title_emty + description_emty): 
    #         "{embed.description}"
    #         Image (image_emty): {embed.image.url}
    #         Author Name (title_feed): {embed.author.name}
    #         Author URL (link_feed): {embed.author.url}
    #         Author Icon URL (logo_feed): {embed.author.icon_url}
    #         ''')
