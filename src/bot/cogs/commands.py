from bot.BLL.ChannelEmtyBLL import ChannelEmtyBLL
from bot.utils.ReadRSS import ReadRSS
from bot.GUI.Embed import Embed
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.FeedDTO import FeedDTO
from bot.BLL.ChannelBLL import ChannelBLL
from bot.BLL.FeedBLL import FeedBLL
from bot.BLL.ChannelFeedBLL import ChannelFeedBLL
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from bot.GUI.Embed import Embed
from bot.utils.ReadRSS import ReadRSS
from bot.utils.Database import Database

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def servers(self, ctx):
        guilds = self.bot.guilds
        guild_names = [guild.name for guild in guilds]
        await ctx.send(f'The bot is in the following servers: {", ".join(guild_names)}')
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def super_clear(self, ctx):
        Database().clear()
        await ctx.send("Cleared all data in the database successfully.")
    
    @commands.command()
    async def clear_channel_entry(self, ctx, channel: nextcord.TextChannel):
        ChannelEmtyBLL().deleteChannelEmtyById_channel(channel.id)
        await ctx.send(f"Delete the history of the posts sent in '{channel}' successfully.")
    
    @commands.command()
    async def read(self, ctx, url):
        ReadRSS(url)
        await ctx.send("Read RSS successfully.")

    @commands.command()
    async def test_channel(self, ctx, channel: nextcord.TextChannel):
        embed = Embed("https://www.facebook.com/TuoitrekhoaCongngheThongtinSGU", 
                      "https://www.facebook.com/814717200441834/posts/957235702856649", 
                      "RED").get_embed()
        await channel.send(embed=embed)
        await ctx.send(f'Sent the feed to {channel.mention}')
    
    @commands.command()
    async def test(self, ctx):
        embed = Embed("https://www.facebook.com/TuoitrekhoaCongngheThongtinSGU", 
                      "https://www.facebook.com/814717200441834/posts/957235702856649", 
                      "RED").get_embed()
        await ctx.send(embed=embed)

    @commands.command()
    async def set_channel_feed(self, ctx, channel: nextcord.TextChannel, link_atom_feed: str):
        try: 
            ReadRSS(link_atom_feed)
            feedBLL = FeedBLL()
            channelBLL = ChannelBLL()
            channelFeedBLL = ChannelFeedBLL()
            
            feedDTO = feedBLL.getFeedByLinkAtom_feed(link_atom_feed)
            channelDTO = ChannelDTO(channel.id, channel.name)
            
            channelBLL.insertChannel(channelDTO)
            channelFeedBLL.insertChannelFeed(channelDTO, feedDTO)
            await ctx.send(f"Set {channel.name}'s feed successfully.")
            
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")

# Hàm setup để thêm cog vào bot
async def setup(bot):
    await bot.add_cog(BotCommands(bot))
