import nextcord
from nextcord.ext import commands
from nextcord import TextChannel
from bot.dto.server_dto import ServerDTO
from bot.dto.channel_dto import ChannelDTO
from bot.dto.color_dto import ColorDTO
from bot.dto.channel_feed_dto import ChannelFeedDTO
from bot.dto.server_channel_dto import ServerChannelDTO
from bot.dto.server_color_dto import ServerColorDTO
from bot.bll.feed_bll import FeedBLL
from bot.bll.server_bll import ServerBLL
from bot.bll.channel_bll import ChannelBLL
from bot.bll.channel_emty_bll import ChannelEmtyBLL
from bot.bll.channel_feed_bll import ChannelFeedBLL
from bot.bll.server_channel_bll import ServerChannelBLL
from bot.bll.server_color_bll import ServerColorBLL
from bot.gui.feed_embed import FeedEmbed
from bot.gui.test_embed import TestEmbed
from bot.utils.read_rss import ReadRSS
from bot.utils.read_rss_without_saving import ReadRSSWithoutSaving

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
          
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
        
    @commands.command()
    async def clear_channel_entry(self, ctx, channel: TextChannel):
        channel_emty_bll = ChannelEmtyBLL()
        channel_emty_bll.delete_channel_emty_by_id_channel(channel.id)
        await ctx.send(f"Deleted the history of posts in {channel.mention} successfully.")
        
    @commands.command()
    async def clear_channel_feed(self, ctx, channel: TextChannel):
        channel_feed_bll = ChannelFeedBLL()
        channel_feed_bll.delete_channel_feed_by_id_channel(channel.id)
        await ctx.send(f"Deleted feed settings for {channel.mention} successfully.")

    @commands.command()
    async def test(self, ctx, channel: TextChannel, link_atom_feed: str):
        try:
            read_rss = ReadRSSWithoutSaving(link_atom_feed)
            feed_emty_dto = read_rss.get_first_feed_emty()
            
            embed = TestEmbed(feed_emty_dto).get_embed()
            await channel.send(embed=embed)
            await ctx.send(f'Sent the feed to {channel.mention} successfully.')
       
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")
    
    @commands.command()
    async def set_channel_feed(self, ctx, channel: TextChannel, link_atom_feed: str):
        try: 
            ReadRSS(link_atom_feed)
            feed_bll = FeedBLL()
            server_bll = ServerBLL()
            channel_bll = ChannelBLL()
            channel_feed_bll = ChannelFeedBLL()
            server_channel_bll = ServerChannelBLL()
            
            feed_dto = feed_bll.get_feed_by_link_atom_feed(link_atom_feed)
            server_dto = ServerDTO(str(channel.guild.id), channel.guild.name)
            channel_dto = ChannelDTO(str(channel.id), channel.name)
            channel_feed_dto = ChannelFeedDTO(channel_dto, feed_dto)
            server_channel_dto = ServerChannelDTO(server_dto, channel_dto)
            
            server_bll.insert_server(server_dto)
            channel_bll.insert_channel(channel_dto)
            channel_feed_bll.insert_channel_feed(channel_feed_dto)
            server_channel_bll.insert_server_channel(server_channel_dto)
            await ctx.send(f"Set {channel.mention} to have {link_atom_feed} feed successfully.")
        
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")

    @commands.command()
    async def set_color(self, ctx, color: str):
        try:
            color_dto = ColorDTO(color)
            server_dto = ServerDTO(str(ctx.guild.id), ctx.guild.name)
            server_color_dto = ServerColorDTO(server_dto, color_dto)
            server_color_bll = ServerColorBLL()
            
            if server_color_bll.insert_server_color(server_color_dto) == False:
                server_color_bll.update_server_color_by_id_server(server_dto.get_id_server(), server_color_dto)
            
            await ctx.send(f"Set color **{color_dto.get_name_color()}** successfully.")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")
                       
    @commands.command()
    async def show(self, ctx):
        description = ""
        channel_feed_bll = ChannelFeedBLL()
        for channel_feed_dto in channel_feed_bll.get_all_channel_feed():
            channel_dto = channel_feed_dto.get_channel()
            feed_dto = channel_feed_dto.get_feed()
            
            channel = self.bot.get_channel(int(channel_dto.get_id_channel()))
            if channel in ctx.guild.channels:
                description += f"{channel_dto.get_name_channel()} : [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})" + "\n"
        
        embed = nextcord.Embed(
            title= "List of feeds in channels",
            description= description,
        )
        await ctx.send(embed=embed)
        
async def setup(bot):
    bot.add_cog(BotCommands(bot))
