from test import testChannelEmty, testChannelFeed, testFeedEmty, testServerChannel
from bot.GUI.Embed import Embed
from bot.utils.ReadRSS import ReadRSS
from bot.utils.Database import Database
import nextcord
from nextcord.ext import commands
import os
import tracemalloc
import logging
import asyncio


def aboutUs():
    print('''
This is a Discord bot built with Python, ReadRSS bot brings RSS feeds 
to your Discord server. Receive notifications from news sources 
including Facebook and much more. 

                        -- ABOUT US --
                         
         ██████╗  ██████╗██████╗ ███████╗██╗   ██╗     #GCdev24
        ██╔════╝ ██╔════╝██╔══██╗██╔════╝██║   ██║     HaoWasabi
        ██║  ███╗██║     ██║  ██║█████╗  ██║   ██║     NaelTuhline
        ██║   ██║██║     ██║  ██║██╔══╝  ╚██╗ ██╔╝     tivibin789
        ╚██████╔╝╚██████╗██████╔╝███████╗ ╚████╔╝   
        ╚═════╝  ╚═════╝╚═════╝ ╚══════╝  ╚═══╝       
                                                                  
''')
    
tracemalloc.start()

intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nextcord')

bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
async def load_cogs():
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'bot/cogs')):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'bot.cogs.{filename[:-3]}')
            except Exception as e:
                print(f'Failed to load extension {filename}: {e}')
            
@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready")
    print("Các lệnh hiện có:", [command.name for command in bot.commands])

    # Đồng bộ lệnh slash
    await bot.sync_application_commands()
    print("Đã đồng bộ các lệnh slash")

def run():    
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("TOKEN không được tìm thấy trong file .env.")
    
if __name__ == "__main__":
    # __RSS_TESTING__
    # ReadRSS("https://fetchrss.com/rss/66692c903413f4ff7e03b4e2666fdd5607b27c15980a5e02.xml")
    
    # __BLL_TESTING__
    # testChannelEmty()
    # testServerChannel()
    # testFeedEmty()
    # testChannelFeed()
    
    # __EMBED_TESTING__
    # testFeedEmty()
    # embed = Embed("https://www.facebook.com/TuoitrekhoaCongngheThongtinSGU", "https://www.facebook.com/814717200441834/posts/957235702856649",  "RED")
    # print(embed)
    
    # __BOT_RUNNING__
    aboutUs()
    Database().clear()
    asyncio.run(load_cogs())
    run()