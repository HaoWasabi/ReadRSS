from nextcord import Interaction
from nextcord import TextChannel
from nextcord.ext import commands
from bot.utils.Database import Database
from bot.BLL.ChannelEmtyBLL import ChannelEmtyBLL
from bot.utils.ReadRSS import ReadRSS
from bot.GUI.Embed import Embed
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.FeedDTO import FeedDTO
from bot.BLL.ChannelBLL import ChannelBLL
from bot.BLL.FeedBLL import FeedBLL
from bot.BLL.ChannelFeedBLL import ChannelFeedBLL

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="servers", description="Shows the servers the bot is in")
    async def _servers(self, interaction: Interaction):
        guilds = self.bot.guilds
        guild_names = [guild.name for guild in guilds]
        await interaction.response.send_message(f'The bot is in the following servers: {", ".join(guild_names)}')

    @commands.slash_command(name="ping", description="Replies with Pong!")
    async def _ping(self, interaction: Interaction):
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.slash_command(name="super_clear", description="Clears all data in the database")
    async def _super_clear(self, interaction: Interaction):
        Database().clear()
        await interaction.response.send_message("Cleared all data in the database successfully.")
        
    @commands.slash_command(name="clear_channel_entry", description="Delete the history of the posts sent in the channel")
    async def _clear_channel_entry(self, interaction: Interaction, channel: TextChannel):
        ChannelEmtyBLL().deleteChannelEmtyById_channel(channel.id)
        await interaction.response.send_message(f"Delete the history of the posts sent in '{channel}' successfully.")

    @commands.slash_command(name="read", description="Reads RSS from the given URL")
    async def _read(self, interaction: Interaction, url: str):
        ReadRSS(url)
        await interaction.response.send_message("Read RSS successfully.")

    @commands.slash_command(name="test_channel", description="Send the RSS feed to the channel")
    async def _test_channel(self, interaction: Interaction, channel: TextChannel):
        embed = Embed("https://www.facebook.com/TuoitrekhoaCongngheThongtinSGU", 
                    "https://www.facebook.com/814717200441834/posts/957235702856649", 
                    "RED").get_embed()
        await channel.send(embed=embed)
        await interaction.response.send_message(f'Sent the feed to {channel.mention}')
        
    @commands.slash_command(name="test", description="Send the RSS feed to the channel")
    async def _test(self, interaction: Interaction):
        embed = Embed("https://www.facebook.com/TuoitrekhoaCongngheThongtinSGU", 
                    "https://www.facebook.com/814717200441834/posts/957235702856649", 
                    "RED").get_embed()
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name="set_channel_feed", description="Set the feed of the channel")
    async def _set_channel_feed(self, interaction: Interaction,  channel: TextChannel, link_atom_feed: str):
        try: 
            ReadRSS(link_atom_feed)
            feedBLL = FeedBLL()
            channelBLL = ChannelBLL()
            channelFeedBLL = ChannelFeedBLL()
            
            feedDTO = feedBLL.getFeedByLinkAtom_feed(link_atom_feed)
            channelDTO = ChannelDTO(channel.id, channel.name)
            
            channelBLL.insertChannel(channelDTO)
            channelFeedBLL.insertChannelFeed(channelDTO, feedDTO)
            await interaction.response.send_message(f"Set {channel.name}'s feed successfully.")
            
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")
            print(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
