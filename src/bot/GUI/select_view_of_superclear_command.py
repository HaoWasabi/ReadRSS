import nextcord
from nextcord.ext import commands
from nextcord.ui import View, Select, Modal, TextInput
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
            nextcord.SelectOption(label="tbl", value="tbl", description="Clear a table in database.")
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
