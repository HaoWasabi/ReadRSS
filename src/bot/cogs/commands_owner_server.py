import datetime
import logging
from tkinter import NO
from nextcord.ext import commands
from nextcord import TextChannel, Embed
from typing import Optional

from nextcord.ext.commands import Context

from ..BLL.qr_pay_code_bll import QrPayCodeBLL

from ..utils.datetime_format import datetime_to_string

from ..DTO.qr_code_pay_dto import QrPayCodeDTO
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
from ..BLL.feed_emty_bll import FeedEmtyBLL
from ..BLL.channel_emty_bll import ChannelEmtyBLL
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..BLL.server_channel_bll import ServerChannelBLL

from ..GUI.custom_embed import CustomEmbed
from ..utils.check_cogs import CheckCogs
from ..utils.read_rss import ReadRSS
from ..utils.create_qr_payment import QRGenerator

logger = logging.getLogger('AdminServerCommands')


class AdminServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def is_dm_channel(self, ctx):
        if await CheckCogs.is_dm_channel(ctx):
            await ctx.send("Can not send DMChannels")
            return True
        else: 
            return False
        
    async def is_onwer_server(self, ctx):
        if await CheckCogs.is_server_owner(ctx=ctx):
            return True
        else:
            await ctx.send("You need to be the server owner to use this command.")
            return False

    @commands.command(name="clear")
    async def clear_history(self, ctx, channel: TextChannel, link_atom_feed: Optional[str] = None):
        if await self.is_dm_channel(ctx): 
            return

        if not await self.is_onwer_server(ctx):
            return

        try:
            channel_emty_bll = ChannelEmtyBLL()

            if link_atom_feed:
                channel_feed_bll = ChannelFeedBLL()
                feed_emty_bll = FeedEmtyBLL()

                list_channel_feed = channel_feed_bll.get_all_channel_feed()
                list_feed_emty = feed_emty_bll.get_all_feed_emty()

                for channel_feed in list_channel_feed:
                    if channel_feed.get_feed().get_link_atom_feed() == link_atom_feed:
                        for feed_emty in list_feed_emty:
                            if channel_feed.get_feed() == feed_emty.get_feed():
                                link_emty_of_feed_emty = feed_emty.get_emty().get_link_emty()
                                channel_emty_bll.delete_channel_emty_by_id_channel_and_link_emty(str(channel.id), link_emty_of_feed_emty)
            else:
                channel_emty_bll.delete_channel_emty_by_id_channel(str(channel.id))

            await ctx.send(f"Deleted the history of posts in {channel.mention} successfully.")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    @commands.command(name="delete_feed")
    async def delete_feed(self, ctx, channel: TextChannel, link_atom_feed: Optional[str] = None):
        if await self.is_dm_channel(ctx):
            return

        if not await self.is_onwer_server(ctx):
            return

        try:
            channel_feed_bll = ChannelFeedBLL()
            channel_emty_bll = ChannelEmtyBLL()

            if link_atom_feed:
                feed_emty_bll = FeedEmtyBLL()
                channel_feed_bll.delete_channel_feed_by_id_channel_and_link_atom_feed(str(channel.id), link_atom_feed)
                
                list_channel_feed = channel_feed_bll.get_all_channel_feed()
                list_feed_emty = feed_emty_bll.get_all_feed_emty_by_link_atom_feed(link_atom_feed)

                for channel_feed in list_channel_feed:
                    feed_of_channel_feed = channel_feed.get_feed()
                    for feed_emty in list_feed_emty:
                        feed_of_feed_emty = feed_emty.get_feed()
                        link_emty_of_feed_emty = feed_emty.get_emty().get_link_emty()

                        if feed_of_channel_feed == feed_of_feed_emty and feed_of_channel_feed.get_link_atom_feed() == link_atom_feed:
                            channel_emty_bll.delete_channel_emty_by_id_channel_and_link_emty(str(channel.id), link_emty_of_feed_emty)
            else:
                server_channel_bll = ServerChannelBLL()
                channel_bll = ChannelBLL()
                channel_feed_bll.delete_channel_feed_by_id_channel(str(channel.id))
                channel_emty_bll.delete_channel_emty_by_id_channel(str(channel.id))
                server_channel_bll.delete_server_channel_by_id_channel(str(channel.id))
                channel_bll.delete_channel_by_id_channel(str(channel.id))

            await ctx.send(f"Deleted feed settings for {channel.mention} successfully.")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    @commands.command(name="set_feed")
    async def set_feed(self, ctx, channel: TextChannel, link_atom_feed: str):
        if await self.is_dm_channel(ctx):
            return

        if not await self.is_onwer_server(ctx):
            return

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

            await ctx.send(f"Set {channel.mention} to have {link_atom_feed} feed successfully.")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    @commands.command(name="set_color")
    async def set_color(self, ctx, color: str):
        if await self.is_dm_channel(ctx):
            return

        if not await self.is_onwer_server(ctx):
            return
        
        try:
            color_dto = ColorDTO(color)
            server_dto = ServerDTO(str(ctx.guild.id), ctx.guild.name)
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

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    @commands.command(name="show")
    async def show_feeds(self, ctx):
        if await self.is_dm_channel(ctx):
            return

        if not await self.is_onwer_server(ctx):
            return

        try:
            channel_feed_bll = ChannelFeedBLL()
            server_data = {}
            num = 0

            for channel_feed_dto in channel_feed_bll.get_all_channel_feed():
                channel = self.bot.get_channel(int(channel_feed_dto.get_channel().get_id_channel()))
                if channel and channel in ctx.guild.channels:
                    server_name = f"**Server:** {ctx.guild.name} ({ctx.guild.id})"
                    channel_info = f"- **Channel:** {channel.mention} - [{channel_feed_dto.get_feed().get_title_feed()}]({channel_feed_dto.get_feed().get_link_feed()})"
                    server_data.setdefault(server_name, []).append(channel_info)
                    num += 1

            embed = CustomEmbed(
                id_server=str(ctx.guild.id),
                title="List of Feeds in Channels",
                description=f"You have {num} feeds in channels:")

            for server_name, channels in server_data.items():
                embed.add_field(name=server_name, value="\n".join(channels), inline=False)

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")
        
async def setup(bot):
    bot.add_cog(AdminServerCommands(bot))
