from ..DTO.feed_emty_dto import FeedEmtyDTO
from ..GUI.custom_embed import CustomEmbed
from ..utils.text_processor import TextProcessor

class EmbedTest(CustomEmbed):
    def __init__(self, id_server: str, feed_emty_dto: FeedEmtyDTO, **kwargs):
        # Khởi tạo các thuộc tính
        self.__feed_emty_dto = feed_emty_dto
        self.__link = self.__feed_emty_dto.get_feed().get_link_feed()
        self.__logo = self.__feed_emty_dto.get_feed().get_logo_feed()
        self.__footer_text = self.__feed_emty_dto.get_feed().get_description_feed()
        self.__title = self.__feed_emty_dto.get_feed().get_title_feed()
        self.__image = ""  # Khởi tạo mặc định cho __image nếu không có ảnh

        # Gọi super để kế thừa khởi tạo từ lớp cha CustomEmbed
        super().__init__(id_server=id_server, description="", **kwargs)

        # Xử lý mô tả và link bài viết
        self.description = f'''
            [**Xem bài viết**]({feed_emty_dto.get_emty().get_link_emty()})
            {feed_emty_dto.get_emty().get_description_emty()}
        '''
        self.description = TextProcessor.clean_feed_text(self.description)

        # Kiểm tra nếu có image từ entry (emty)
        if feed_emty_dto.get_emty() is not None and feed_emty_dto.get_emty().get_image_emty() != "":
            self.__image = feed_emty_dto.get_emty().get_image_emty()
            self.set_image(url=self.__image)  # Cài đặt ảnh cho embed nếu có

        # Cài đặt các thông tin của Embed như author và footer
        self.set_author(name=self.__title, url=self.__link, icon_url=self.__logo)
        self.set_footer(text=self.__footer_text)
