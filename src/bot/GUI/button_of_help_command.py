import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ui import View, Button, button

class ButtonOfHelpCommnad(View):
    def __init__(self):
        super().__init__()
        button = Button(style=nextcord.ButtonStyle.link, label="Join the support server", url="https://discord.com/invite/Q7NXBFpZeM")
        self.add_item(button)

    @button(label="Infor", style=nextcord.ButtonStyle.primary)
    async def send_message(self, button: Button, interaction: Interaction):
        await interaction.response.send_message(''' 
```This is a Discord bot built with Python. ReadRSS bot brings RSS feeds 
to your Discord server. Receive notifications from news sources 
including Facebook and much more. 

                        -- ABOUT US --
                         
         ██████╗  ██████╗██████╗ ███████╗██╗   ██╗     Summer 2024
        ██╔════╝ ██╔════╝██╔══██╗██╔════╝██║   ██║     + HaoWasabi
        ██║  ███╗██║     ██║  ██║█████╗  ██║   ██║     + nguyluky
        ██║   ██║██║     ██║  ██║██╔══╝  ╚██╗ ██╔╝     + NaelTuhline
        ╚██████╔╝╚██████╗██████╔╝███████╗ ╚████╔╝      + tivibin789
        ╚═════╝  ╚═════╝╚═════╝ ╚══════╝  ╚═══╝        
                                                     
        ```''')
