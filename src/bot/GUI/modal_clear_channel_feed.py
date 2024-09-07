from nextcord import Interaction
from nextcord.ui import TextInput, Modal
from .check_authorization import check_authorization
from ..BLL.channel_bll import ChannelBLL
from ..BLL.channel_feed_bll import ChannelFeedBLL

class ModalClearChannelFeed(Modal):
    def __init__(self, user):
        super().__init__(title="Clear Channel Feed")
        self.author = user
        self.id_channel = TextInput(label="Channel ID", placeholder="Enter the channel ID", required=True)
        self.link_feed = TextInput(label="Feed Link (Optional)", placeholder="Enter the feed link", required=False)
        self.link_atom_feed = TextInput(label="Feed Link RSS (Optional)", placeholder="Enter the feed link RSS", required=False)
        self.add_item(self.id_channel)
        self.add_item(self.link_feed)
        self.add_item(self.link_atom_feed)
        
    async def callback(self, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return
        
        channel_bll = ChannelBLL()
        channel_info = channel_bll.get_channel_by_id_channel(str(self.id_channel.value))
        
        if channel_info is None:
            await interaction.response.send_message(f"Channel ID '{self.id_channel.value}' not found.", ephemeral=True)
            return

        name_channel = channel_info.get_name_channel()  
        channel_feed_bll = ChannelFeedBLL()
        
        if not self.link_feed.value and not self.link_atom_feed.value:
            channel_feed_bll.delete_channel_feed_by_id_channel(str(self.id_channel.value))  
        
        elif self.link_feed.value and not self.link_atom_feed.value:
            channel_feed_bll.delete_channel_feed_by_id_channel_and_link_feed(str(self.id_channel.value), self.link_feed.value)
        
        elif not self.link_feed.value and self.link_atom_feed.value:
            channel_feed_bll.delete_channel_feed_by_id_channel_and_link_atom_feed(str(self.id_channel.value), self.link_atom_feed.value)

        await interaction.response.send_message(
            f"Successfully feed setting for channel **{name_channel}** (`{self.id_channel.value}`).",
            ephemeral=True
        )