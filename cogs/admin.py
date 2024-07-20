from nextcord.ext import commands
from bot.utils.Database import Database
import nextcord

class AdminCommands(commands.Cog):
    def __init__(self, bot):
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
        Database().clear()
        await ctx.send("Cleared all data in the database successfully.")

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
