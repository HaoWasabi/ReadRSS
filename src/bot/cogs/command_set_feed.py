import logging
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, TextChannel
from ..BLL.feed_bll import FeedBLL
from ..BLL.channel_bll import ChannelBLL
from ..BLL.emty_bll import EmtyBLL
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..BLL.server_bll import ServerBLL
from ..DTO.server_dto import ServerDTO
from ..DTO.channel_dto import ChannelDTO
from ..DTO.channel_feed_dto import ChannelFeedDTO
from ..utils.commands_cog import CommandsCog
from ..utils.handle_rss import get_rss_link, read_rss_link

logger = logging.getLogger("CommandSetFeed")

class CommandSetFeed(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="setfeed")
    async def set_feed(self, ctx, channel: TextChannel, link_rss: str):
        if await self.is_dm_channel(ctx):
            return

        if not link_rss:
            await ctx.send('This command requires an RSS link.')
            return

        await self._handle_feed(ctx, channel, link_rss)

    @nextcord.slash_command(name="setfeed", description="Set feed notification channel")
    async def slash_set_feed(self, interaction: Interaction, 
                             channel: TextChannel = SlashOption(description="The target channel"), 
                             link_rss: str = SlashOption(description="RSS feed link", required=False), 
                             url: str = SlashOption(description="Website URL", required=False)):
        await interaction.response.defer()

        # Check if the command is being executed in a guild (server)
        if not interaction.guild:
            await interaction.followup.send('This command can only be used in a server.')
            return

        if link_rss and url:
            await interaction.followup.send('Please provide only one: either an RSS link or a URL.')
            return

        if not link_rss and not url:
            await interaction.followup.send('This command requires an RSS link or URL.')
            return

        if not link_rss and url:
            link_rss = get_rss_link(url)
            if not link_rss:
                await interaction.followup.send('No RSS link found for the provided URL.')
                return

        await self._handle_feed(interaction.followup, channel, link_rss)

    async def _handle_feed(self, source, channel: TextChannel, link_rss: str):
        try:
            feed_dto, emty_dto = read_rss_link(rss_link=link_rss)
            if not feed_dto or not emty_dto:
                await source.send(f"No RSS feed or posts found.")
                return

            # Ensure guild exists
            if channel.guild:
                server_dto = ServerDTO(str(channel.guild.id), channel.guild.name)
            else:
                server_dto = ServerDTO(str(source.author.id), source.author.name)

            channel_dto = ChannelDTO(str(channel.id), channel.name, server_dto.get_server_id())

            ChannelBLL().insert_channel(channel_dto)
            FeedBLL().insert_feed(feed_dto)
            ChannelFeedBLL().insert_channel_feed(ChannelFeedDTO(channel_dto, feed_dto))
            EmtyBLL().insert_emty(emty_dto)
            ServerBLL().insert_server(server_dto)

            await source.send(f"Successfully set feed for {channel.mention}.")
        
        except Exception as e:
            await source.send(f"Error: {e}")
            logger.error(f"Error: {e}")

async def setup(bot):
   bot.add_cog(CommandSetFeed(bot))
