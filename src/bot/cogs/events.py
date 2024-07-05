from nextcord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} is ready")
        print("Các lệnh hiện có:", [command.name for command in self.bot.commands])

        # Đồng bộ lệnh slash
        await self.bot.sync_application_commands()
        print("Đã đồng bộ các lệnh slash")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            available_commands = [command.name for command in self.bot.commands]
            command_list = ", ".join(available_commands)
            await ctx.send(f"Lệnh không tồn tại. Các lệnh hiện có: {command_list}")
        else:
            raise error

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined {guild.name} (id: {guild.id})")
        await guild.system_channel.send("Hello!")
        print("Các lệnh hiện có:", [command.name for command in self.bot.commands])

async def setup(bot):
    await bot.add_cog(Events(bot))
