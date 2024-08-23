from nextcord.ext import commands
from bot.utils.database import Database
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
    
    @commands.command(name="superclear")
    @commands.is_owner()
    async def superclear(self, ctx):
        Database().clear()
        await ctx.send("Cleared all data in the database successfully.")

    @commands.command(name="servers")
    @commands.is_owner()
    async def servers(self, ctx):
        guilds = self.bot.guilds
        num = 0
        for guild in guilds:
            guild_names += [guild.name]
            num += 1
        await ctx.send(f'The bot joined **{num}** guilds: **{", ".join(guild_names)}**')
      
async def setup(bot):
    bot.add_cog(AdminCommands(bot))
