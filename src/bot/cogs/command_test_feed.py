import logging
from typing import Optional
from nextcord.ext import commands
import nextcord
from nextcord import Interaction, SlashOption
from requests import get

from ..GUI.embed_feed import EmbedFeed
from ..utils.commands_cog import CommandsCog
from ..utils.handle_rss import get_rss_link, read_rss_link

logger = logging.getLogger("CommandTestFeed")

class CommandTestFeed(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)

    async def _test(self, ctx, link_rss: Optional[str] = None):
        try:
            feed_data = read_rss_link(rss_link=link_rss)
            if not feed_data or not all(feed_data):
                raise TypeError("Feed data is incomplete or None")
            
            feed_dto, emty_dto = feed_data
            embed = EmbedFeed(
                id_server=str(ctx.guild.id) if ctx.guild else "DM", 
                feed_dto=feed_dto, 
                emty_dto=emty_dto
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    @commands.command(name="test")
    async def command_test(self, ctx, url: Optional[str] = None):
        if not link_rss:
            link_rss = get_rss_link(url="https://fit.sgu.edu.vn/site/")
            if not link_rss:
                await ctx.send('Link Atom feed is not found.')
                return
        await self._test(ctx, link_rss)

    @nextcord.slash_command(name="test", description="Test the bot")
    async def slash_command_test(self, interaction: Interaction, 
                                  url: Optional[str] = SlashOption(description="The feed link"), 
                                  link_rss: Optional[str] = SlashOption(description="The Atom feed link")):
        await interaction.response.defer()
        if link_rss and url:
            await interaction.followup.send('Choose one of link_rss or url.')
            return
        elif not link_rss and not url:
            link_rss = get_rss_link(url="https://fit.sgu.edu.vn/site/")
            if not link_rss:
                await interaction.followup.send('Link Atom feed is not found.')
                return
        elif not link_rss and url:
            link_rss = get_rss_link(url) 
        await self._test(interaction.followup, link_rss)

async def setup(bot):
   bot.add_cog(CommandTestFeed(bot))
