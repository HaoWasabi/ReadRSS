import logging
from ..utils.commands_cog import CommandsCog
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from ..BLL.feed_bll import FeedBLL
from ..GUI.embed_custom import EmbedCustom
from ..utils.check_have_premium import check_have_premium


logger = logging.getLogger("CommandShowChannel")

class CommandShowChannel(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)
        
    @commands.command(name="show")
    async def command_show(self, ctx):
        '''Show the feed notification channel'''
        await self._show_channel(ctx, ctx.guild, ctx.author)
        
    @nextcord.slash_command(name="show", description="Show the feed notification channel")
    async def slash_command_show(self, interaction: Interaction):
        # Trì hoãn phản hồi để xử lý lệnh
        await interaction.response.defer()
        
        # Kiểm tra xem lệnh được gọi trong DM hay Guild
        if isinstance(interaction.channel, nextcord.DMChannel):
            await self._show_channel(interaction.followup, None, interaction.user)
        else:
            await self._show_channel(interaction.followup, interaction.guild, interaction.user)

    async def _show_channel(self, ctx, guild, user):
        server_id = str(guild.id if guild else user.id )
        server_name = guild.name if guild else user.name 
        
        try:
            if not check_have_premium(str(user.id)):
                await ctx.send("This command is only available for premium servers.")
                return
            
            feed_bll = FeedBLL()
            server_data = {}
            num_feeds = 0

            for feed_dto in feed_bll.get_all_feed():
                channel_id = int(feed_dto.get_channel_id())
                
                # Kiểm tra nếu lệnh được gọi trong DMChannel hoặc trong guild
                if isinstance(ctx.channel, nextcord.DMChannel):
                    # Với kênh DM, kiểm tra nếu channel_id trùng với user.id
                    if channel_id == user.id:
                        server_name = f"**User:** {user.name} (DM)"
                        channel_info = f"- **Notification:** [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})"
                        
                        server_data.setdefault(server_name, []).append(channel_info)
                        num_feeds += 1
                else:
                    channel = self.bot.get_channel(channel_id)

                    # Kiểm tra nếu channel tồn tại và là một phần của guild
                    if channel and channel.guild.id == server_id:
                        server_name = f"**Server:** {server_name} ({server_id})"
                        channel_info = f"- **Channel:** {channel.mention} - [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})"
                        
                        server_data.setdefault(server_name, []).append(channel_info)
                        num_feeds += 1

            embed = EmbedCustom(
                id_server=server_id,
                title="List of Feeds in Channels",
                description=f"You have {num_feeds} feeds in channels:"
            )

            for server_name, channels in server_data.items():
                embed.add_field(name=server_name, value="\n".join(channels), inline=False)

            # Gửi embed trả về từ slash command (ctx trong trường hợp này là followup)
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")


async def setup(bot):
    bot.add_cog(CommandShowChannel(bot))
