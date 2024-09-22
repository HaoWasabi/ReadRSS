import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ui import View, Button
from nextcord.ext.commands import Bot
from ..DTO.color_dto import ColorDTO
from ..BLL.feed_bll import FeedBLL

from ..GUI.embed_custom import EmbedCustom
from ..utils.check_authorization import check_authorization

class ButtonOfCtrlCommand(View):
    def __init__(self, user, bot: Bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.author = user  # Người dùng khởi tạo tương tác
        self.color = int(ColorDTO("darkkhaki").get_hex_color().replace("#", ""), 16)       

    @nextcord.ui.button(label="show settings", style=nextcord.ButtonStyle.success)
    async def show_settings_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            channel_feed_bll = FeedBLL()
            id_server = str(interaction.guild.id) if interaction.guild else "Unknown"
            server_data = {}
            num = 0
            
            for channel_feed_dto in channel_feed_bll.get_all_channel_feed():
                channel_dto = channel_feed_dto.get_channel()
                feed_dto = channel_feed_dto.get_feed()
                channel_id = int(channel_dto.get_id_channel())
                channel = self.bot.get_channel(channel_id)
                
                if channel:  # Kiểm tra xem kênh có tồn tại không
                    for server in self.bot.guilds:
                        if channel in server.channels:
                            server_name = f"**Server:** {server.name} ({server.id})"
                            channel_info = f"- **{channel_dto.get_name_channel()}** (`{channel_id}`) - [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})"
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
    
    @nextcord.ui.button(label="show servers", style=nextcord.ButtonStyle.blurple)
    async def show_servers_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            id_server = str(interaction.guild.id) if interaction.guild else "Unknown"
            guild_names = [guild.name for guild in self.bot.guilds]
            num = len(guild_names)

            embed = EmbedCustom(
                id_server=id_server,
                title="Servers",
                description=f"The bot joined {num} guilds: **{', '.join(guild_names)}**",
                color=self.color
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            print(f"Error in show_servers_button: {e}")
            
    @nextcord.ui.button(label="shutdown", style=nextcord.ButtonStyle.danger)
    async def shutdown_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return
            
        await interaction.response.send_message("The bot is shutting down...", ephemeral=True)
        await self.bot.close()
