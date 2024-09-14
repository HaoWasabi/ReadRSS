import logging
import nextcord
from nextcord.ext import commands
from nextcord import SlashOption, Interaction, TextChannel
from typing import Optional

from ..DTO.server_dto import ServerDTO
from ..DTO.channel_dto import ChannelDTO
from ..DTO.color_dto import ColorDTO
from ..DTO.channel_feed_dto import ChannelFeedDTO
from ..DTO.server_channel_dto import ServerChannelDTO
from ..DTO.server_color_dto import ServerColorDTO

from ..BLL.feed_bll import FeedBLL
from ..BLL.server_bll import ServerBLL
from ..BLL.channel_bll import ChannelBLL
from ..BLL.feed_emty_bll import FeedEmtyBLL
from ..BLL.channel_emty_bll import ChannelEmtyBLL
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..BLL.server_channel_bll import ServerChannelBLL
from ..BLL.server_color_bll import ServerColorBLL

from ..GUI.embed_test import EmbedTest
from ..GUI.custom_embed import CustomEmbed
from ..GUI.select_clear import SelectClear
from ..GUI.button_of_help_command import ButtonOfHelpCommnad
from ..GUI.button_of_ctrl_command import ButtonOfCtrlCommand

from ..utils.read_rss_without_saving import ReadRSSWithoutSaving
from ..utils.check_cogs import CheckCogs
from ..utils.read_rss import ReadRSS
from ..utils.get_rss import GetRSS

