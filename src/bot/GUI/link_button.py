import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ui

class LinkButton(ui.View):
    def __init__(self):
        super().__init__()

    @ui.button(label="More help", style=nextcord.ButtonStyle.primary)
    async def send_message(self, button: ui.Button, interaction: Interaction):
        await interaction.response.send_message(''' 
            Need more help? Let's join our server: https://discord.com/invite/Q7NXBFpZeM 
        ''', ephemeral=True)
