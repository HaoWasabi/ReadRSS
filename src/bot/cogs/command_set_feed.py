import logging
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, TextChannel

from ..BLL import FeedBLL, ChannelBLL, ServerBLL
from ..DTO import ServerDTO, ChannelDTO

from ..utils.commands_cog import CommandsCog
from ..utils.handle_rss import get_rss_link, read_rss_link

logger = logging.getLogger("CommandSetFeed")


class CommandSetFeed(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="setfeed")
    async def set_feed(self, ctx, channel: TextChannel, link_rss: str):
        """Lệnh dùng để đăng ký kênh nhận thông báo từ RSS feed."""
        if await self.is_dm_channel(ctx):
            await ctx.send("Lệnh này chỉ dùng trong server.")
            return

        if not link_rss:
            await ctx.send('Vui lòng cung cấp một đường dẫn RSS hợp lệ.')
            return

        await self._handle_feed(ctx, channel, link_rss)

    @nextcord.slash_command(name="setfeed", description="Set feed notification channel")
    async def slash_set_feed(self, interaction: Interaction,
                             channel: TextChannel = SlashOption(
                                 description="Kênh thông báo RSS"),
                             link_rss: str = SlashOption(
                                 description="Đường dẫn RSS", required=False),
                             url: str = SlashOption(description="Đường dẫn trang web", required=False)):
        """Lệnh slash dùng để thiết lập kênh nhận thông báo từ RSS feed."""
        await interaction.response.defer()

        if not interaction.guild:
            await interaction.followup.send('Lệnh này chỉ sử dụng trong server.')
            return

        if link_rss and url:
            await interaction.followup.send('Vui lòng chỉ cung cấp một: đường dẫn RSS hoặc URL.')
            return

        if not link_rss and not url:
            await interaction.followup.send('Vui lòng cung cấp một đường dẫn RSS hoặc URL.')
            return

        if not link_rss and url:
            link_rss = get_rss_link(url)  # type: ignore
            if not link_rss:
                await interaction.followup.send('Không tìm thấy link RSS cho trang web đã cung cấp.')
                return

        await self._handle_feed(interaction.followup, channel, link_rss)

    async def _handle_feed(self, source, channel: TextChannel, link_rss: str):
        """Xử lý cài đặt feed và lưu vào cơ sở dữ liệu."""
        try:
            feed_data = read_rss_link(rss_link=link_rss)
            if not feed_data or not feed_data[0]:
                await source.send("Không tìm thấy dữ liệu RSS từ link cung cấp.")
                return

            feed_dto = feed_data[0]

            # Tạo ServerDTO và ChannelDTO
            server_dto = ServerDTO(str(channel.guild.id), channel.guild.name)
            channel_dto = ChannelDTO(
                str(channel.id), channel.name, server_dto.server_id)

            # Lưu thông tin vào cơ sở dữ liệu
            ServerBLL().insert_server(server_dto)
            ChannelBLL().insert_channel(channel_dto)

            feed_dto.channel_id = channel_dto.channel_id
            FeedBLL().insert_feed(feed_dto)

            await source.send(f"Đã đăng ký feed thành công cho kênh {channel.mention}.")

        except Exception as e:
            await source.send(f"Đã xảy ra lỗi: {e}")
            logger.error(f"Lỗi khi đăng ký feed: {e}")


async def setup(bot):
    """Hàm khởi tạo để thêm cog vào bot."""
    bot.add_cog(CommandSetFeed(bot))
