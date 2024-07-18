import os
import logging
import tracemalloc
import asyncio
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def about_us():
    print('''
This is a Discord bot built with Python. ReadRSS bot brings RSS feeds 
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

@bot.event
async def on_ready():
    await bot.sync_all_application_commands()
    print(f'Bot {bot.user} is ready and commands are synced.')

def run():    
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("TOKEN không được tìm thấy trong file .env.")

if __name__ == "__main__":
    about_us()
    asyncio.run(load_cogs())
    run()

    # __CLEAR_DATABASE__
    # Database().clear()
    
    # __TEST_READRSS__
    # testReadRSS()
    
    # __TEST_BLL__
    # testServerChannel()
    # testFeedEmty()
    # testChannelFeed()
    
    # __TEST_EMBED__
    # testChannelEmty()
    # testFeedEmbeb()