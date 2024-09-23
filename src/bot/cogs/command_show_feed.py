import logging
import nextcord
from nextcord.ext import commands
from nextcord import Interaction

from ..utils.commands_cog import CommandsCog
from ..BLL import FeedBLL
from ..GUI import EmbedCustom

logger = logging.getLogger("CommandShowChannel")


class CommandShowChannel(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="show")
    async def command_show(self, ctx):
        if await self.is_dm_channel(ctx):
            return
        await self._show_channel(ctx=ctx, guild=ctx.guild, user=ctx.author)

    @nextcord.slash_command(name="show", description="Show the feed notification channel")
    async def slash_command_show(self, interaction: Interaction):
        await interaction.response.defer()
        if await self.is_dm_channel(interaction):
            return
        await self._show_channel(ctx=interaction.followup, guild=interaction.guild, user=interaction.user)

    async def _show_channel(self, ctx, guild=None, user=None):
        try:
            # Kiểm tra xem có phải là DM không
            if guild is not None:
                guild_id = guild.id
                guild_name = guild.name
            else:
                guild_id = "DM"
                guild_name = "Direct Message"

            feed_bll = FeedBLL()
            server_data = {}
            num_feeds = 0

            for feed_dto in feed_bll.get_all_feed():
                channel_id = int(feed_dto.channel_id)  # type: ignore
                channel = self.bot.get_channel(channel_id)

                # Kiểm tra nếu channel tồn tại và là một phần của guild
                if channel and channel.guild.id == guild_id:
                    server_name = f"**Server:** {guild_name} ({guild_id})"
                    channel_info = f"- **Channel:** {channel.mention} - [{
                        feed_dto.title_feed}]({feed_dto.link_feed})"

                    server_data.setdefault(
                        server_name, []).append(channel_info)
                    num_feeds += 1

            embed = EmbedCustom(
                id_server=guild_id,
                title="List of Feeds in Channels",
                description=f"You have {num_feeds} feeds in channels:"
            )

            for server_name, channels in server_data.items():
                embed.add_field(name=server_name, value="\n".join(
                    channels), inline=False)

            await ctx.send(embed=embed)  # Gửi embed

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")


async def setup(bot):
    bot.add_cog(CommandShowChannel(bot))
