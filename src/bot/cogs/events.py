import time
import threading
import asyncio
import nextcord
from nextcord.ext import commands
from bot.dto.server_channel_dto import ServerChannelDTO
from bot.dto.channel_emty_dto import ChannelEmtyDTO
from bot.dto.channel_dto import ChannelDTO
from bot.dto.server_dto import ServerDTO
from bot.bll.server_channel_bll import ServerChannelBLL
from bot.bll.channel_feed_bll import ChannelFeedBLL
from bot.bll.channel_emty_bll import ChannelEmtyBLL
from bot.bll.feed_emty_bll import FeedEmtyBLL
from bot.bll.channel_bll import ChannelBLL
from bot.bll.server_bll import ServerBLL
from bot.gui.feed_embeb import FeedEmbed
from bot.utils.read_rss import ReadRSS

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def load_guilds(self):
        serverBLL = ServerBLL() 
        channelBLL = ChannelBLL()
        serverChannelBLL = ServerChannelBLL()
        guilds = self.bot.guilds
        
        for guild in guilds:
            serverDTO = ServerDTO(str(guild.id), str(guild.name))
            serverBLL.insert_server(serverDTO)
            
            for channel in guild.channels:
                channelDTO = ChannelDTO(str(channel.id), str(channel.name))
                
                for channel_of_db in channelBLL.get_all_channel():
                    if channelDTO.get_id_channel() == channel_of_db.get_id_channel():
                        serverChannelDTO = ServerChannelDTO(serverDTO, channelDTO)
                        serverChannelBLL.insert_server_channel(serverChannelDTO)        

    def load_list_feed(self):
        channelFeedBLL = ChannelFeedBLL()
        channelEmtyBLL = ChannelEmtyBLL()
        feedEmtyBLL = FeedEmtyBLL()

        list_channel_feed = channelFeedBLL.get_all_channel_feed()
        list_feed_emty = feedEmtyBLL.get_all_feed_emty()
        
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
                    # linkAtom_feed = feed_of_feed_emty.get_link_atom_feed()
                    
                    if channelEmtyBLL.insert_channel_emty(channel_emty):
                        channel_of_channel_emty = channel_emty.get_channel()
                        channel_id_of_channel_emty = int(channel_of_channel_emty.get_id_channel())
                        
                        channel_to_send = self.bot.get_channel(channel_id_of_channel_emty)
                        if channel_to_send and channel_id_of_channel_feed == channel_id_of_channel_emty:
                            # embed = FeedEmbed(linkAtom_feed, link_emty).get_embed()
                            # asyncio.run_coroutine_threadsafe(channel_to_send.send(embed=embed), self.bot.loop)
                            asyncio.run_coroutine_threadsafe(channel_to_send.send(f"{link_emty}"), self.bot.loop)
        
    def push_noti(self):
        # self.load_guilds()
        self.load_list_feed()
        
    def send_message(self): #test
        channel_id = 1123394796329898004
        channel = self.bot.get_channel(channel_id)
        if channel:
            asyncio.run_coroutine_threadsafe(channel.send('Bot has started!'), self.bot.loop)

    def periodic_message(self):
        while True:
            # self.send_message()
            self.push_noti()
            time.sleep(10)

    def start_periodic_messages(self):
        thread = threading.Thread(target=self.periodic_message)
        thread.daemon = True
        thread.start()
                            
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} is ready")
        print("Các lệnh command hiện có:", [command.name for command in self.bot.commands])
        print("Các lệnh slash command hiện có:", [command.name for command in self.bot.get_application_commands()])
        self.start_periodic_messages()
        
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
    await bot.add_cog(Events(bot))
