from nextcord import Interaction
from nextcord.ui import TextInput, Modal
from ..utils.check_authorization import check_authorization
from ..BLL.premium_bll import PremiumBLL

class ModalDeletePremium(Modal):
    def __init__(self, user):
        super().__init__(title="Delete Premium")  # Sửa tiêu đề phù hợp với chức năng
        self.author = user
        self.id_premium = TextInput(label="Premium ID", placeholder="Enter the premium ID", required=True)
        self.add_item(self.id_premium)
        
    async def callback(self, interaction: Interaction):
        # Kiểm tra quyền hạn
        if not await check_authorization(interaction, self.author):
            return
        
        await interaction.response.defer()
        
        premium_bll = PremiumBLL()
        
        # Lấy premium_dto
        premium_dto = premium_bll.get_premium_by_id(self.id_premium.value) # type: ignore
        
        if not premium_dto:
            await interaction.followup.send(f"Premium ID '{self.id_premium.value}' not found.", ephemeral=True)
            return
        
        # Xóa premium và gửi thông báo
        premium_bll.delete_premium_by_id(self.id_premium.value) # type: ignore
        
        await interaction.followup.send(
            f"Successfully deleted premium **{premium_dto.get_premium_name()}** (`{self.id_premium.value}`).",
            ephemeral=True
        )
