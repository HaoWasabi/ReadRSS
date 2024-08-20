import time
import threading
import asyncio
import nextcord
from nextcord.ext import commands
from bot.dto.channel_dto import ChannelDTO
from bot.dto.server_dto import ServerDTO
from bot.dto.channel_emty_dto import ChannelEmtyDTO
from bot.dto.server_channel_dto import ServerChannelDTO
from bot.bll.server_bll import ServerBLL
from bot.bll.channel_bll import ChannelBLL
from bot.bll.feed_emty_bll import FeedEmtyBLL
from bot.bll.channel_feed_bll import ChannelFeedBLL
from bot.bll.channel_emty_bll import ChannelEmtyBLL
from bot.bll.server_channel_bll import ServerChannelBLL
from bot.gui.feed_embeb import FeedEmbed
from bot.utils.read_rss import ReadRSS

class Events(commands.Cog):
    def __init__(self, bot):
        self.__bot = bot
        self.__server_bll = ServerBLL()
        self.__channel_bll = ChannelBLL()
        self.__feed_emty_bll = FeedEmtyBLL()
        self.__channel_feed_bll = ChannelFeedBLL()
        self.__channel_emty_bll = ChannelEmtyBLL()
        self.__server_channel_bll = ServerChannelBLL()
        
    def load_guilds(self):
        guilds = self.__bot.guilds
        
        for guild in guilds:
            serverDTO = ServerDTO(str(guild.id), str(guild.name))
            if self.__server_bll.get_server_by_id_server(serverDTO.get_id_server()) == None:
                self.__server_bll.insert_server(serverDTO)
                print("server_id: ", guild.id)
                
            for channel in guild.channels:
                print(channel.name + " " + str(channel.id) + "\n")
                channelDTO = ChannelDTO(str(channel.id), str(channel.name))
                if self.__channel_bll.get_channel_by_id_channel(channelDTO.get_id_channel()) != None:
                    if channel.is_nsfw():                            
                        channel_of_db = self.__channel_bll.get_channel_by_id_channel(channelDTO.get_id_channel())
                        print("channel_id:", channel.id)
                        serverChannelDTO = ServerChannelDTO(serverDTO, channel_of_db)
                        self.__server_channel_bll.insert_server_channel(serverChannelDTO)        

    # def load_guilds(self):
    #     guilds = self.__bot.guilds
        
    #     print(f"Bot đã kết nối với {len(guilds)} máy chủ")  # In ra số lượng guild mà bot đã kết nối

    #     for guild in guilds:
    #         print(f"Đang xử lý máy chủ: {guild.name} (ID: {guild.id})")  # In ra tên và ID của máy chủ

    #         # Kiểm tra nếu server đã tồn tại trong cơ sở dữ liệu
    #         if not self.__server_bll.get_server_by_id_server(guild.id):
    #             serverDTO = ServerDTO(str(guild.id), str(guild.name))
    #             self.__server_bll.insert_server(serverDTO)
    #         else:
    #             print(f"Server với ID {guild.id} đã tồn tại trong cơ sở dữ liệu.")

    #         # Kiểm tra và in ra các kênh trong guild
    #         if not guild.channels:
    #             print(f"Máy chủ {guild.name} không có kênh nào.")  # In ra nếu không có kênh
    #         else:
    #             for channel in guild.channels:
    #                 print(f"Kênh ID: {channel.id}, Tên kênh: {channel.name}, Loại kênh: {channel.type}")
    #                 # Bạn có thể xử lý thêm logic cho các kênh ở đây

    #         print()  # In ra một dòng trống để phân biệt giữa các máy chủ
        
    def load_list_feed(self):
        list_channel_feed = self.__channel_feed_bll.get_all_channel_feed()
        list_feed_emty = self.__feed_emty_bll.get_all_feed_emty()
        
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
                    # link_atom_feed = feed_of_feed_emty.get_link_atom_feed()
                    
                    if self.__channel_emty_bll.insert_channel_emty(channel_emty):
                        channel_of_channel_emty = channel_emty.get_channel()
                        channel_id_of_channel_emty = int(channel_of_channel_emty.get_id_channel())
                        
                        channel_to_send = self.__bot.get_channel(channel_id_of_channel_emty)
                        if channel_to_send and channel_id_of_channel_feed == channel_id_of_channel_emty:
                            # embed = FeedEmbed(link_atom_feed, link_emty).get_embed()
                            # asyncio.run_coroutine_threadsafe(channel_to_send.send(embed=embed), self.__bot.loop)
                            asyncio.run_coroutine_threadsafe(channel_to_send.send(f"{link_emty}"), self.__bot.loop)
        
    async def push_noti(self):
        self.load_guilds()
        # self.load_list_feed()
        
    def send_message(self): #test
        channel_id = 1123394796329898004
        channel = self.__bot.get_channel(channel_id)
        if channel:
            asyncio.run_coroutine_threadsafe(channel.send('Bot has started!'), self.__bot.loop)

    def periodic_message(self):
        while True:
            # asyncio.run_coroutine_threadsafe(self.send_message(), self.__bot.loop)
            asyncio.run_coroutine_threadsafe(self.push_noti(), self.__bot.loop)
            time.sleep(10)

    def start_periodic_messages(self):
        thread = threading.Thread(target=self.periodic_message)
        thread.daemon = True
        thread.start()
                            
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.__bot.user} is ready")
        print("Các lệnh command hiện có:", [command.name for command in self.__bot.commands])
        print("Các lệnh slash command hiện có:", [command.name for command in self.__bot.get_application_commands()])
        self.start_periodic_messages()
        
        await self.__bot.sync_all_application_commands()
        print(f'Bot {self.__bot.user} is ready and commands are synced.')
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            available_commands = [command.name for command in self.__bot.commands]
            available_slash_commands = [command.name for command in self.__bot.get_application_commands()]
            
            command_list_1 = ", ".join(available_commands)
            command_list_2 = ", ".join(available_slash_commands)
            
            await ctx.send(f'''
Lệnh **{ctx.invoked_with}** không hợp lệ
- Các lệnh command hiện có: {command_list_1}
- Các lệnh slash command hiện có: {command_list_2}
            ''')
        
        else:
            raise error

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        available_commands = [command.name for command in self.__bot.commands]
        available_slash_commands = [command.name for command in self.__bot.get_application_commands()]
        command_list_1 = ", ".join(available_commands)
        command_list_2 = ", ".join(available_slash_commands)
        
        if guild.system_channel:
            await guild.system_channel.send(f'''
**{self.__bot.user}** joined {guild.name} successfully!
- Các lệnh command hiện có: {command_list_1}
- Các lệnh slash command hiện có: {command_list_2}
        ''')

async def setup(bot):
    await bot.add_cog(Events(bot))
