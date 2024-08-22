import nextcord
from nextcord.ext import commands
from nextcord import TextChannel
from bot.dto.server_dto import ServerDTO
from bot.dto.channel_dto import ChannelDTO
from bot.dto.channel_feed_dto import ChannelFeedDTO
from bot.dto.server_channel_dto import ServerChannelDTO
from bot.bll.feed_bll import FeedBLL
from bot.bll.server_bll import ServerBLL
from bot.bll.channel_bll import ChannelBLL
from bot.bll.channel_emty_bll import ChannelEmtyBLL
from bot.bll.channel_feed_bll import ChannelFeedBLL
from bot.bll.server_channel_bll import ServerChannelBLL
from bot.gui.feed_embeb import FeedEmbed
from bot.utils.read_rss import ReadRSS

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.__bot = bot
        self.__feed_bll = FeedBLL()
        self.__server_bll = ServerBLL()
        self.__channel_bll = ChannelBLL()
        self.__channel_feed_bll = ChannelFeedBLL()
        self.__channel_emty_bll = ChannelEmtyBLL()
        self.__server_channel_bll = ServerChannelBLL()
          
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.__bot.latency * 1000)}ms')
        
    @commands.command()
    async def clear_channel_entry(self, ctx, channel: TextChannel):
        self.__channel_emty_bll.delete_channel_emty_by_id_channel(channel.id)
        await ctx.send(f"Delete the history of the posts sent in {channel.mention} successfully.")
        
    @commands.command()
    async def clear_channel_feed(self, ctx, channel: TextChannel):
        self.__channel_feed_bll.delete_channel_feed_by_id_channel(channel.id)
        await ctx.send(f"Delete settings of the feed sent in {channel.mention} successfully.")
    
    @commands.command()
    async def read(self, ctx, link_atom_feed: str):
        ReadRSS(link_atom_feed)
        await ctx.send(f"Read **{link_atom_feed}** successfully.")

    @commands.command()
    async def test(self, ctx, channel: TextChannel, link_atom_feed: str):
        try:
            read_rss = ReadRSS(link_atom_feed)
            link_first_entry = read_rss.get_link_first_entry()
            
            embed = FeedEmbed(link_atom_feed, link_first_entry).get_embed()
            await channel.send(embed=embed)
            await ctx.send(f'Sent the feed to {channel.mention} successfully.')
       
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")
    
    @commands.command()
    async def set_channel_feed(self, ctx, channel: TextChannel, link_atom_feed: str):
        try: 
            ReadRSS(link_atom_feed)
            
            feedDTO = self.__feed_bll.get_feed_by_link_atom_feed(link_atom_feed)
            serverDTO = ServerDTO(str(channel.guild.id), channel.guild.name)
            channelDTO = ChannelDTO(str(channel.id), channel.name)
            channelFeedDTO = ChannelFeedDTO(channelDTO, feedDTO)
            serverChanneDTO = ServerChannelDTO(serverDTO, channelDTO)
            
            self.__server_bll.insert_server(serverDTO)
            self.__channel_bll.insert_channel(channelDTO)
            self.__channel_feed_bll.insert_channel_feed(channelFeedDTO)
            self.__server_channel_bll.insert_server_channel(serverChanneDTO)
            await ctx.send(f"Set {channel.mention} to have {link_atom_feed} feed successfully.")
        
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")

    @commands.command()
    async def show(self, ctx):
        description = ""
        for channelFeedDTO in self.__channel_feed_bll.get_all_channel_feed():
            channelDTO = channelFeedDTO.get_channel()
            feedDTO = channelFeedDTO.get_feed()
            description += f"{channelDTO.get_name_channel()} : [{feedDTO.get_title_feed()}]({feedDTO.get_link_feed()})" + "\n"
        embed = nextcord.Embed(
            title= "List of feeds in channels",
            description= description,
            )
        await ctx.send(embed=embed)
        
async def setup(bot):
    bot.add_cog(BotCommands(bot))
