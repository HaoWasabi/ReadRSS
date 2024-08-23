import nextcord
from nextcord.ext import commands
from nextcord import SlashOption, Interaction, TextChannel
from ..DTO.server_dto import ServerDTO
from ..DTO.channel_dto import ChannelDTO
from ..DTO.color_dto import ColorDTO
from ..DTO.channel_feed_dto import ChannelFeedDTO
from ..DTO.server_channel_dto import ServerChannelDTO
from ..DTO.server_color_dto import ServerColorDTO
from ..BLL.feed_bll import FeedBLL
from ..BLL.server_bll import ServerBLL
from ..BLL.channel_bll import ChannelBLL
from ..BLL.channel_emty_bll import ChannelEmtyBLL
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..BLL.server_channel_bll import ServerChannelBLL
from ..BLL.server_color_bll import ServerColorBLL
from ..GUI.feed_embed import FeedEmbed
from ..GUI.test_embed import TestEmbed
from ..utils.read_rss import ReadRSS
from ..utils.read_rss_without_saving import ReadRSSWithoutSaving

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping", description="Check bot latency")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms')

    @nextcord.slash_command(name="clear_channel_entry", description="Clear channel post history")
    async def clear_channel_entry(self, interaction: Interaction, channel: TextChannel = SlashOption(description="The target channel")):
        channel_emty_bll = ChannelEmtyBLL()
        channel_emty_bll.delete_channel_emty_by_id_channel(str(channel.id))
        await interaction.response.send_message(f"Deleted the history of posts in {channel.mention} successfully.")

    @nextcord.slash_command(name="clear_channel_feed", description="Clear channel feed settings")
    async def clear_channel_feed(self, interaction: Interaction, channel: TextChannel = SlashOption(description="The target channel")):
        channel_feed_bll = ChannelFeedBLL()
        channel_feed_bll.delete_channel_feed_by_id_channel(str(channel.id))
        await interaction.response.send_message(f"Deleted feed settings for {channel.mention} successfully.")
    
    @nextcord.slash_command(name="test_feed", description="Test sending an RSS feed")
    async def test(self, interaction: Interaction, channel: TextChannel = SlashOption(description="The target channel"), link_atom_feed: str = SlashOption(description="The Atom/RSS feed link")):
        try:
            read_rss = ReadRSSWithoutSaving(link_atom_feed)
            feed_emty_dto = read_rss.get_first_feed_emty()
            
            embed = TestEmbed(feed_emty_dto).get_embed()
            await channel.send(embed=embed)
            await interaction.response.send_message(f'Sent the feed to {channel.mention} successfully.')
       
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")
            print(f"Error: {e}")
    
    @nextcord.slash_command(name="set_channel_feed", description="Set a channel feed")
    async def set_channel_feed(self, interaction: Interaction, channel: TextChannel = SlashOption(description="The target channel"), link_atom_feed: str = SlashOption(description="The Atom/RSS feed link")):
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
            await interaction.response.send_message(f"Set {channel.mention} to have {link_atom_feed} feed successfully.")
        
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")
            print(f"Error: {e}")
            
    @nextcord.slash_command(name="set_color", description="Set the color of all embeds that you want it would send")
    async def set_color(self, interaction: Interaction, color: str):
        try:
            color_dto = ColorDTO(color)
            server_dto = ServerDTO(str(interaction.guild.id), interaction.guild.name)
            server_color_dto = ServerColorDTO(server_dto, color_dto)
            server_color_bll = ServerColorBLL()

            if server_color_bll.insert_server_color(server_color_dto) == False:
                server_color_bll.update_server_color_by_id_server(server_dto.get_id_server(), server_color_dto)
                
            await interaction.response.send_message(f"Set color **{color_dto.get_name_color()}** successfully.")
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")
            print(f"Error: {e}")

    @nextcord.slash_command(name="show_feeds", description="Show list of feeds in channels")
    async def show(self, interaction: Interaction):
        description = ""
        channel_feed_bll = ChannelFeedBLL()
        for channel_feed_dto in channel_feed_bll.get_all_channel_feed():
            channel_dto = channel_feed_dto.get_channel()
            feed_dto = channel_feed_dto.get_feed()
            
            channel = self.bot.get_channel(int(channel_dto.get_id_channel()))
            if (interaction.guild is None): return
            if channel in interaction.guild.channels:
                description += f"{channel_dto.get_name_channel()} : [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})" + "\n"
        
        embed = nextcord.Embed(
            title= "List of feeds in channels",
            description= description,
        )
        await interaction.response.send_message(embed=embed)
        
        
async def setup(bot):
    bot.add_cog(SlashCommands(bot))
