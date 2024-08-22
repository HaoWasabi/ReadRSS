import nextcord
from nextcord import Interaction, SlashOption
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

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="ping", description="Check the bot's latency.")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms')

    @nextcord.slash_command(name="clear_channel_entry", description="Clear channel entry by channel ID.")
    async def clear_channel_entry(self, interaction: Interaction, channel: TextChannel):
        channel_emty_bll = ChannelEmtyBLL()
        channel_emty_bll.delete_channel_emty_by_id_channel(channel.id)
        await interaction.response.send_message(f"Deleted the history of posts in {channel.mention} successfully.")
        
    @nextcord.slash_command(name="clear_channel_feed", description="Clear feed settings by channel.")
    async def clear_channel_feed(self, interaction: Interaction, channel: TextChannel):
        channel_feed_bll = ChannelFeedBLL()
        channel_feed_bll.delete_channel_feed_by_id_channel(channel.id)
        await interaction.response.send_message(f"Deleted feed settings for {channel.mention} successfully.")
    
    @nextcord.slash_command(name="read", description="Read an atom feed link.")
    async def read(self, interaction: Interaction, link_atom_feed: str):
        ReadRSS(link_atom_feed)
        await interaction.response.send_message(f"Read **{link_atom_feed}** successfully.")
    
    @nextcord.slash_command(name="test", description="Test sending an embed feed to a channel.")
    async def test(self, interaction: Interaction, channel: TextChannel, link_atom_feed: str):
        try:
            read_rss = ReadRSS(link_atom_feed)
            link_first_entry = read_rss.get_link_first_entry()

            embed = FeedEmbed(link_atom_feed, link_first_entry).get_embed()
            await channel.send(embed=embed)
            await interaction.response.send_message(f'Sent the feed to {channel.mention} successfully.')
       
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")
            print(f"Error: {e}")
    
    @nextcord.slash_command(name="set_channel_feed", description="Set a channel to a specific feed.")
    async def set_channel_feed(self, interaction: Interaction, channel: TextChannel, link_atom_feed: str):
        try:
            ReadRSS(link_atom_feed)
            feed_bll = FeedBLL()
            server_bll = ServerBLL()
            channel_bll = ChannelBLL()
            channel_feed_bll = ChannelFeedBLL()
            server_channel_bll = ServerChannelBLL() 
            
            feedDTO = feed_bll.get_feed_by_link_atom_feed(link_atom_feed)
            serverDTO = ServerDTO(str(channel.guild.id), channel.guild.name)
            channelDTO = ChannelDTO(str(channel.id), channel.name)
            channelFeedDTO = ChannelFeedDTO(channelDTO, feedDTO)
            serverChanneDTO = ServerChannelDTO(serverDTO, channelDTO)
            
            server_bll.insert_server(serverDTO)
            channel_bll.insert_channel(channelDTO)
            channel_feed_bll.insert_channel_feed(channelFeedDTO)
            server_channel_bll.insert_server_channel(serverChanneDTO)
            await interaction.response.send_message(f"Set {channel.mention} to have {link_atom_feed} feed successfully.")
        
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")
            print(f"Error: {e}")
    
    @nextcord.slash_command(name="show", description="Show a list of feeds in all channels.")
    async def show(self, interaction: Interaction):
        description = ""
        channel_feed_bll = ChannelFeedBLL()
        for channelFeedDTO in channel_feed_bll.get_all_channel_feed():
            channelDTO = channelFeedDTO.get_channel()
            feedDTO = channelFeedDTO.get_feed()
            description += f"{channelDTO.get_name_channel()} : [{feedDTO.get_title_feed()}]({feedDTO.get_link_feed()})" + "\n"
        
        embed = nextcord.Embed(
            title="List of feeds in channels",
            description=description,
        )
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
