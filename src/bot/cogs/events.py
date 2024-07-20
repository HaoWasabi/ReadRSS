import time
import threading
import asyncio
import nextcord
from nextcord.ext import commands
from bot.DTO.ChannelEmtyDTO import ChannelEmtyDTO
from bot.BLL.ChannelFeedBLL import ChannelFeedBLL
from bot.BLL.ChannelEmtyBLL import ChannelEmtyBLL
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL
from bot.GUI.FeedEmbed import FeedEmbed
from bot.utils.ReadRSS import ReadRSS

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def send_message(self):
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

    def push_noti(self):
        channelFeedBLL = ChannelFeedBLL()
        channelEmtyBLL = ChannelEmtyBLL()
        feedEmtyBLL = FeedEmtyBLL()

        list_channel_feed = channelFeedBLL.getAllChannelFeed()
        list_feed_emty = feedEmtyBLL.getAllFeedEmty()
        
        
        for channel_feed in list_channel_feed:
            ReadRSS(channel_feed.getFeed().getLinkAtom_feed())
            channel_of_channel_feed = channel_feed.getChannel()
            channel_id_of_channel_feed = int(channel_of_channel_feed.getId_channel())
            print(channel_of_channel_feed)
            
            for feed_emty in list_feed_emty:
                feed_of_feed_emty = feed_emty.getFeed()
                emty_of_feed_emty = feed_emty.getEmty()
                channel_emty = ChannelEmtyDTO(channel_of_channel_feed, emty_of_feed_emty)
                
                linkAtom_feed = feed_of_feed_emty.getLinkAtom_feed()
                link_emty = emty_of_feed_emty.getLink_emty()
                
                if channelEmtyBLL.insertChannelEmty(channel_emty):
                    channel_of_channel_emty = channel_emty.getChannel()
                    channel_id_of_channel_emty = int(channel_of_channel_emty.getId_channel())
                    
                    channel_to_send = self.bot.get_channel(channel_id_of_channel_emty)
                    if channel_to_send and channel_id_of_channel_feed == channel_id_of_channel_emty:
                        embed = FeedEmbed(linkAtom_feed, link_emty, "RED").get_embed()
                        asyncio.run_coroutine_threadsafe(channel_to_send.send(embed=embed), self.bot.loop)
                        # asyncio.run_coroutine_threadsafe(channel_to_send.send(f"{link_emty}"), self.bot.loop)

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
