from code import interact
from re import S
from urllib import response
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ui import View, Button
from nextcord.ext.commands import Bot
from ..DTO.color_dto import ColorDTO
from ..BLL.feed_bll import FeedBLL
from ..BLL.channel_bll import ChannelBLL
from ..GUI.embed_custom import EmbedCustom
# from ..GUI.select_clear import SelectClear
from ..GUI.select_feed import SelectFeed
from ..GUI.select_premium import SelectPremium
from ..GUI.select_insert_user_premium import SelectInsertUserPremium
from ..utils.check_authorization import check_authorization

class ButtonOfCtrlCommand(View):
    def __init__(self, user, bot: Bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.author = user  # Người dùng khởi tạo tương tác
        self.color = int(ColorDTO("darkkhaki").get_hex_color().replace("#", ""), 16)       

    @nextcord.ui.button(label="feed", style=nextcord.ButtonStyle.gray)
    async def feed_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            await interaction.response.send_message("Choose an option to change feed.", view=SelectFeed(user=self.author, bot=self.bot), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            print(f"Error in show_settings_button: {e}")

    @nextcord.ui.button(label="premium", style=nextcord.ButtonStyle.gray)
    async def premium_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            await interaction.response.send_message("Choose an option to change premium.", view=SelectPremium(user=self.author, bot=self.bot), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            print(f"Error in show_settings_button: {e}")

    @nextcord.ui.button(label="userpremium", style=nextcord.ButtonStyle.gray)
    async def userpremium_button(self, button: Button, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return

        try:
            await interaction.response.send_message("Choose a premium to insert userpremium.", view=SelectInsertUserPremium(user=self.author, bot=self.bot), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            print(f"Error in show_settings_button: {e}")
    
    @nextcord.ui.button(label="servers", style=nextcord.ButtonStyle.success)
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
