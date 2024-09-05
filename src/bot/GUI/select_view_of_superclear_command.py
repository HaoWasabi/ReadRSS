import nextcord
from nextcord.ext import commands
from nextcord.ui import View, Select, Modal, TextInput
from ..BLL.channel_bll import ChannelBLL
from ..BLL.channel_emty_bll import ChannelEmtyBLL
from ..BLL.feed_emty_bll import FeedEmtyBLL
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..utils.Database import dataBase

class SelectView(View):
    def __init__(self, user):
        super().__init__()
        self.author = user  # Store the user who initiated the interaction

    @nextcord.ui.select(
        placeholder="Choose a command category",
        options=[
            nextcord.SelectOption(label="all", value="all", description="Clear all database."),
            nextcord.SelectOption(label="tbl", value="tbl", description="Clear a table in database."),
            nextcord.SelectOption(label="channel_emty", value="channel_emty", description="Clear a channel emty in database."),
        ]
    )
    async def select_callback(self, select, interaction: nextcord.Interaction):
        if interaction.user != self.author:
            await interaction.response.send_message(
                "You are not authorized to use this select menu.",
                ephemeral=True
            )
            return

        if select.values[0] == "all":
            dataBase.clear()
            await interaction.response.send_message("Clear all database successfully.", ephemeral=True)
        elif select.values[0] == "tbl":
            # Tạo và hiển thị Modal để người dùng nhập tên bảng cần xóa
            modal = TableClearModal(interaction.user)  # Pass the user to the modal
            await interaction.response.send_modal(modal)
        elif select.values[0] == "channel_emty":
            # Tạo và hiển thị Modal để người dùng nhập id_channel và link_emty cần xóa
            modal = ChannelEmtyClearModal(interaction.user)
            await interaction.response.send_modal(modal)

class TableClearModal(Modal):
    def __init__(self, user):
        super().__init__(title="Clear Table")
        self.author = user  # Store the user who initiated the modal

        self.table_name = TextInput(
            label="Enter the table name you want to clear",
            placeholder="Table name",
            required=True
        )
        self.add_item(self.table_name)

    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user != self.author:
            await interaction.response.send_message(
                "You are not authorized to use this modal.",
                ephemeral=True
            )
            return

        table_name = self.table_name.value
        dataBase.delete_table(table_name)
        await interaction.response.send_message(f"Table '{table_name}' cleared successfully.", ephemeral=True)

class ChannelEmtyClearModal(Modal):
    def __init__(self, user):
        super().__init__(title="Clear Table")
        self.author = user  # Lưu thông tin người đã mở modal này

        self.id_channel = TextInput(
            label="Nhập ID kênh bạn muốn xóa",
            placeholder="ID kênh",
            required=True
        )
        self.add_item(self.id_channel)
        
        self.link_emty = TextInput(
            label="Nhập đường dẫn emty bạn muốn xóa (tuỳ chọn)",
            placeholder="Link emty",
            required=False
        )
        self.add_item(self.link_emty)
        
    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user != self.author:
            await interaction.response.send_message(
                "Bạn không có quyền sử dụng modal này.",
                ephemeral=True
            )
            return

        try:
            id_channel = self.id_channel.value
            link_emty = self.link_emty.value    
            
            channel_bll = ChannelBLL()
            channel_info = channel_bll.get_channel_by_id_channel(id_channel) # type: ignore

            # Kiểm tra nếu channel_info là None
            if channel_info is None:
                await interaction.response.send_message(f"Không tìm thấy kênh với ID `{id_channel}`.", ephemeral=True)
                return

            # Gọi phương thức get_name_channel() chỉ khi channel_info không phải là None
            name_channel = channel_info.get_name_channel()  # type: ignore
            
            # Thực hiện việc xóa theo id_channel và link_emty
            channel_emty_bll = ChannelEmtyBLL()
            
            if not link_emty:
                channel_emty_bll.delete_channel_emty_by_id_channel(id_channel) # type: ignore
            else:
                channel_emty_bll.delete_channel_emty_by_id_channel_and_link_emty(id_channel, link_emty) # type: ignore
                
            await interaction.response.send_message(f"Xóa lịch sử bài đăng trong kênh **{name_channel}** (`{id_channel}`) thành công.", ephemeral=True)
        
        except Exception as e:
            await interaction.response.send_message(f"Lỗi: {e}", ephemeral=True)
            print(f"Lỗi: {e}")
