from nextcord import Interaction
from nextcord.ui import TextInput, Modal
from ..BLL.feed_emty_bll import FeedEmtyBLL
from ..GUI.check_authorization import check_authorization


class ModalClearFeedEmty(Modal):
        def __init__(self, user):
            super().__init__(title="Clear Feed Emty")
            self.author = user
            self.link_feed = TextInput(label="Feed Link (Optional)", placeholder="Enter the feed link", required=False)
            self.link_atom_feed =TextInput(label="Feed link RSS (Optional)", placeholder="Enter the feed link RSS", required=False)
            self.link_emty = TextInput(label="Emty Link (Optional)", placeholder="Enter the emty link", required=False)
            self.add_item(self.link_feed)
            self.add_item(self.link_atom_feed)
            self.add_item(self.link_emty)
            
        async def callback(self, interaction: Interaction):
            if not await check_authorization(interaction, self.author):
                return
                
            feed_emty_bll = FeedEmtyBLL()
            if self.link_feed.value and not self.link_atom_feed.value and not self.link_emty.value:
                feed_emty_bll.delete_feed_emty_by_link_feed(str(self.link_feed.value))
            
            elif self.link_feed.value and not self.link_atom_feed.value and self.link_emty.value:
                feed_emty_bll.delete_feed_emty_by_link_feed_and_link_emty(str(self.link_feed.value), self.link_emty.value)
            
            elif not self.link_feed.value and self.link_atom_feed.value and self.link_emty.value:
                feed_emty_bll.delete_feed_emty_by_link_atom_feed_and_link_emty(str(self.link_atom_feed.value), self.link_emty.value)
              
            await interaction.response.send_message(
                f"Successfully delete feed emty by link feed **{self.link_feed.value}**.",
                ephemeral=True
                )