logger = logging.getLogger('SlashCommands')

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping", description="Check bot latency")
    async def ping(self, interaction: Interaction):
        result = f'Pong! {round(self.bot.latency * 1000)}ms'
        await interaction.response.send_message(result)

    @nextcord.slash_command(name="clear", description="Clear channel post history")
    async def clear_history(self, interaction: Interaction, channel: TextChannel = SlashOption(description="The target channel"), link_atom_feed: Optional[str] = SlashOption(description="The Atom/RSS feed link")):
        try:
            channel_emty_bll = ChannelEmtyBLL()
            if link_atom_feed is None:
                channel_emty_bll.delete_channel_emty_by_id_channel(str(channel.id))
            else:
                channel_feed_bll = ChannelFeedBLL()
                feed_emty_bll = FeedEmtyBLL()
                list_channel_feed = channel_feed_bll.get_all_channel_feed()
                list_feed_emty = feed_emty_bll.get_all_feed_emty()

                for channel_feed in list_channel_feed:
                    feed_of_channel_feed = channel_feed.get_feed()

                    for feed_emty in list_feed_emty:
                        feed_of_feed_emty = feed_emty.get_feed()
                        link_emty_of_feed_emty = feed_emty.get_emty().get_link_emty()

                        if feed_of_channel_feed == feed_of_feed_emty and feed_of_channel_feed.get_link_atom_feed() == link_atom_feed:
                            channel_emty_bll.delete_channel_emty_by_id_channel_and_link_emty(str(channel.id), link_emty_of_feed_emty)

            # Đánh dấu rằng phản hồi sẽ được gửi sau
            await interaction.response.send_message(f"Deleted the history of posts in {channel.mention} successfully.")
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            logger.error(f"Error: {e}")

    @nextcord.slash_command(name="delete_feed", description="Delete feed notification channel settings")
    async def delete_feed(self, interaction: Interaction, 
                        channel: TextChannel = SlashOption(description="The target channel"), 
                        link_atom_feed: Optional[str] = SlashOption(description="The Atom/RSS feed link"), 
                        link_feed: Optional[str] = SlashOption(description="The feed link")):
        try:
            channel_feed_bll = ChannelFeedBLL()
            channel_emty_bll = ChannelEmtyBLL()
            feed_emty_bll = FeedEmtyBLL()

            if link_atom_feed or link_feed:
                list_channel_feed = channel_feed_bll.get_all_channel_feed_by_id_channel(str(channel.id))
                list_feed_emty = []

                if link_feed:
                    channel_feed_bll.delete_channel_feed_by_id_channel_and_link_feed(str(channel.id), link_feed)
                    list_feed_emty = feed_emty_bll.get_all_feed_emty_by_link_feed(link_feed)
                elif link_atom_feed:
                    channel_feed_bll.delete_channel_feed_by_id_channel_and_link_atom_feed(str(channel.id), link_atom_feed)
                    list_feed_emty = feed_emty_bll.get_all_feed_emty_by_link_atom_feed(link_atom_feed)

                for channel_feed in list_channel_feed:
                    for feed_emty in list_feed_emty:
                        if channel_feed.get_feed() == feed_emty.get_feed() and (
                            channel_feed.get_feed().get_link_atom_feed() == link_atom_feed or channel_feed.get_feed().get_link_feed() == link_feed):
                            channel_emty_bll.delete_channel_emty_by_id_channel_and_link_emty(str(channel.id), feed_emty.get_emty().get_link_emty())

                if len(list_channel_feed) == 1:
                    self.delete_channel_data(channel.id)
            
            else:
                self.delete_channel_data(channel.id)

            await interaction.response.send_message(f"Deleted feed settings for {channel.mention} successfully.")
        
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            logger.error(f"Error: {e}")

    def delete_channel_data(self, channel_id):
        """Helper function to delete all data related to a channel."""
        channel_feed_bll = ChannelFeedBLL()
        channel_emty_bll = ChannelEmtyBLL()
        server_channel_bll = ServerChannelBLL()
        channel_bll = ChannelBLL()
        
        channel_feed_bll.delete_channel_feed_by_id_channel(str(channel_id))
        channel_emty_bll.delete_channel_emty_by_id_channel(str(channel_id))
        server_channel_bll.delete_server_channel_by_id_channel(str(channel_id))
        channel_bll.delete_channel_by_id_channel(str(channel_id))

    @nextcord.slash_command(name="test", description="Test sending an RSS feed")
    async def test_feed(self, interaction: nextcord.Interaction,  
                        channel: Optional[TextChannel] = SlashOption(description="The target channel"),
                        link_atom_feed: Optional[str] = None, 
                        link_feed: Optional[str] = None):
        try:
            # Kiểm tra nếu chỉ có link_feed, lấy link_atom_feed từ RSS
            if link_atom_feed is None and link_feed is not None:
                get_rss = GetRSS(link_feed)
                link_atom_feed = get_rss.get_rss_link()
                
                if link_atom_feed is None:
                    await interaction.response.send_message('Link RSS feed is not found.', ephemeral=True)
                    return

            # Kiểm tra nếu link_atom_feed không tồn tại
            if link_atom_feed is None:
                await interaction.response.send_message('Link Atom feed is not found.', ephemeral=True)
                return
            
            # Đọc RSS feed và lấy entry đầu tiên
            read_rss = ReadRSSWithoutSaving(link_atom_feed)    
            feed_emty_dto = read_rss.get_first_feed_emty()

            if feed_emty_dto is None:
                raise TypeError("link_first_entry is None")
            
            # Kiểm tra nếu tin nhắn đến từ DMChannel
            if CheckCogs.check_dm_channel(interaction):
                id_server = "DM"
                embed = EmbedTest(id_server, feed_emty_dto)
                await interaction.response.send_message(embed=embed)
            
            elif channel is not None:
                id_server = str(interaction.guild.id)  # type: ignore # Sử dụng interaction.guild.id nếu không phải là DM          
                embed = EmbedTest(id_server, feed_emty_dto)
                await interaction.response.send_message(f"Test sent to {channel.mention}.")
                await channel.send(embed=embed)
            
            elif channel is None:
                id_server = str(interaction.guild.id)   # type: ignore # Sử dụng interaction.guild.id nếu không phải là D              
                embed = EmbedTest(id_server, feed_emty_dto)
                await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            # Gửi thông báo lỗi nếu xảy ra ngoại lệ
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            logger.error(f"Error: {e}")

    @nextcord.slash_command(name="set_feed", description="Set feed notification channel")
    async def set_feed(self, interaction: Interaction, 
                       channel: TextChannel = SlashOption(description="The target channel"), 
                       link_atom_feed: Optional[str] = None, 
                       link_feed: Optional[str] = None):
        try:
            if link_atom_feed is None and link_feed is not None:
                get_rss = GetRSS(link_feed)
                if get_rss.get_rss_link() is None:
                    await interaction.response.send_message(f'Link RSS feed is not found.')
                    return
                else: 
                    link_atom_feed = get_rss.get_rss_link()
            
            if link_atom_feed is None:
            # Đánh dấu rằng phản hồi sẽ được gửi sau
                await interaction.response.send_message(f'Link Atom feed is not found.')
                return
            
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

            channel_feed_bll.insert_channel_feed(channel_feed_dto)
            server_channel_bll.insert_server_channel(server_channel_dto)
            channel_bll.insert_channel(channel_dto)
            server_bll.insert_server(server_dto)

             # Đánh dấu rằng phản hồi sẽ được gửi sau
            await interaction.response.send_message(f'Successfully set the feed for {channel.mention}.')
        
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            logger.error(f"Error: {e}")

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
            embed = CustomEmbed(
                id_server=server_dto.get_id_server(),
                title="Set color", 
                description=f"Set color **{color_dto.get_name_color()}** successfully.", 
                color=int(hex_color, 16))
            
            # Đánh dấu rằng phản hồi sẽ được gửi sau
            await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            logger.error(f"Error: {e}")

    @nextcord.slash_command(name="show", description="Shows a list of feeds in channels.")
    async def show(self, interaction: Interaction):
        try:
            num = 0
            channel_feed_bll = ChannelFeedBLL()
            id_server = str(interaction.guild.id)  # type: ignore
            
            # Tạo dictionary để nhóm các channel và feed theo server
            server_data = {}
            
            for channel_feed_dto in channel_feed_bll.get_all_channel_feed():
                channel_dto = channel_feed_dto.get_channel()
                feed_dto = channel_feed_dto.get_feed()
                
                channel = self.bot.get_channel(int(channel_dto.get_id_channel()))
                if channel in interaction.guild.channels:  # type: ignore
                    server_name = f"**Server:** {interaction.guild.name} ({interaction.guild.id})" # type: ignore
                    channel_info = f"- **Channel:** {channel.mention} - [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})"
                    
                    # Thêm channel và feed vào server tương ứng
                    if server_name not in server_data:
                        server_data[server_name] = []
                    server_data[server_name].append(channel_info)
                    num += 1
            
            # Chuẩn bị nội dung cho embed
            embed = CustomEmbed(
                id_server=id_server,
                title="List of Feeds in Channels",
                description=f"You have {num} feeds in channels:",
            )
            
            # Thêm thông tin server và channel vào embed
            for server_name, channels in server_data.items():
                embed.add_field(
                    name=server_name,
                    value="\n".join(channels) if channels else "No channels found.",
                    inline=False
                )
            
            # Đánh dấu rằng phản hồi sẽ được gửi sau
            await interaction.response.send_message(embed=embed)  # Sửa từ "ctx.send" thành "interaction.send"
                
        except Exception as e:
            # Thông báo lỗi
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)  # Gửi lỗi một cách riêng tư
            logger.error(f"Error: {e}")
        
    @nextcord.slash_command(name="help", description="List of commands")
    async def help(self, interaction: Interaction):
        try:
            available_commands = [command.name for command in self.bot.commands]
            available_slash_commands = [command.name for command in self.bot.get_application_commands()]
            
            command_list_1 = ", ".join(available_commands)
            command_list_2 = ", ".join(available_slash_commands)  # type: ignore
            
            if interaction.guild is not None:
                server_color_bll = ServerColorBLL()
                server_dto = ServerDTO(str(interaction.guild.id), interaction.guild.name)
                server_color_dto = server_color_bll.get_server_color_by_id_server(server_dto.get_id_server())
                hex_color = server_color_dto.get_color().get_hex_color()  # type: ignore
                
                embed = CustomEmbed(
                    id_server=str(interaction.guild.id), 
                    title="List of commands",
                    description=f'''
command prefix `{self.bot.command_prefix}`
- The current commands have: {command_list_1}
- The current slash commands have: {command_list_2}
                    ''',
                    color=int(hex_color, 16) if hex_color else nextcord.Color(0x808080)
                )
            # Đánh dấu rằng phản hồi sẽ được gửi sau
            await interaction.response.send_message(embed=embed, view=ButtonOfHelpCommnad())
        
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            logger.error(f"Error: {e}")

    @nextcord.slash_command(name="get_rss", description="Get the RSS link of a website")
    async def get_rss(self, interaction: Interaction, url: str = SlashOption(description="The website URL")):
        try:
            link_rss = GetRSS(url).get_rss_link()
            await interaction.response.send_message(f"RSS link: {link_rss}") if link_rss else await interaction.response.send_message("No RSS link found.")
        
        except Exception as e:
            # Đánh dấu rằng phản hồi sẽ được gửi sau
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            logger.error(f"Error: {e}")
            
def setup(bot):
    bot.add_cog(SlashCommands(bot))
