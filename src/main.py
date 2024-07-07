from test import testChannelEmty, testChannelFeed, testFeedEmty, testServerChannel
from test import testReadRSS, testEmbeb
from bot.utils.Database import Database
import nextcord
from nextcord.ext import commands
import tracemalloc
import logging
import asyncio
import os


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

bot = commands.Bot(command_prefix='_', intents=intents)

# Load cogs
async def load_cogs():
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'bot/cogs')):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'bot.cogs.{filename[:-3]}')
            except Exception as e:
                print(f'Failed to load extension {filename}: {e}')
                
def run():    
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("TOKEN không được tìm thấy trong file .env.")
    
if __name__ == "__main__":
    
    # __BOT_RUNNING__
    # aboutUs()
    Database().clear()
    asyncio.run(load_cogs())
    run()
    
    # __RSS_TESTING__
    # testReadRSS()
    
    # __BLL_TESTING__
    # testChannelEmty()
    # testServerChannel()
    # testFeedEmty()
    # testChannelFeed()
    
    # __EMBED_TESTING__
    # testEmbeb()