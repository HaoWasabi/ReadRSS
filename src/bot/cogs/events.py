import nextcord
from nextcord.ext import commands
from nextcord.ext import tasks

from ..DTO.server_channel_dto import ServerChannelDTO
from ..DTO.channel_emty_dto import ChannelEmtyDTO
from ..DTO.server_color_dto import ServerColorDTO
from ..DTO.channel_dto import ChannelDTO
from ..DTO.server_dto import ServerDTO
from ..DTO.color_dto import ColorDTO

from ..BLL.server_channel_bll import ServerChannelBLL
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..BLL.channel_emty_bll import ChannelEmtyBLL
from ..BLL.feed_emty_bll import FeedEmtyBLL
from ..BLL.server_color_bll import ServerColorBLL
from ..BLL.channel_bll import ChannelBLL
from ..BLL.server_bll import ServerBLL

from ..GUI.feed_embed import FeedEmbed
from ..GUI.custom_embed import CustomEmbed
from ..utils.read_rss import ReadRSS

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def load_guilds(self):
        try:
            server_bll = ServerBLL() 
            channel_bll = ChannelBLL()
            server_color_bll = ServerColorBLL()
            guilds = self.bot.guilds
            
            list_channel = channel_bll.get_all_channel()
            for guild in guilds:
                server_dto = ServerDTO(str(guild.id), str(guild.name))
                server_bll.insert_server(server_dto)
                
                color_dto = ColorDTO("blue")
                server_color_bll.insert_server_color(ServerColorDTO(server_dto, color_dto))
                
                for channel in guild.channels:
                    channel_dto = ChannelDTO(str(channel.id), channel.name)
                    for channel_of_list_channel in list_channel:
                        if channel_dto.get_id_channel() == channel_of_list_channel.get_id_channel() and channel_dto.get_name_channel() != channel_of_list_channel.get_name_channel():
                            channel_bll.update_channel_by_id_channel(str(channel.id), channel_dto)

                if not server_bll.insert_server(server_dto):
                    server_bll.update_server_by_id_server(str(guild.id), server_dto)
                    
        except Exception as e:
            print(f"Error loading guilds: {e}")
            
    async def load_list_feed(self):
            channel_feed_bll = ChannelFeedBLL()
            channel_emty_bll = ChannelEmtyBLL()
            feed_emty_bll = FeedEmtyBLL()

            list_channel_feed = channel_feed_bll.get_all_channel_feed()
            list_feed_emty = feed_emty_bll.get_all_feed_emty()
            
            for channel_feed in list_channel_feed:
                feed_of_channel_feed = channel_feed.get_feed()
                ReadRSS(feed_of_channel_feed.get_link_atom_feed())
                
                channel_of_channel_feed = channel_feed.get_channel()
                channel_id_of_channel_feed = int(channel_of_channel_feed.get_id_channel())
                
                for feed_emty in list_feed_emty:
                    feed_of_feed_emty = feed_emty.get_feed()
                    emty_of_feed_emty = feed_emty.get_emty()
                    
                    if feed_of_channel_feed == feed_of_feed_emty:
                        channel_emty = ChannelEmtyDTO(channel_of_channel_feed, emty_of_feed_emty)
                        link_emty = emty_of_feed_emty.get_link_emty()
                        
                        if channel_emty_bll.insert_channel_emty(channel_emty):
                            channel_of_channel_emty = channel_emty.get_channel()
                            channel_id_of_channel_emty = int(channel_of_channel_emty.get_id_channel())
                            
                            channel_to_send = self.bot.get_channel(channel_id_of_channel_emty)
                            if channel_to_send is None:
                                return
                            if channel_to_send and channel_id_of_channel_feed == channel_id_of_channel_emty:
                                try:
                                    print(f"Sending message to {channel_to_send}")
                                    # NOTE: Lỗi chưa tự gửi đươc embed
                                    # ERROR id server không phải là channel_id
                                    server_id = str(channel_to_send.guild.id) # type: ignore
                                    link_atom = feed_of_feed_emty.get_link_atom_feed()
                                    feed_embed = FeedEmbed(server_id, link_atom, link_emty)
                                    await channel_to_send.send(embed=feed_embed.get_embed()) # type: ignore
                                    # await channel_to_send.send(f"{link_emty}") #type: ignore
                                except TypeError as e:
                                    print(f"Error loading list feed: {e}")

            
    @tasks.loop(seconds=10)
    async def push_noti(self):
        print('run background task')
        await self.load_list_feed()
        await self.load_guilds()
        
    @push_noti.before_loop
    async def await_bot_ready(self):
        # đợi cho bot đăng nhập xong
        print('waiting...')
        await self.bot.wait_until_ready()
        print('start')
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} is ready")
        print("Current commands:", [command.name for command in self.bot.commands])
        print("Current slash commands:", [command.name for command in self.bot.get_application_commands()])
        
        await self.bot.sync_all_application_commands()
        print(f'Bot {self.bot.user} is ready and commands are synced.')

        if not self.push_noti.is_running():
            self.push_noti.start()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            available_commands = [command.name for command in self.bot.commands]
            available_slash_commands = [command.name for command in self.bot.get_application_commands()]
            
            command_list_1 = ", ".join(available_commands)
            command_list_2 = ", ".join(available_slash_commands) # type: ignore
            
            server_color_bll = ServerColorBLL()
            server_dto = ServerDTO(str(ctx.guild.id), ctx.guild.name)
            server_color_dto = server_color_bll.get_server_color_by_id_server(server_dto.get_id_server())
            hex_color = server_color_dto.get_color().get_hex_color() # type: ignore
            
            embed = CustomEmbed(
                id_server=str(ctx.guild.id),
                title=f"Lệnh **{ctx.invoked_with}** không hợp lệ",
                description=f'''
Lệnh tiền tố: `{ctx.prefix}`
- Các lệnh command hiện có: {command_list_1}
- Các lệnh slash command hiện có: {command_list_2}
                ''',
                color = int(hex_color, 16) if hex_color else nextcord.Color(0x808080)
            )
            await ctx.send(embed=embed)
        else:
            raise error

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        available_commands = [command.name for command in self.bot.commands]
        available_slash_commands = [command.name for command in self.bot.get_application_commands()]
        command_list_1 = ", ".join(available_commands)
        command_list_2 = ", ".join(available_slash_commands) # type: ignore
        
        server_color_bll = ServerColorBLL()
        server_dto = ServerDTO(str(guild.id), guild.name)
        server_color_dto = server_color_bll.get_server_color_by_id_server(server_dto.get_id_server())
        hex_color = server_color_dto.get_color().get_hex_color() # type: ignore
            
        if guild.system_channel:
            embed = CustomEmbed(
                id_server=str(guild.id),
                title=f"**{self.bot.user}** joined {guild.name} successfully!",
                description=f'''
Aloha! Tôi là **{self.bot.user}**, bot giúp bạn nhận thông báo bài đăng mới từ Facebook và các ứng dụng khác một cách miễn phí. Thay vì trả phí cho những bot khác, hãy sử dụng tôi. Đóng góp ý kiến hay cần hỗ trợ ư, tham gia server **[Greencode](https://discord.com/invite/Q7NXBFpZeM)** nhé. Hàng chùa bất diệt!
Lệnh tiền tố: `{self.bot.command_prefix}`
- Các lệnh command hiện có: {command_list_1}
- Các lệnh slash command hiện có: {command_list_2}
                ''',
                color = int(hex_color, 16) if hex_color else nextcord.Color(0x808080)
            )
            embed.set_thumbnail(url="https://cdn-longterm.mee6.xyz/plugins/welcome/images/911798642518663208/d7a41040adf3036620000c397fbfa21a487c9e5bb1db698fd3081ed541f4b5c1.gif")
            await guild.system_channel.send(embed=embed)

async def setup(bot: commands.Bot):
    # NOTE: add_cog là một funstion bình thường không phải là async funstion
    bot.add_cog(Events(bot))