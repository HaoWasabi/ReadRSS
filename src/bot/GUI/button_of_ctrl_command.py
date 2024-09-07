import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ui import View, Button, button
from nextcord.ext.commands import Bot
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..GUI.custom_embed import CustomEmbed
from ..GUI.check_authorization import check_authorization

class ButtonOfCtrlCommand(View):
    def __init__(self, user, bot: Bot):
        super().__init__()
        self.bot = bot
        self.author = user  # Store the user who initiated the interaction        

    @button(label="show settings", style=nextcord.ButtonStyle.success)
    async def show_settings_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return
        try:
            channel_feed_bll = ChannelFeedBLL()
            id_server = str(interaction.guild.id) if interaction.guild is not None else "Unknown"
            
            # Tạo dictionary để nhóm các channel và feed theo server
            server_data = {}
            num = 0
            
            for channel_feed_dto in channel_feed_bll.get_all_channel_feed():
                channel_dto = channel_feed_dto.get_channel()
                feed_dto = channel_feed_dto.get_feed()
                
                channel = self.bot.get_channel(int(channel_dto.get_id_channel()))
                for server in self.bot.guilds:
                    if channel in server.channels:
                        server_name = f"**Server:** {server.name} ({server.id})"
                        channel_info = f"- **{channel_dto.get_name_channel()}** (`{channel_dto.get_id_channel()}`) - [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})"
                        
                        # Thêm channel và feed vào server tương ứng
                        if server_name not in server_data:
                            server_data[server_name] = []
                        server_data[server_name].append(channel_info)
                        num += 1
            
            # Chuẩn bị nội dung cho embed
            embed = CustomEmbed(
                id_server=id_server,
                title="List of Feeds in Channels",
                description=f" You have {num} feeds in channels:",
                color=0xFFA500
            )
            
            # Thêm thông tin server và channel vào embed
            for server_name, channels in server_data.items():
                embed.add_field(
                    name=server_name,
                    value="\n".join(channels) if channels else "No channels found.",
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")
    
    @button(label="show servers", style=nextcord.ButtonStyle.blurple)
    async def show_servers_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return
        
        try:
            if interaction.guild: 
                guilds = self.bot.guilds; num = 0; guild_names = []
                
                for guild in guilds:
                    guild_names.append(guild.name); num += 1
                
                embed = CustomEmbed(
                    id_server=str(interaction.guild.id),
                    title="Servers",
                    description=f"The bot joined {num} guilds: **{', '.join(guild_names)}**",
                    color=0xFFA500
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")
            
    @button(label="shutdown", style=nextcord.ButtonStyle.danger)
    async def shutdown_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return
        await interaction.response.send_message("The bot is shutting down...", ephemeral=True)
        await self.bot.close()