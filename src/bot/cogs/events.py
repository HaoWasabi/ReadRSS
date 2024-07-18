import time
import threading
from nextcord.ext import commands
from bot.DTO.ChannelEmtyDTO import ChannelEmtyDTO
from bot.BLL.ChannelFeedBLL import ChannelFeedBLL
from bot.BLL.ChannelEmtyBLL import ChannelEmtyBLL
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL
from bot.utils.ReadRSS import ReadRSS

def loop_event_per15min():
    while True:
        push_noti()
        print('Thread', 15)
        time.sleep(900)  # 15 minutes = 900 seconds

threading.Thread(target=loop_event_per15min, daemon=True).start()

def push_noti():
    channelFeedBLL = ChannelFeedBLL()
    channelEmtyBLL = ChannelEmtyBLL()
    feedEmtyBLL = FeedEmtyBLL()

    list_channel_feed = channelFeedBLL.getAllChannelFeed()
    list_channel_emty = channelEmtyBLL.getAllChannelEmty()
    list_feed_emty = feedEmtyBLL.getAllFeedEmty()
    
    list_emty_of_list_feed_emty = [feed_emty.getEmty() for feed_emty in list_feed_emty]
    
    for channel_feed in list_channel_feed:
        ReadRSS(channel_feed.getFeed().getLinkAtom_feed())
        channel_of_channel_feed = channel_feed.getChannel()
        print(channel_of_channel_feed)
        
        for feed_emty in list_feed_emty:
            emty_of_feed_emty = feed_emty.getEmty()
            channel_emty = ChannelEmtyDTO(channel_of_channel_feed, emty_of_feed_emty)
            
            if not list_channel_emty or emty_of_feed_emty not in list_emty_of_list_feed_emty:
                print(channelEmtyBLL.insertChannelEmty(channel_emty))

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} is ready")
        print("Các lệnh command hiện có:", [command.name for command in self.bot.commands])
        print("Các lệnh slash command hiện có:", [command.name for command in self.bot.get_application_commands()])

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
