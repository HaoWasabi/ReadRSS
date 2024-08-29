import nextcord
from nextcord.ext import commands
from ..utils.Database import dataBase
from nextcord.ext.commands import Bot

class AdminCommands(commands.Cog):
    
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        try: 
            embed = nextcord.Embed(
                title="Warning",
                description="The bot is shutting down...",
                color=0xFFA500
            )
            await ctx.send(embed=embed)
            await self.bot.close()
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")
    
    @commands.command(name="superclear")
    @commands.is_owner()
    async def superclear(self, ctx):
        dataBase.clear()
        embed = nextcord.Embed(
            title="Warning",
            description="Cleared all data in the database successfully.",
            color=0xFFA500
        )
        await ctx.send(embed=embed)

    @commands.command(name="clear")
    @commands.is_owner()
    async def clear(self, ctx, table_name: str):
        dataBase.delete_table(table_name)
        embed = nextcord.Embed(
            title="Warning",
            description=f"Cleared data in the {table_name} successfully.",
            color=0xFFA500
        )
        await ctx.send(embed=embed)
        
    @commands.command(name="servers")
    @commands.is_owner()
    async def servers(self, ctx):
        guilds = self.bot.guilds
        num = 0
        guild_names = []
        for guild in guilds:
            guild_names.append(guild.name)
            num += 1
        embed = nextcord.Embed(
            title="Servers",
            description=f"The bot joined {num} guilds: **{', '.join(guild_names)}**",
            color=0xFFA500
        )
        await ctx.send(embed=embed)
      
async def setup(bot):
    bot.add_cog(AdminCommands(bot))
