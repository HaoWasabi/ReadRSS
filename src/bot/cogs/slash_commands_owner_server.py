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

from ..GUI.custom_embed import CustomEmbed

from ..utils.read_rss import ReadRSS
from ..utils.get_rss import GetRSS

class SlashCommandsOnwerServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="clear", description="Clear channel post history")
    async def clear_history(self, interaction: Interaction, channel: TextChannel = SlashOption(description="The target channel"), link_atom_feed: Optional[str] = SlashOption(description="The Atom/RSS feed link")):
        await interaction.response.defer()
        
        if not interaction.guild:
            await interaction.followup.send("This command is only available in servers.", ephemeral=True)
            return
        
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
            await interaction.followup.send(f"Deleted the history of posts in {channel.mention} successfully.")
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")

    @nextcord.slash_command(name="delete_feed", description="Delete feed notification channel settings")
    async def delete_feed(self, interaction: Interaction, 
                        channel: TextChannel = SlashOption(description="The target channel"), 
                        link_atom_feed: Optional[str] = SlashOption(description="The Atom/RSS feed link"), 
                        link_feed: Optional[str] = SlashOption(description="The feed link")):
        await interaction.response.defer()
        
        if not interaction.guild:
            await interaction.followup.send("This command is only available in servers.", ephemeral=True)
            return
        
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

            await interaction.followup.send(f"Deleted feed settings for {channel.mention} successfully.")
        
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")

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

    @nextcord.slash_command(name="set_feed", description="Set feed notification channel")
    async def set_feed(self, interaction: Interaction, 
                       channel: TextChannel = SlashOption(description="The target channel"), 
                       link_atom_feed: Optional[str] = None, 
                       link_feed: Optional[str] = None):
        await interaction.response.defer()
        
        if not interaction.guild:
            await interaction.followup.send("This command is only available in servers.", ephemeral=True)
            return
        
        try:
            if link_atom_feed is None and link_feed is not None:
                get_rss = GetRSS(link_feed)
                if get_rss.get_rss_link() is None:
                    await interaction.followup.send(f'Link RSS feed is not found.')
                    return
                else: 
                    link_atom_feed = get_rss.get_rss_link()
            
            if link_atom_feed is None:
            # Đánh dấu rằng phản hồi sẽ được gửi sau
                await interaction.followup.send(f'Link Atom feed is not found.')
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
            await interaction.followup.send(f'Successfully set the feed for {channel.mention}.')
        
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
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
        await interaction.response.defer()
        
        if not interaction.guild:
            await interaction.followup.send("This command is only available in servers.", ephemeral=True)
            return
        
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
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")

    @nextcord.slash_command(name="show", description="Shows a list of feeds in channels.")
    async def show(self, interaction: Interaction):
        await interaction.response.defer()
        
        if not interaction.guild:
            await interaction.followup.send("This command is only available in servers.", ephemeral=True)
            return
        
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
            await interaction.followup.send(embed=embed)  # Sửa từ "ctx.send" thành "interaction.send"
                
        except Exception as e:
            # Thông báo lỗi
            await interaction.followup.send(f"Error: {e}", ephemeral=True)  # Gửi lỗi một cách riêng tư
            print(f"Error: {e}")
            
def setup(bot):
    bot.add_cog(SlashCommandsOnwerServer(bot))
