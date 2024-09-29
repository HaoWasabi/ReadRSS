import os, sys, logging, tracemalloc, asyncio, nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from bot.DAL.channel_dal import ChannelDAL
from bot.DAL.emty_dal import EmtyDAL
from bot.DAL.feed_dal import FeedDAL
from bot.DAL.qr_pay_code_dal import QrPayCodeDAL
from bot.DAL.transaction_history_dal import TransactionHistoryDAL
from bot.DAL.premium_dal import PremiumDAL
from bot.DAL.server_dal import ServerDAL
from bot.DAL.user_dal import UserDAL
from bot.DAL.user_premium_dal import UserPremiumDAL
from bot.utils.Database import dataBase


# Load environment variables
load_dotenv()
# Start memory tracking
tracemalloc.start()

# Set up intents
intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True

# Set up logging
logging.basicConfig(level=logging.NOTSET, format="%(filename)s:%(lineno)d [%(levelname)-s] %(message)s")
logger = logging.getLogger(__name__)

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

def create_database_tables():
    ChannelDAL().create_table()
    EmtyDAL().create_table()
    FeedDAL().create_table()
    QrPayCodeDAL().create_table()
    TransactionHistoryDAL().create_table()
    PremiumDAL().create_table()
    ServerDAL().create_table()
    UserDAL().create_table()
    UserPremiumDAL().create_table()
    
if __name__ == "__main__":
    ## Create database tables
    create_database_tables()
    
    # ## Run bot and load cogs
    asyncio.run(load_cogs())
    run_bot()
    
    # dataBase.delete_table("tbl_user_premium")