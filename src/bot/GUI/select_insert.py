import nextcord
from nextcord.ui import View
from nextcord import SelectOption
from ..utils.check_authorization import check_authorization
from .modal_insert_user_premium import ModalInserUserPremium
from .modal_insert_premium import ModalInserPremium

class SelectInsert(View):
    def __init__(self, user, bot):
        super().__init__()
        self.author = user  # Store the user who initiated the interaction
        self.bot = bot

    @nextcord.ui.select(
        placeholder="Choose a command category",
        options=[
            SelectOption(label="premium", value="premium", description="Insert a premium."),
            SelectOption(label="userpremium", value="userpremium", description="Insert user to have premium.")
        ]
    )
    
    async def select_callback(self, select, interaction: nextcord.Interaction):
        if not await check_authorization(interaction, self.author):
            return
        
        selection = select.values[0]
        if selection == "premium":
            await interaction.response.send_modal(ModalInserPremium(self.author))
                
        if selection == "userpremium":
            await interaction.response.send_modal(ModalInserUserPremium(self.author, self.bot))
         