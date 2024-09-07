import nextcord
from nextcord import Interaction
from nextcord.ui import View
from nextcord.ext import commands
from typing import Optional
from ..utils.Database import dataBase
from nextcord.ext.commands import Bot
from ..BLL.channel_bll import ChannelBLL
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..BLL.channel_emty_bll import ChannelEmtyBLL
from ..GUI.custom_embed import CustomEmbed
from ..GUI.select_clear import SelectClear
from ..GUI.button_of_ctrl_command import ButtonOfCtrlCommand
from ..GUI.check_authorization import check_authorization

class AdminCommands(commands.Cog):
    
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        try: 
            embed = CustomEmbed(
                id_server=str(ctx.guild.id),
                title="Warning",
                description="The bot is shutting down...",
                color=0xFFA500
            )
            await ctx.send(embed=embed)
            await self.bot.close()
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")
        
    @commands.command(name="ctrl")
    @commands.is_owner()
    async def ctrl_command(self, ctx):
        try:
            embed = CustomEmbed(
                id_server=str(ctx.guild.id),
                title="Control Panel",
                description="Choose an option to control the bot.",
                color=0xFFA500
            )
            await ctx.send(embed=embed, view=ButtonOfCtrlCommand(ctx.author, self.bot)) 
            await ctx.send("Choice an option to clear in database.", view = SelectClear(user=ctx.author))
            
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")
            
async def setup(bot):
    bot.add_cog(AdminCommands(bot))
