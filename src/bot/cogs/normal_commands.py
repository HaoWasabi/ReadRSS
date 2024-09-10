from nextcord.ext import commands
from nextcord import TextChannel
from ..GUI.test_embed import TestEmbed
from ..cogs.check_dm_channel import check_dm_channel
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
    async def test(self, ctx, channel: TextChannel, link_feed: str):
        if check_dm_channel(ctx):
            return

        try:
            get_rss = GetRSS(link_feed)
            link_atom_feed = get_rss.get_rss_link()
            
            if link_atom_feed is None:
                await ctx.send('Link Atom feed is not found.')
                return
            
            read_rss = ReadRSSWithoutSaving(link_atom_feed)
            feed_emty_dto = read_rss.get_first_feed_emty()
            
            if feed_emty_dto is None:
                raise TypeError("link_first_entry is None")
            
            embed = TestEmbed(str(ctx.guild.id), feed_emty_dto).get_embed()
            await ctx.send(f"Sending test embed to {channel.mention} successfully.")
            await channel.send(embed=embed)
       
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")

async def setup(bot):
    bot.add_cog(NormalCommands(bot))
