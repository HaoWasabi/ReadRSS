from nextcord import Interaction
from nextcord.ui import TextInput, Modal
from .check_authorization import check_authorization
from ..BLL.channel_bll import ChannelBLL
from ..BLL.channel_emty_bll import ChannelEmtyBLL

class ModalClearChannelEmty(Modal):
    def __init__(self, user):
        super().__init__(title="Clear Channel Emty")
        self.author = user
        self.id_channel = TextInput(label="Channel ID", placeholder="Enter the channel ID", required=True)
        self.link_emty = TextInput(label="Emty Link (Optional)", placeholder="Enter the emty link", required=False)
        self.add_item(self.id_channel)
        self.add_item(self.link_emty)

    async def callback(self, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        channel_bll = ChannelBLL()
        channel_info = channel_bll.get_channel_by_id_channel(str(self.id_channel.value))
        
        if channel_info is None:
            await interaction.response.send_message(f"Channel ID '{self.id_channel.value}' not found.", ephemeral=True)
            return

        name_channel = channel_info.get_name_channel() 
        channel_emty_bll = ChannelEmtyBLL()
        
        if not self.link_emty.value:
            channel_emty_bll.delete_channel_emty_by_id_channel(str(self.id_channel.value)) 
        
        else:
            channel_emty_bll.delete_channel_emty_by_id_channel_and_link_emty(str(self.id_channel.value), self.link_emty.value) 

        await interaction.response.send_message(
            f"Successfully cleared emty history in channel **{name_channel}** (`{self.id_channel.value}`).",
            ephemeral=True
        )