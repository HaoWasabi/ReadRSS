import logging
import nextcord
from nextcord.ext import commands
from ..utils.commands_cog import CommandsCog
from ..utils.check_have_premium import check_have_premium

logger = logging.getLogger("CommandCheckPremium")

class CheckPremium(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)
        
    def check_have_premium(self, user_id: str) -> str:
        return f"User <@{user_id}> (`{user_id}`) has premium." if check_have_premium(user_id) else f"User <@{user_id}> (`{user_id}`) does not have premium."

    @commands.command(name="checkpremium")
    async def command_check_premium(self, ctx):
        '''Check if the user has premium'''
        await ctx.send(self.check_have_premium(str(ctx.author.id)))
        
    @nextcord.slash_command(name="checkpremium", description="Check if the user has premium")
    async def slash_command_check_premium(self, interaction):
        await interaction.response.defer()
        await interaction.followup.send(self.check_have_premium(str(interaction.user.id)))

def setup(bot):
    bot.add_cog(CheckPremium(bot))
        