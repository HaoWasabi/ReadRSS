import logging
from nextcord.ext import commands
from nextcord import TextChannel, DMChannel
from typing import Optional
from ..GUI.embed_test import EmbedTest
from ..utils.check_cogs import CheckCogs
from ..utils.read_rss_without_saving import ReadRSSWithoutSaving
from ..utils.get_rss import GetRSS

logger = logging.getLogger('nextcord')


class NormalCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="ping")
    async def ping(self, ctx):
        channel = ctx.channel
        await channel.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command(name="get_rss")
    async def get_rss(self, ctx, url: str):
        channel = ctx.channel
        try:
            link_rss = GetRSS(url).get_rss_link()
            if link_rss:
                await channel.send(f'''RSS link:```{link_rss}```''') if link_rss else await channel.send("No RSS link found.")

        except Exception as e:
            await channel.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    @commands.command(name="test")
    async def test(self, ctx, link_feed: Optional[str]):
        try:
            channel = ctx.channel

            get_rss = GetRSS(link_feed) if link_feed is not None else GetRSS("https://fit.sgu.edu.vn/site/")
            link_atom_feed = get_rss.get_rss_link()
            
            if link_atom_feed is None:
                await channel.send('Link Atom feed is not found.')
                return
            
            read_rss = ReadRSSWithoutSaving(link_atom_feed)
            feed_emty_dto = read_rss.get_first_feed_emty()

            if feed_emty_dto is None:
                raise TypeError("link_first_entry is None")
                
            id_server = str(ctx.guild.id) if ctx.guild else "DM"
            embed = EmbedTest(id_server, feed_emty_dto)
            await channel.send(embed=embed)
        
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

async def setup(bot):
    bot.add_cog(NormalCommands(bot))
