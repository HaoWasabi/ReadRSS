import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from bot.utils.ReadRSS import ReadRSS
from bot.utils.Database import Database
import os
import tracemalloc
import logging

tracemalloc.start()

intents = nextcord.Intents.default()
intents.message_content = True
intents.guilds = True

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nextcord')

bot = commands.Bot(command_prefix='!', intents=intents)

# __BOT_EVENT__

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready")
    print("Các lệnh hiện có:", [command.name for command in bot.commands])

    # Đồng bộ lệnh slash
    await bot.sync_application_commands()
    print("Đã đồng bộ các lệnh slash")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        available_commands = [command.name for command in bot.commands]
        command_list = ", ".join(available_commands)
        await ctx.send(f"Lệnh không tồn tại. Các lệnh hiện có: {command_list}")
    else:
        raise error

# __BOT_COMMAND__

# Lệnh thông thường
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def read_rss(ctx, url):
    ReadRSS(url)
    await ctx.send("Read RSS successfully.")

@bot.command()
async def clear_db(ctx):
    Database().clear()
    await ctx.send("Cleared database successfully.")

@bot.command()
async def servers(ctx):
    guilds = bot.guilds
    guild_names = [guild.name for guild in guilds]
    await ctx.send(f'The bot is in the following servers: {", ".join(guild_names)}')

# Lệnh Slash
@bot.slash_command(name="ping", description="Replies with Pong!")
async def _ping(interaction: Interaction):
    await interaction.response.send_message(f'Pong! {round(bot.latency * 1000)}ms')

@bot.slash_command(name="read_rss", description="Reads RSS from the given URL")
async def _read_rss(interaction: Interaction, url: str):
    ReadRSS(url)
    await interaction.response.send_message("Read RSS successfully.")

@bot.slash_command(name="clear_db", description="Clears the database")
async def _clear_db(interaction: Interaction):
    Database().clear()
    await interaction.response.send_message("Cleared database successfully.")

@bot.slash_command(name="servers", description="Shows the servers the bot is in")
async def _servers(interaction: Interaction):
    guilds = bot.guilds
    guild_names = [guild.name for guild in guilds]
    await interaction.response.send_message(f'The bot is in the following servers: {", ".join(guild_names)}')

