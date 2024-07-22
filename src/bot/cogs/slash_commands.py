import nextcord
from nextcord.ext import commands
from nextcord import Interaction, TextChannel
from bot.utils.ReadRSS import ReadRSS
from bot.GUI.FeedEmbed import FeedEmbed
from bot.DTO.ChannelFeedDTO import ChannelFeedDTO
from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.FeedDTO import FeedDTO
from bot.BLL.ChannelEmtyBLL import ChannelEmtyBLL
from bot.BLL.ChannelFeedBLL import ChannelFeedBLL
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL
from bot.BLL.ChannelBLL import ChannelBLL
from bot.BLL.FeedBLL import FeedBLL

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping", description="Replies with Pong!")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms')

    @nextcord.slash_command(name="clear_channel_entry", description="Delete the history of the posts sent in the channel")
    async def clear_channel_entry(self, interaction: Interaction, channel: TextChannel):
        ChannelEmtyBLL().deleteChannelEmtyById_channel(channel.id)
        await interaction.response.send_message(f"Delete the history of the posts sent in {channel.mention} successfully.")

    @nextcord.slash_command(name="clear_channel_feed", description="Delete settings of the feed sent in the channel")
    async def clear_channel_feed(self, interaction: Interaction, channel: TextChannel):
        ChannelFeedBLL().deleteChannelFeedById_channel(channel.id)
        await interaction.response.send_message(f"Delete settings of the feed sent in {channel.mention} successfully.")
        
    @nextcord.slash_command(name="read", description="Reads RSS from the given URL")
    async def read(self, interaction: Interaction, link_atom_feed: str):
        ReadRSS(link_atom_feed)
        await interaction.response.send_message(f"Read **{link_atom_feed}** successfully.")

    @nextcord.slash_command(name="test", description="Send the RSS feed to the channel")
    async def test(self, interaction: Interaction, channel: TextChannel, link_atom_feed: str):
        try:
            read_rss = ReadRSS(link_atom_feed)
            link_first_entry = read_rss.getLink_firstEntry()
            
            embed = FeedEmbed(link_atom_feed, link_first_entry).get_embed()
            await channel.send(embed=embed)
            await interaction.response.send_message(f'Sent the feed to {channel.mention} successfully.')
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")
            print(f"Error: {e}")

    @nextcord.slash_command(name="set_channel_feed", description="Set the feed of the channel")
    async def set_channel_feed(self, interaction: Interaction, channel: TextChannel, link_atom_feed: str):
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
            await interaction.response.send_message(f"Set {channel.mention} to have {link_atom_feed} feed successfully.")
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")
            print(f"Error: {e}")

    @nextcord.slash_command(name="show", description="Show the list of feeds in channels")
    async def show(self, interaction: Interaction):
        channelFeedBLL = ChannelFeedBLL()
        description = ""
        for channelFeedDTO in channelFeedBLL.getAllChannelFeed():
            channelDTO = channelFeedDTO.getChannel()
            feedDTO = channelFeedDTO.getFeed()
            description += f"- {channelDTO.getName_channel()} ({channelDTO.getId_channel()}): {feedDTO.getTitle_feed()} ({feedDTO.getLink_feed()})" + "\n"
        embed = nextcord.Embed(
            title="List of feeds in channels",
            description=description,
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
