import os, sys, logging, tracemalloc, asyncio, nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from bot.utils.Database import Database
# from test import test_server_color

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

# Start memory tracking
tracemalloc.start()

# Set up intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True

# Set up logging
logging.basicConfig(level=logging.INFO, format="p%(process)s %(pathname)s:%(lineno)d %(levelname)s - %(message)s")
logger = logging.getLogger('nextcord')

# Set up bot instance
bot = commands.Bot(command_prefix='_', intents=intents)

# Load cogs asynchronously
async def load_cogs():
    cogs_dir = os.path.join(os.path.dirname(__file__), 'bot/cogs')
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            cog_name = f'bot.cogs.{filename[:-3]}'
            try:
                bot.load_extension(cog_name)
                logger.info(f'Successfully loaded extension {cog_name}')
            except Exception as e:
                logger.error(f'Failed to load extension {cog_name}: {e}')

def run_bot():
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
    else:
        logger.error("DISCORD_TOKEN not found in .env file.")

if __name__ == "__main__":
    # Display about info
    about_us()
    
    # Run bot and load cogs
    asyncio.run(load_cogs())
    run_bot()

    # __CLEAR_DATABASE__
    # Database().delete_table('tbl_channel_emty')
    # Database().delete_table('tbl_channel')
    # Database().delete_table('tbl_server_channel')
    # Database().clear()
    # Database().drop_table('tbl_channel_feed')
    # Database().drop_table('tbl_feed')
    # Database().drop_table('tbl_server_color')

    # __TEST_READRSS__
    # test_read_rss()
    
    # __TEST_BLL__
    # test_server_channel()
    # test_feed_emty()
    # test_channel_feed()
    # test_channel_emty()
    # test_server_color()
    
    # __TEST_EMBED__
    # test_feed_embeb()
