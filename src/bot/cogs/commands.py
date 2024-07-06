from nextcord.ext import commands
from nextcord import TextChannel
from bot.utils.ReadRSS import ReadRSS
from bot.GUI.Embed import Embed
from bot.DTO.ChannelFeedDTO import ChannelFeedDTO
from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.FeedDTO import FeedDTO
from bot.BLL.ChannelEmtyBLL import ChannelEmtyBLL
from bot.BLL.ChannelFeedBLL import ChannelFeedBLL
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL
from bot.BLL.ChannelBLL import ChannelBLL
from bot.BLL.FeedBLL import FeedBLL

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def servers(self, ctx):
        guilds = self.bot.guilds
        guild_names = [guild.name for guild in guilds]
        await ctx.send(f'The bot is in the following servers: **{", ".join(guild_names)}**')
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
        
    @commands.command()
    async def clear_channel_entry(self, ctx, channel: TextChannel):
        ChannelEmtyBLL().deleteChannelEmtyById_channel(channel.id)
        await ctx.send(f"Delete the history of the posts sent in {channel.mention} successfully.")
        
    @commands.command()
    async def read(self, ctx, link_atom_feed: str):
        ReadRSS(link_atom_feed)
        await ctx.send(f"Read **{link_atom_feed}** successfully.")

    @commands.command()
    async def test(self, ctx, channel: TextChannel, link_atom_feed: str):
        try: 
            link_emty = ReadRSS(link_atom_feed)
            embed = Embed(link_atom_feed, link_emty, "RED").get_embed()
            await channel.send(embed=embed)
            await ctx.send(f'Sent the feed to {channel.mention} successfully.')
            
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")
        
    @commands.command()
    async def set_channel_feed(self, ctx, channel: TextChannel, link_atom_feed: str):
        try: 
            ReadRSS(link_atom_feed)
            feedBLL = FeedBLL()
            channelBLL = ChannelBLL()
            channelFeedBLL = ChannelFeedBLL()
            
            feedDTO = feedBLL.getFeedByLinkAtom_feed(link_atom_feed)
            channelDTO = ChannelDTO(channel.id, channel.name)
            channelFeedDTO = ChannelFeedDTO(channelDTO, feedDTO)
            
            channelBLL.insertChannel(channelDTO)
            channelFeedBLL.insertChannelFeed(channelFeedDTO)
            await ctx.send(f"Set {channel.mention} to have {link_atom_feed} feed successfully.")
            
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
