import logging
from nextcord.ext import commands
from nextcord import DMChannel
from ..GUI.custom_embed import CustomEmbed
from ..GUI.select_clear import SelectClear
from ..GUI.button_of_ctrl_command import ButtonOfCtrlCommand
from ..cogs.check_dm_channel import check_dm_channel

logger = logging.getLogger('AdminBotCommands')

class AdminBotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        try:
            channel = ctx.channel if check_dm_channel(ctx) else ctx.channel

            embed = CustomEmbed(
                id_server=str(ctx.guild.id) if not isinstance(ctx.channel, DMChannel) else "DM",
                title="Warning",
                description="The bot is shutting down...",
                color=0xFFA500
            )
            await channel.send(embed=embed)
            await self.bot.close()
        except Exception as e:
            logger.error(f"Error: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command(name="ctrl")
    @commands.is_owner()
    async def ctrl_command(self, ctx):
        try:
            channel = ctx.channel if check_dm_channel(ctx) else ctx.channel

            embed = CustomEmbed(
                id_server=str(ctx.guild.id) if not isinstance(ctx.channel, DMChannel) else "DM",
                title="Control Panel",
                description="Choose an option to control the bot.",
                color=0xFFA500
            )
            await channel.send(embed=embed, view=ButtonOfCtrlCommand(ctx.author, self.bot)) 
            await channel.send("Choose an option to clear in the database.", view=SelectClear(user=ctx.author))
            
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")
        
        raise NotImplementedError("This is a placeholder for the AdminBotCommands cog. You should implement this cog before using it.")
async def setup(bot):
    bot.add_cog(AdminBotCommands(bot))
