from nextcord.ext import commands
from nextcord import TextChannel, DMChannel
from ..GUI.embed_test import EmbedTest
from ..utils.check_cogs import CheckCogs
from ..utils.read_rss_without_saving import ReadRSSWithoutSaving
from ..utils.get_rss import GetRSS

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
                await channel.send(f"RSS link: {link_rss}")
            else:
                await channel.send("No RSS link found.")
        except Exception as e:
            await channel.send(f"Error: {e}")
            print(f"Error: {e}")

    @commands.command(name="test")
    async def test(self, ctx, link_feed: str):
        try:
            channel = ctx.channel
            get_rss = GetRSS(link_feed)
            link_atom_feed = get_rss.get_rss_link()

            if link_atom_feed is None:
                await ctx.send('Link Atom feed is not found.')
                return

            read_rss = ReadRSSWithoutSaving(link_atom_feed)
            feed_emty_dto = read_rss.get_first_feed_emty()

            if feed_emty_dto is None:
                raise TypeError("link_first_entry is None")
                
            if CheckCogs.check_dm_channel(ctx):
                id_server = "DM"
            else:
                id_server = str(ctx.guild.id)
            embed = EmbedTest(id_server, feed_emty_dto)
            await channel.send(embed=embed)
        
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")

async def setup(bot):
    bot.add_cog(NormalCommands(bot))
