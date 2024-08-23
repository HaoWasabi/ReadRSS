from nextcord.ext import commands
from ..utils.Database import dataBase
from nextcord import Guild
from nextcord.ext.commands import Bot

class AdminCommands(commands.Cog):
    
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        try: 
            await ctx.send("Bot is shutting down...")
            await self.bot.close()
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")
    
    @commands.command(name="super_clear")
    @commands.is_owner()
    async def super_clear(self, ctx):
        dataBase.clear()
        await ctx.send("Cleared all data in the database successfully.")

    @commands.command(name="servers")
    @commands.is_owner()
    async def servers(self, ctx):
        guilds = self.bot.guilds
        num = 0
        guild_names = []
        for guild in guilds:
            guild_names.append(guild.name)
            num += 1
        await ctx.send(f'The bot joined **{num}** guilds: **{", ".join(guild_names)}**')
      
async def setup(bot):
    bot.add_cog(AdminCommands(bot))
