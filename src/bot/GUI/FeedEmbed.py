import nextcord
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL

class FeedEmbed:
    def __init__(self, linkAtom_feed: str, link_emty: str, colorText="BLUE"):
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
        self.__colorText = colorText
        self.__color = {
            "RED": "0xff0000",
            "ORANGE": "0xffa500",
            "YELLOW": "0xffff00",
            "GREEN": "0x008000",
            "BLUE": "0x00aaff",
            "PURPLE": "0x800080",
            "PINK": "0xffc0cb",
            "WHITE": "0xffffff",
            "GRAY": "0x808080",
            "BLACK": "0x000000"
        }

    def get_embed(self) -> nextcord.Embed:
        embed = nextcord.Embed(
            description=self.__description,
            color=int(self.__color[self.__colorText], 16)
        )
        if self.__image != "": 
            embed.set_image(url=self.__image)
        embed.set_image(url=self.__image)
        embed.set_author(name=self.__title, url=self.__link, icon_url=self.__logo)
        embed.set_footer(text=self.__footer_text, icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Facebook_Logo_%282019%29.png/600px-Facebook_Logo_%282019%29.png")
        return embed

    def __str__(self) -> str:
        embed = self.get_embed()
        return (f'''
            __ str __
            Title (title_feed): {embed.title}
            Description (title_emty + description_emty): 
            "{embed.description}"
            Image (image_emty): {embed.image.url}
            Author Name (title_feed): {embed.author.name}
            Author URL (link_feed): {embed.author.url}
            Author Icon URL (logo_feed): {embed.author.icon_url}
            ''')
