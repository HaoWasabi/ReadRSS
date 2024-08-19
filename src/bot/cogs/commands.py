import nextcord
from nextcord.ext import commands
from nextcord import TextChannel
from bot.dto.channel_feed_dto import ChannelFeedDTO
from bot.dto.feed_emty_dto import FeedEmtyDTO
from bot.dto.channel_dto import ChannelDTO
from bot.dto.feed_dto import FeedDTO
from bot.bll.channel_emty_bll import ChannelEmtyBLL
from bot.bll.channel_feed_bll import ChannelFeedBLL
from bot.bll.feed_emty_bll import FeedEmtyBLL
from bot.bll.channel_bll import ChannelBLL
from bot.bll.feed_bll import FeedBLL
from bot.gui.feed_embeb import FeedEmbed
from bot.utils.read_rss import ReadRSS

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
          
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
        
    @commands.command()
    async def clear_channel_entry(self, ctx, channel: TextChannel):
        ChannelEmtyBLL().delete_channel_emty_by_id_channel(channel.id)
        await ctx.send(f"Delete the history of the posts sent in {channel.mention} successfully.")
        
    @commands.command()
    async def clear_channel_feed(self, ctx, channel: TextChannel):
        ChannelFeedBLL().delete_channel_feed_by_id_channel(channel.id)
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
            feedBLL = FeedBLL()
            channelBLL = ChannelBLL()
            channelFeedBLL = ChannelFeedBLL()
            
            feedDTO = feedBLL.get_feed_by_link_atom_feed(link_atom_feed)
            channelDTO = ChannelDTO(str(channel.id), channel.name)
            channelFeedDTO = ChannelFeedDTO(channelDTO, feedDTO)
            
            channelBLL.insert_channel(channelDTO)
            channelFeedBLL.insert_channel_feed(channelFeedDTO)
            await ctx.send(f"Set {channel.mention} to have {link_atom_feed} feed successfully.")
        
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")

    @commands.command()
    async def show(self, ctx):
        channelFeedBLL = ChannelFeedBLL()
        description = ""
        for channelFeedDTO in channelFeedBLL.get_all_channel_feed():
            channelDTO = channelFeedDTO.get_channel()
            feedDTO = channelFeedDTO.get_feed()
            description += f"{channelDTO.get_name_channel()} : [{feedDTO.get_title_feed()}]({feedDTO.get_link_feed()})" + "\n"
        embed = nextcord.Embed(
            title= "List of feeds in channels",
            description= description,
            )
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(BotCommands(bot))
