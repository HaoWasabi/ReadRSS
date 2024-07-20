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
    async def set_color(self, ctx, color: str):
        try:
            if len(color) != 6 or not all(c in "0123456789ABCDEFabcdef" for c in color):
                await ctx.send("Invalid color format! Please provide a hex color code (e.g., FF5733).")
                return
            self.embed_color = color
            await ctx.send(f"Embed color set to #{color}.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

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
            read_rss = ReadRSS(link_atom_feed)
            link_first_entry = read_rss.getLink_firstEntry()
            
            embed = Embed(link_atom_feed, link_first_entry, "RED").get_embed()
            await channel.send(embed=embed)
            await ctx.send(f'Sent the feed to {channel.mention} successfully.')
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")
        
    @commands.command()
    async def test_rss(self, ctx, linkAtom_feed: str):
        read_rss = ReadRSS(linkAtom_feed)
        link_first_entry = read_rss.getLink_firstEntry()
        embed = Embed(linkAtom_feed, link_first_entry,  "RED").get_embed()
        await ctx.send(embed=embed)
    
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
            
    @commands.command()
    async def print_stats(self, ctx):
        try:
            # Print guilds information
            guilds = self.bot.guilds
            print(f'The bot is in the following servers: {", ".join([guild.name for guild in guilds])}')
            
            # Print commands information
            command_names = [command.name for command in self.bot.commands]
            print(f'The bot has the following commands: {", ".join(command_names)}')
            
            await ctx.send("Statistics printed to terminal.")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
