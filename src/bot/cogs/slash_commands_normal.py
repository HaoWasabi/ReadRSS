import nextcord
from nextcord.ext import commands
from nextcord import SlashOption, Interaction
from typing import Optional

from ..GUI.embed_test import EmbedTest
from ..GUI.custom_embed import CustomEmbed
from ..GUI.button_of_help_command import ButtonOfHelpCommnad

from ..utils.read_rss_without_saving import ReadRSSWithoutSaving
from ..utils.get_rss import GetRSS

class SlashCommandsNormal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping", description="Check bot latency")
    async def ping(self, interaction: Interaction):
        await interaction.response.defer()
        result = f'Pong! {round(self.bot.latency * 1000)}ms'
        await interaction.followup.send(result)
        
    @nextcord.slash_command(name="get_rss", description="Get the RSS link of a website")
    async def get_rss(self, interaction: Interaction, url: str = SlashOption(description="The website URL")):
        await interaction.response.defer()
        try:
            link_rss = GetRSS(url).get_rss_link()
            await interaction.followup.send(f"RSS link: {link_rss}") if link_rss else await interaction.followup.send("No RSS link found.")
        
        except Exception as e:
            # Đánh dấu rằng phản hồi sẽ được gửi sau
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")
            
    @nextcord.slash_command(name="test", description="Test the bot")
    async def test(self, interaction: Interaction, 
                link_feed: Optional[str] = SlashOption(description="The feed link"), 
                link_atom_feed: Optional[str] = SlashOption(description="The Atom feed link")):
        # Defer the response to avoid timeout
        await interaction.response.defer()

        try:
            if link_atom_feed is None:
                get_rss = GetRSS(link_feed) if link_feed is not None else GetRSS("https://fit.sgu.edu.vn/site/")
                link_atom_feed = get_rss.get_rss_link()

            if link_atom_feed is None:
                await interaction.followup.send('Link Atom feed is not found.')
                return

            read_rss = ReadRSSWithoutSaving(link_atom_feed)
            feed_emty_dto = read_rss.get_first_feed_emty()

            if feed_emty_dto is None:
                raise TypeError("link_first_entry is None")

            id_server = str(interaction.guild.id) if interaction.guild else "DM"
            embed = EmbedTest(id_server, feed_emty_dto)
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")
            
    @nextcord.slash_command(name="help", description="List of commands")
    async def help(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            available_commands = [command.name for command in self.bot.commands]
            available_slash_commands = [command.name for command in self.bot.get_application_commands()]
            
            command_list_1 = ", ".join(available_commands)
            command_list_2 = ", ".join(available_slash_commands)  # type: ignore
            
            id_server = str(interaction.guild.id) if interaction.guild else "DM"
            embed = CustomEmbed(
                id_server=id_server, 
                title="List of commands",                    
                description=f'''
command prefix `{self.bot.command_prefix}`
- The current commands have: {command_list_1}
- The current slash commands have: {command_list_2}
                    '''
                )
            # Đánh dấu rằng phản hồi sẽ được gửi sau
            await interaction.followup.send(embed=embed, view=ButtonOfHelpCommnad())
        
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")
            
def setup(bot):
    bot.add_cog(SlashCommandsNormal(bot))
