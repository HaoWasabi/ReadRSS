from nextcord import Interaction
from nextcord.ui import TextInput, Modal
from datetime import datetime
from ..DTO.premium_dto import PremiumDTO
from ..utils.check_authorization import check_authorization
from ..BLL.premium_bll import PremiumBLL

# PremiumDAL().insert_premium(PremiumDTO('1', 'gói 1', 'gói cơ bản', 10000, datetime.now(), 2, True))
class ModalInserPremium(Modal):
    def __init__(self, user):
        super().__init__(title="Insert Premium")
        self.author = user
        self.name_premium = TextInput(label="Premium name", placeholder="Enter the premium name", required=True)
        self.description_premixum = TextInput(label="Premium description", placeholder="Enter the premium description", required=True)
        self.price = TextInput(label="Price", placeholder="Enter the price", required=True)
        self.duration = TextInput(label="Duration (minutes)", placeholder="Enter the duration", required=True)
        self.add_item(self.name_premium)
        self.add_item(self.description_premixum)
        self.add_item(self.price)
        self.add_item(self.duration)
        
    async def callback(self, interaction: Interaction):
        if not await check_authorization(interaction, self.author):
            return
        
        await interaction.response.defer()
        try:
            premium_bll = PremiumBLL()
            
            premium_dto = PremiumDTO(
                premium_id=None,  # type: ignore
                premium_name=self.name_premium.value, # type: ignore
                description=self.description_premixum.value, # type: ignore
                price=self.price.value, # type: ignore
                date_created=datetime.now(), 
                duration=self.duration.value, # type: ignore
                is_active=True)
            if premium_bll.insert_premium(premium_dto):
                await interaction.followup.send(
                    f"Successfully insert premium **{self.name_premium.value}**.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.followup.send(
                f"Error: {e}",
                ephemeral=True
            )