from nextcord import Interaction
from nextcord.ui import TextInput, Modal
from .check_authorization import check_authorization
from ..utils.Database import dataBase

class ModalClearTable(Modal):
    def __init__(self, user):
        super().__init__(title="Clear Table")
        self.author = user
        self.table_name = TextInput(label="Table Name", placeholder="Enter the table name", required=True)
        self.add_item(self.table_name)

    async def callback(self, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        dataBase.delete_table(self.table_name.value)
        await interaction.response.send_message(
            f"Table '{self.table_name.value}' cleared successfully.", 
            ephemeral=True
            )