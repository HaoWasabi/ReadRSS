# import nextcord
# from nextcord.ext import commands
# from nextcord import Interaction
# from nextcord.ui import View, Button, button

# class ButtonOfPayment(View):
#     def __init__(self, command_premium):
#         super().__init__(timeout=None)
#         self.command_premium = command_premium
        
#     @button(label="1")
#     async def goi1(self, button: Button, interaction: Interaction):
#         await self.command_premium.callback(button, interaction)