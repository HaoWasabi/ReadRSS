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

from ..GUI.test_embed import TestEmbed
from ..GUI.custom_embed import CustomEmbed

from ..utils.read_rss_without_saving import ReadRSSWithoutSaving
from ..utils.read_rss import ReadRSS

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping", description="Check bot latency")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms')

    @nextcord.slash_command(name="clear_history", description="Clear channel post history")
    async def clear_history(self, interaction: Interaction, channel: TextChannel = SlashOption(description="The target channel")):
        channel_emty_bll = ChannelEmtyBLL()
        channel_emty_bll.delete_channel_emty_by_id_channel(str(channel.id))
        await interaction.response.send_message(f"Deleted the history of posts in {channel.mention} successfully.")

    @nextcord.slash_command(name="delete_feed", description="Delete feed notification channel settings")
    async def delete_feed(self, interaction: Interaction, channel: TextChannel = SlashOption(description="The target channel")):
        channel_feed_bll = ChannelFeedBLL()
        channel_feed_bll.delete_channel_feed_by_id_channel(str(channel.id))
        await interaction.response.send_message(f"Deleted feed settings for {channel.mention} successfully.")

    @nextcord.slash_command(name="test_feed", description="Test sending an RSS feed")
    async def test_feed(self, interaction: Interaction, channel: TextChannel = SlashOption(description="The target channel"), link_atom_feed: str = SlashOption(description="The Atom/RSS feed link")):
        try:
            read_rss = ReadRSSWithoutSaving(link_atom_feed)
            feed_emty_dto = read_rss.get_first_feed_emty()

            embed = TestEmbed(str(interaction.guild.id), feed_emty_dto).get_embed()  # type: ignore
            await channel.send(embed=embed)
            await interaction.response.send_message(f'Sent the feed to {channel.mention} successfully.')
       
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")
            print(f"Error: {e}")

    @nextcord.slash_command(name="set_feed", description="Set feed notification channel")
    async def set_feed(self, interaction: Interaction, channel: TextChannel = SlashOption(description="The target channel"), link_atom_feed: str = SlashOption(description="The Atom/RSS feed link")):
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
            channel_feed_dto = ChannelFeedDTO(channel_dto, feed_dto)  # type: ignore
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
    async def set_color(self, interaction: Interaction, 
                        color: str = SlashOption(
                            name="color",
                            description="Choose a color for the embeds",
                            choices={"Red": "red", "Orange": "orange", "Yellow": "yellow", "Green": "green", 
                                     "Blue": "blue", "Purple": "purple", "Black": "black", "Gray": "gray",
                                    }
                        )):
        try:
            color_dto = ColorDTO(color)
            server_dto = ServerDTO(str(interaction.guild.id), interaction.guild.name)  # type: ignore
            server_color_dto = ServerColorDTO(server_dto, color_dto)
            server_color_bll = ServerColorBLL()

            if not server_color_bll.insert_server_color(server_color_dto):
                server_color_bll.update_server_color_by_id_server(server_dto.get_id_server(), server_color_dto)

            hex_color = server_color_dto.get_color().get_hex_color()
            embed = nextcord.Embed(title="Set color", description=f"Set color **{color_dto.get_name_color()}** successfully.", color=int(hex_color, 16))
            
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")
            print(f"Error: {e}")

    @nextcord.slash_command(name="show", description="Shows a list of feeds in channels.")
    async def show(self, interaction: Interaction):
        try:
            value_channel = ""
            value_feed = ""
            num = 0
            channel_feed_bll = ChannelFeedBLL()
            id_server = str(interaction.guild.id)  # type: ignore # Ensures id_server is always defined
            
            for channel_feed_dto in channel_feed_bll.get_all_channel_feed():
                channel_dto = channel_feed_dto.get_channel()
                feed_dto = channel_feed_dto.get_feed()
                
                channel = self.bot.get_channel(int(channel_dto.get_id_channel()))
                if channel in interaction.guild.channels: # type: ignore
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
            await interaction.send(embed=embed)
            
        except Exception as e:
            await interaction.send(f"Error: {e}")
            print(f"Error: {e}")
            
async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
