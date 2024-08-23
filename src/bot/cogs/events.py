import time
import threading
import asyncio
import nextcord
from nextcord.ext import commands, tasks
from ..DTO.server_channel_dto import ServerChannelDTO
from ..DTO.channel_emty_dto import ChannelEmtyDTO
from ..DTO.channel_dto import ChannelDTO
from ..DTO.server_dto import ServerDTO
from ..BLL.server_channel_bll import ServerChannelBLL
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..BLL.channel_emty_bll import ChannelEmtyBLL
from ..BLL.feed_emty_bll import FeedEmtyBLL
from ..BLL.channel_bll import ChannelBLL
from ..BLL.server_bll import ServerBLL
from ..GUI.feed_embed import FeedEmbed
from ..utils.read_rss import ReadRSS

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def load_guilds(self):
        server_bll = ServerBLL() 
        channel_bll = ChannelBLL()
        server_channel_bll = ServerChannelBLL()
        guilds = self.bot.guilds
        
        for guild in guilds:
            server_dto = ServerDTO(str(guild.id), str(guild.name))
            server_bll.insert_server(server_dto)
            
            for channel in guild.channels:
                channel_dto = ChannelDTO(str(channel.id), str(channel.name))
                
                for channel_of_db in channel_bll.get_all_channel():
                    if channel_dto.get_id_channel() == channel_of_db.get_id_channel():
                        server_channel_dto = ServerChannelDTO(server_dto, channel_dto)
                        server_channel_bll.insert_server_channel(server_channel_dto)

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
                        if channel_to_send and channel_id_of_channel_feed == channel_id_of_channel_emty:
                            await channel_to_send.send(f"{link_emty}")

    # NOTE: background main task
    # push notify where have change every 10 second
    @tasks.loop(seconds=10)
    async def push_noti(self):
        await self.load_list_feed()
        
    @push_noti.before_loop
    async def await_bot_ready(self):
        await self.bot.wait_until_ready()
        
    def send_message(self):  # Test
        channel_id = 1123394796329898004
        channel = self.bot.get_channel(channel_id)
        if channel:
            asyncio.run_coroutine_threadsafe(channel.send('Bot has started!'), self.bot.loop)
                            
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} is ready")
        print("Current commands:", [command.name for command in self.bot.commands])
        print("Current slash commands:", [command.name for command in self.bot.get_application_commands()])
        
        await self.bot.sync_all_application_commands()
        print(f'Bot {self.bot.user} is ready and commands are synced.')
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            available_commands = [command.name for command in self.bot.commands]
            available_slash_commands = [command.name for command in self.bot.get_application_commands()]
            
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
        available_commands = [command.name for command in self.bot.commands]
        available_slash_commands = [command.name for command in self.bot.get_application_commands()]
        command_list_1 = ", ".join(available_commands)
        command_list_2 = ", ".join(available_slash_commands)
        
        if guild.system_channel:
            await guild.system_channel.send(f'''
**{self.bot.user}** joined {guild.name} successfully!
- Các lệnh command hiện có: {command_list_1}
- Các lệnh slash command hiện có: {command_list_2}
        ''')

async def setup(bot):
    bot.add_cog(Events(bot))
