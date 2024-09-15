from ..BLL.feed_emty_bll import FeedEmtyBLL
from ..GUI.custom_embed import CustomEmbed
from ..utils.text_processor import TextProcessor

class EmbedFeed(CustomEmbed):  # Kế thừa từ CustomEmbed
    def __init__(self, id_server: str, link_atom_feed: str, link_emty: str, **kwargs):
        # Sử dụng FeedEmtyBLL để lấy FeedEmtyDTO dựa trên link_atom_feed và link_emty
        feed_emty_bll = FeedEmtyBLL()
        feed_emty_dto = feed_emty_bll.get_feed_emty_by_link_atom_feed_and_link_emty(link_atom_feed, link_emty)
        print(f"feed_emty_dto: {feed_emty_dto}")
        
        # Kiểm tra nếu feed_emty_dto không tồn tại
        if feed_emty_dto is None:
            return

        # Lưu trữ các thuộc tính cần thiết từ feed_emty_dto
        self.__id_server = id_server    
        self.__link = feed_emty_dto.get_feed().get_link_feed()
        self.__logo = feed_emty_dto.get_feed().get_logo_feed()
        self.__footer_text = feed_emty_dto.get_feed().get_description_feed()
        self.__title = feed_emty_dto.get_feed().get_title_feed()

        # Mô tả bài viết
        description = f'''
            [**Xem bài viết**]({feed_emty_dto.get_emty().get_link_emty()})
            {feed_emty_dto.get_emty().get_description_emty()}
        '''
        description = TextProcessor.clean_feed_text(description)  # Làm sạch nội dung

        # Ảnh (nếu có)
        self.__image = feed_emty_dto.get_emty().get_image_emty() if feed_emty_dto.get_emty().get_image_emty() else ""

        # Gọi constructor của lớp CustomEmbed với các tham số thích hợp
        super().__init__(
            id_server=self.__id_server,
            description=description,  # Đặt description ở đây
            **kwargs  # Truyền các đối số bổ sung nếu có
        )

        # Nếu có ảnh, thêm vào embed
        if self.__image != "":
            self.set_image(url=self.__image)
        
        # Đặt thông tin tác giả với tên, link và icon
        self.set_author(name=self.__title, url=self.__link, icon_url=self.__logo)

        # Đặt footer
        self.set_footer(text=self.__footer_text)

