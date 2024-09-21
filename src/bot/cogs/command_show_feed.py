import logging
from ..utils.commands_cog import CommandsCog
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..GUI.embed_custom import EmbedCustom

logger = logging.getLogger("CommandShowChannel")

class CommandShowChannel(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)
        
    @commands.command(name="show")
    async def command_show(self, ctx):
        if await self.is_dm_channel(ctx):
            return
        await self._show_channel(ctx)
        
    @nextcord.slash_command(name="show", description="Show the feed notification channel")
    async def slash_command_show(self, interaction: Interaction):
        await interaction.response.defer()
        if await self.is_dm_channel(interaction):
            return
        await self._show_channel(interaction)

    async def _show_channel(self, ctx):
        try:
            channel_feed_bll = ChannelFeedBLL()
            server_data = {}
            num_feeds = 0

            for channel_feed_dto in channel_feed_bll.get_all_channel_feed():
                channel_id = int(channel_feed_dto.get_channel().get_channel_id())
                channel = self.bot.get_channel(channel_id)

                if channel and channel in ctx.guild.channels:
                    server_name = f"**Server:** {ctx.guild.name} ({ctx.guild.id})"
                    channel_info = f"- **Channel:** {channel.mention} - [{channel_feed_dto.get_feed().get_title_feed()}]({channel_feed_dto.get_feed().get_link_feed()})"
                    
                    server_data.setdefault(server_name, []).append(channel_info)
                    num_feeds += 1

            embed = EmbedCustom(
                id_server=str(ctx.guild.id),
                title="List of Feeds in Channels",
                description=f"You have {num_feeds} feeds in channels:"
            )

            for server_name, channels in server_data.items():
                embed.add_field(name=server_name, value="\n".join(channels), inline=False)

            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

async def setup(bot):
   bot.add_cog(CommandShowChannel(bot))
