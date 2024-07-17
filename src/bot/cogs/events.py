import time
import threading
from nextcord.ext import commands
from nextcord import TextChannel
from bot.DTO.ChannelEmtyDTO import ChannelEmtyDTO
from bot.BLL.ChannelFeedBLL import ChannelFeedBLL
from bot.BLL.ChannelEmtyBLL import ChannelEmtyBLL
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL
from bot.GUI.FeedEmbed import FeedEmbed
from bot.utils.ReadRSS import ReadRSS

def loop_event_per15min():
    while True:
        push_noti()
        print('Thread', 15)
        time.sleep(10) 
threading.Thread(target=loop_event_per15min).start()

def push_noti():
    # Tạo các đối tượng BLL (Business Logic Layer)
    channelFeedBLL = ChannelFeedBLL()
    channelEmtyBLL = ChannelEmtyBLL()
    feedEmtyBLL = FeedEmtyBLL()
    
    # Lấy tất cả danh sách channel feeds, channel emty và feed emty
    list_channel_feed = channelFeedBLL.getAllChannelFeed()
    list_channel_emty = channelEmtyBLL.getAllChannelEmty()
    list_feed_emty = feedEmtyBLL.getAllFeedEmty()
    
    # Trích xuất danh sách các đối tượng 'Emty' từ danh sách feed emty
    list_emty_of_list_feed_emty = [feed_emty.getEmty() for feed_emty in list_feed_emty]
    
    # Duyệt qua từng channel feed
    for channel_feed in list_channel_feed:
        # Đọc RSS feed từ link
        ReadRSS(channel_feed.getFeed().getLinkAtom_feed())
        
        # Lấy channel liên quan của channel feed hiện tại
        channel_of_channel_feed = channel_feed.getChannel()
        print(channel_of_channel_feed)
        
        # Duyệt qua từng feed emty
        for feed_emty in list_feed_emty:
            emty_of_feed_emty = feed_emty.getEmty()
            
            # Tạo đối tượng ChannelEmtyDTO
            channel_emty = ChannelEmtyDTO(channel_of_channel_feed, emty_of_feed_emty)
            
            # emty_of_channel_emty = channel_emty.getEmty()
            
            # Chèn vào ChannelEmty nếu danh sách trống hoặc nếu 'Emty' chưa có trong danh sách feed emty
            # if not list_channel_emty or emty_of_channel_emty not in list_emty_of_list_feed_emty:
            print(channelEmtyBLL.insertChannelEmty(channel_emty))

                

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} is ready")
        print("Các lệnh command hiện có:", [command.name for command in self.bot.commands])
        print("Các lệnh slash command hiện có:", [command.name for command in self.bot.get_application_commands()])
        
        # Đồng bộ lệnh slash
        await self.bot.sync_application_commands()
        print("Đã đồng bộ các lệnh slash")
    
    

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
        await guild.system_channel.send(f'''
**{self.bot.user}** joined {guild.name} successfully!
- Các lệnh command hiện có: {command_list_1}
- Các lệnh slash command hiện có: {command_list_2}
            ''')

async def setup(bot):
    await bot.add_cog(Events(bot))


