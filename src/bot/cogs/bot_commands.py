import nextcord
from nextcord.ext import commands
from nextcord import TextChannel
from ..DTO.server_dto import ServerDTO
from ..DTO.channel_dto import ChannelDTO
from ..DTO.color_dto import ColorDTO
from ..DTO.channel_feed_dto import ChannelFeedDTO
from ..DTO.server_channel_dto import ServerChannelDTO
from ..DTO.server_color_dto import ServerColorDTO
from ..BLL.server_color_bll import ServerColorBLL
from ..BLL.feed_bll import FeedBLL
from ..BLL.server_bll import ServerBLL
from ..BLL.channel_bll import ChannelBLL
from ..BLL.channel_emty_bll import ChannelEmtyBLL
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..BLL.server_channel_bll import ServerChannelBLL
from ..GUI.test_embed import TestEmbed
from ..GUI.custom_embed import CustomEmbed
from ..utils.read_rss import ReadRSS
from ..utils.read_rss_without_saving import ReadRSSWithoutSaving

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
          
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
        
    @commands.command()
    async def clear_history(self, ctx, channel: TextChannel):
        channel_emty_bll = ChannelEmtyBLL()
        channel_emty_bll.delete_channel_emty_by_id_channel(str(channel.id))
        await ctx.send(f"Deleted the history of posts in {channel.mention} successfully.")
        
    @commands.command()
    async def delete_feed(self, ctx, channel: TextChannel):
        channel_feed_bll = ChannelFeedBLL()
        channel_feed_bll.delete_channel_feed_by_id_channel(str(channel.id))
        await ctx.send(f"Deleted feed settings for {channel.mention} successfully.")

    @commands.command()
    async def test_feed(self, ctx, channel: TextChannel, link_atom_feed: str):
        try:
            read_rss = ReadRSSWithoutSaving(link_atom_feed)
            feed_emty_dto = read_rss.get_first_feed_emty()
            
            if feed_emty_dto is None:
                raise TypeError("link_first_entry is None")
            embed = TestEmbed(str(ctx.guild.id), feed_emty_dto).get_embed()
            await channel.send(embed=embed)
            await ctx.send(f'Sent the feed to {channel.mention} successfully.')
       
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")
    
    @commands.command()
    async def set_feed(self, ctx, channel: TextChannel, link_atom_feed: str):
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
            channel_feed_dto = ChannelFeedDTO(channel_dto, feed_dto) # type: ignore
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

            hex_color = server_color_dto.get_color().get_hex_color()
            embed = nextcord.Embed(title="Set color", description=f"Set color **{color_dto.get_name_color()}** successfully.", color=int(hex_color, 16))
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")
                       
    @commands.command()
    async def show(self, ctx):
        try:
            value_channel = ""
            value_feed = ""
            num = 0
            channel_feed_bll = ChannelFeedBLL()
            id_server = str(ctx.guild.id)  # Move the id_server definition outside the loop to ensure it's always defined
            
            for channel_feed_dto in channel_feed_bll.get_all_channel_feed():
                channel_dto = channel_feed_dto.get_channel()
                feed_dto = channel_feed_dto.get_feed()
                
                channel = self.bot.get_channel(int(channel_dto.get_id_channel()))
                if channel in ctx.guild.channels:
                    value_channel += f"{channel_dto.get_name_channel()}\n"
                    value_feed += f"[{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})\n"
                    num += 1
                    
            embed = CustomEmbed(
                id_server=id_server,
                title="List of feeds in channels",
                description=f"You have {num} feeds in channels",
            )
            embed.add_field(name="channel", value=value_channel)
            embed.add_field(name="feed", value=value_feed)
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")

                
async def setup(bot):
    bot.add_cog(BotCommands(bot))
