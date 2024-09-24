from operator import le
import nextcord, os, logging

from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.message import Message
import google.generativeai as genai
from ..DTO.channel_dto import ChannelDTO
from ..DTO.server_dto import ServerDTO
from ..DTO.color_dto import ColorDTO

from ..BLL.channel_bll import ChannelBLL
from ..BLL.server_bll import ServerBLL
from ..BLL.feed_bll import FeedBLL
from ..BLL.emty_bll import EmtyBLL

from ..GUI.embed_feed import EmbedFeed
from ..GUI.embed_custom import EmbedCustom
from ..utils.commands_cog import CommandsCog
from ..utils.handle_rss import read_rss_link

logger = logging.getLogger("Events")

class Events(CommandsCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    async def load_guilds(self):
        try:
            guilds = self.bot.guilds
            channel_bll = ChannelBLL()
            server_bll = ServerBLL()
            list_channel = channel_bll.get_all_channel()
            list_server = server_bll.get_all_server()

            # default_color = ColorDTO("blue").get_hex_color()
            # channel_dto = ChannelDTO("DM", "DM", "DM")
            # channel_bll.insert_channel(channel_dto)
            
            # server_dto = ServerDTO(
            #     server_id="DM", 
            #     server_name="DM", 
            #     hex_color=default_color)
            # server_bll.insert_server(server_dto)
    
            for guild in guilds:
                id_server = str(guild.id)
                name_server = str(guild.name)
                server_dto = ServerDTO(id_server, name_server)
                
                if server_dto not in list_server:
                    server_bll.insert_server(server_dto)
                else:
                    matching_server = next((s for s in list_server if s.get_server_id() == server_dto.get_server_id()), None)
                    if matching_server and matching_server.get_server_name() != server_dto.get_server_name():
                        server_bll.update_server(server_dto)
                    
                for channel in guild.channels:
                    id_channel = str(channel.id)
                    name_channel = channel.name
                    channel_dto = ChannelDTO(id_channel, name_channel, id_server)
                    
                    matching_channel = next((ch for ch in list_channel if ch.get_channel_id() == channel_dto.get_channel_id()), None)
                    if matching_channel and matching_channel.get_channel_name() != channel_dto.get_channel_name():
                        channel_bll.update_channel(channel_dto)

        except Exception as e:
            logger.error(f"Error loading guilds: {e}")
                
    async def load_list_feed(self):
        try:
            # Khởi tạo các BLL (Business Logic Layer)
            channel_bll = ChannelBLL()
            emty_bll = EmtyBLL()
            feed_bll = FeedBLL()

            # Lấy tất cả các channel và feed từ cơ sở dữ liệu
            list_channel = channel_bll.get_all_channel()
            list_emty = emty_bll.get_all_emty()
            list_feed = feed_bll.get_all_feed()

            # Duyệt qua từng channel
            for channel in list_channel:
                channel_id = channel.get_channel_id()
                channel_send_id = int(channel_id)
                channel_send = self.bot.get_channel(channel_send_id)

                # Nếu không tìm thấy kênh (có thể là DMChannel)
                if not channel_send:
                    # Lấy user từ ID cho DMChannel
                    channel_send = await self.bot.fetch_user(channel_send_id)

                # Duyệt qua từng feed
                for feed in list_feed:
                    # Đọc RSS từ link của feed
                    feed_data = read_rss_link(rss_link=feed.get_link_atom_feed())
                    if not feed_data or not all(feed_data):
                        raise TypeError("Feed data is incomplete or None")
                    
                    # Kiểm tra xem feed có thuộc về kênh hiện tại không
                    if feed.get_channel_id() == channel_id:
                        feed_dto, emty_dto = feed_data
                        emty_dto.set_channel_id(channel_id)

                        if emty_dto not in list_emty:
                            # Lưu emty vào cơ sở dữ liệu
                            emty_bll.insert_emty(emty_dto)

                            # Tạo Embed và gửi tin nhắn đến kênh
                            if isinstance(channel_send, nextcord.User):  # Nếu là DMChannel
                                id_server = str(channel_send.id)
                            else:  # Nếu là channel trong server
                                id_server = str(channel_send.guild.id)

                            embed = EmbedFeed(
                                id_server=id_server if id_server else "DM",
                                feed_dto=feed_dto, 
                                emty_dto=emty_dto
                            )

                            await channel_send.send(embed=embed)  # Gửi tin nhắn đến kênh
                            logger.info(f"Sending message to {'DM' if isinstance(channel_send, nextcord.User) else 'channel'} {channel_send_id} with embed {embed}")
                            logger.info(f"Inserting emty: {emty_dto.__dict__}")

        except Exception as e:
            logger.error(f"Lỗi khi load list feed: {e}")

 
    @tasks.loop(seconds=10)
    async def push_noti(self):
        logger.debug('run background task')
        await self.load_list_feed()
        await self.load_guilds()

    @push_noti.before_loop
    async def await_bot_ready(self):
        # đợi cho bot đăng nhập xong
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Bot {self.bot.user} is ready")
        logger.info("Current commands: %s", str([command.name for command in self.bot.commands]))
        logger.info("Current slash commands: %s", str([command.name for command in self.bot.get_application_commands()]))
        
        await self.bot.sync_all_application_commands()
        logger.info(f'Bot {self.bot.user} is ready and commands are synced.')

        logger.info('check notify start')
        if not self.push_noti.is_running():
            self.push_noti.start()
            
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return

        if self.bot.user is None:
            await message.channel.send('wtf')
            return
        
    
        if message.content.startswith(f'<@{self.bot.user.id.__str__()}>'):

            prompt = message.content[len(f'<@{self.bot.user.id.__str__()}> '):]
            print(prompt)

            try:  
                history = []
                
                async for message1 in message.channel.history(limit=20):
                    if message1.author.id != self.bot.user.id:
                        prompt1 = message1.content
                        
                        if (prompt1.startswith(f'<@{self.bot.user.id.__str__()}> ')):
                            prompt1 = prompt1[len(f'<@{self.bot.user.id.__str__()}> '):]
                        
                        if len(prompt1) == 0: continue
                            
                        history.append({"role": "user", "parts": f'{message1.author.name}: "{prompt1}"'})
                    else:
                        history.append({"role": "model", "parts": message1.content})

                # Gửi tin nhắn "Creating prompt..."
                prompt_message = await message.channel.send('Creating prompt...')
                

                # Cấu hình client Generative AI
                genai.configure(api_key=os.getenv("GEMINI_TOKEN"))

                # Sử dụng mô hình Generative AI để tạo nội dung
                model = genai.GenerativeModel("gemini-1.5-flash")
                chat = model.start_chat(history=history[::-1])
                response = chat.send_message(f'{message.author.name}: "{prompt}"')
                response_text = response.text
                print(response_text)
                
                # Chia nhỏ nội dung phản hồi thành các phần nhỏ tối đa 2000 ký tự
                chunk_size = 2000
                chunks = [response_text[i:i + chunk_size] for i in range(0, len(response_text), chunk_size)]
                response_message = await message.reply(chunks[0])

                # Gửi các đoạn tin nhắn tiếp theo
                for chunk in chunks[1:]:
                    response_message = await response_message.reply(chunk)
                    
                # Xóa tin nhắn "Creating prompt..." sau khi gửi phản hồi
                await prompt_message.delete()
            except Exception as e:
                await message.channel.send(f'Error: {e}')
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            available_commands = [command.name for command in self.bot.commands]
            available_slash_commands = [command.name for command in self.bot.get_application_commands()]
            
            command_list_1 = ", ".join(available_commands)
            command_list_2 = ", ".join(available_slash_commands) # type: ignore
            
            id_server = str(ctx.guild.id) if ctx.guild else "DM"
            embed = EmbedCustom(
                id_server=id_server,
                title=f"Command **{ctx.invoked_with}** is invalid",
                description=f'''
command prefix: `{ctx.prefix}`
- The current commands have: {command_list_1}
- The current slash commands have: {command_list_2}
                ''',
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
        
        id_server = str(guild.id)
        if guild.system_channel:
            embed = EmbedCustom(
                id_server=id_server,
                title=f"**Aloha {guild.name}!**",
                description=f'''
I am ** {self.bot.user} **, bot helps you receive a new post from Facebook and other applications for free. Instead of paying other bots, use me. Contribute ideas or need support, participate in ** [GreenCode](https://discord.com/invite/Q7NXBFpZeM)** server!

command prefix: `{self.bot.command_prefix}`
- The current commands have: {command_list_1}
- The current slash commands have: {command_list_2}
                ''',
                color = nextcord.Color(0x3498DB)
            )
            embed.set_thumbnail(url="https://cdn-longterm.mee6.xyz/plugins/welcome/images/911798642518663208/d7a41040adf3036620000c397fbfa21a487c9e5bb1db698fd3081ed541f4b5c1.gif")
            await guild.system_channel.send(embed=embed)

async def setup(bot: commands.Bot):
    # NOTE: add_cog là một funstion bình thường không phải là async funstion
    bot.add_cog(Events(bot))