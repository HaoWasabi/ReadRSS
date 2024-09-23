import logging
from nextcord.ext import commands
from nextcord import DMChannel, Color

from ..GUI import EmbedCustom, SelectClear, ButtonOfCtrlCommand
from ..DTO import ColorDTO
from ..utils.commands_cog import CommandsCog

logger = logging.getLogger("AdminBotCommands")


class AdminBotCommands(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.color = int(
            ColorDTO("darkkhaki").hex_color.replace("#", ""), 16)

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        try:
            channel = ctx.channel
            embed = EmbedCustom(
                id_server=str(ctx.guild.id) if not isinstance(
                    ctx.channel, DMChannel) else "DM",
                title="Warning",
                description="The bot is shutting down...",
                color=self.color
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
            channel = ctx.channel

            hex_color = int(
                ColorDTO("darkkhaki").hex_color.replace("#", ""), 16)
            embed = EmbedCustom(
                id_server=str(ctx.guild.id) if not isinstance(
                    ctx.channel, DMChannel) else "DM",
                title="Control Panel",
                description="Choose an option to control the bot.",
                color=self.color
            )
            await channel.send(embed=embed, view=ButtonOfCtrlCommand(ctx.author, self.bot))
            await channel.send("Choose an option to clear in the database.", view=SelectClear(user=ctx.author))

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

        raise NotImplementedError(
            "This is a placeholder for the AdminBotCommands cog. You should implement this cog before using it.")


async def setup(bot):
    bot.add_cog(AdminBotCommands(bot))
