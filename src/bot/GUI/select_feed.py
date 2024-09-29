import nextcord
from nextcord import SelectOption
from nextcord.ui import Select, View
from ..utils.check_authorization import check_authorization
from ..DTO.color_dto import ColorDTO
from ..DTO.feed_dto import FeedDTO
from ..BLL.feed_bll import FeedBLL
from ..BLL.channel_bll import ChannelBLL
from ..GUI.embed_custom import EmbedCustom
from ..GUI.modal_delete_channel_feed import ModalDeleteChannelFeed

class SelectFeed(View):
    def __init__(self, user, bot):
        super().__init__()
        self.author = user
        self.bot = bot
        self.color = int(ColorDTO("darkkhaki").get_hex_color().replace("#", ""), 16)

        self.select = Select(
            placeholder="Choose an option to change feed.",
            min_values=1,
            max_values=1,
            options=[
                SelectOption(label="delete", value="delete", description="Delete a feed."),
                SelectOption(label="show", value="show", description="Show list of feeds."),
            ]
        )

        self.add_item(self.select)
        self.select.callback = self.select_callback

    # Callback for Select
    async def select_callback(self, interaction: nextcord.Interaction):
        # Check for authorization
        if not await check_authorization(interaction, self.author):
            await interaction.followup.send("You are not authorized to use this command.", ephemeral=True)
            return

        selection = self.select.values[0]
        if selection == "delete":
             await interaction.response.send_modal(ModalDeleteChannelFeed(self.author))
        
        elif selection == "show":
            try:
                feed_bll = FeedBLL()
                channel_bll = ChannelBLL()
                id_server = str(interaction.guild.id) if interaction.guild else "Unknown"
                server_data = {}
                num = 0
                
                for feed_dto in feed_bll.get_all_feed():
                    channel_id = int(feed_dto.get_channel_id())
                    channel = self.bot.get_channel(channel_id)
                    channel_dto = channel_bll.get_channel_by_channel_id(str(channel_id))
                    
                    if channel:  # Kiểm tra xem kênh có tồn tại không
                        for server in self.bot.guilds:
                            if channel in server.channels:
                                server_name = f"**Server:** {server.name} ({server.id})"
                                channel_info = f"- **{channel_dto.get_channel_name()}** (`{channel_id}`) - [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})" # type: ignore
                                server_data.setdefault(server_name, []).append(channel_info)
                                num += 1
                
                # Tạo nội dung cho embed
                embed = EmbedCustom(
                    id_server=id_server,
                    title="List of Feeds in Channels",
                    description=f"You have {num} feeds in channels:",
                    color=self.color
                )
                
                for server_name, channels in server_data.items():
                    embed.add_field(
                        name=server_name,
                        value="\n".join(channels) if channels else "No channels found.",
                        inline=False
                    )
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
        
            except Exception as e:
                await interaction.response.send_message(f"Error: {e}", ephemeral=True)
                print(f"Error in show_settings_button: {e}")