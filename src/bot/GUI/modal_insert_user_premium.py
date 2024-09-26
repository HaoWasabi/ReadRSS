from re import U
from nextcord import Interaction, User
from nextcord.ui import TextInput, Modal
from datetime import datetime
from ..DTO.user_premium_dto import UserPremiumDTO
from ..DTO.user_dto import UserDTO
from ..DTO.premium_dto import PremiumDTO
from ..utils.check_authorization import check_authorization
from ..BLL.user_premium_bll import UserPremiumBLL
from ..BLL.user_bll import UserBLL
from ..BLL.premium_bll import PremiumBLL

class ModalInserUserPremium(Modal):
    def __init__(self, user, bot):
        self.bot = bot
        super().__init__(title="Insert User To Have Premium")
        self.author = user
        self.id_user = TextInput(label="User ID", placeholder="Enter the user ID", required=True)
        self.id_premium = TextInput(label="Premium ID", placeholder="Enter the premium ID", required=True)
        self.add_item(self.id_user)
        self.add_item(self.id_premium)
        
    async def callback(self, interaction: Interaction):
        # Kiểm tra quyền
        if not await check_authorization(interaction, self.author):
            return
        
        await interaction.response.defer()
        try:
            user_premium_bll = UserPremiumBLL()
            user_bll = UserBLL()
            premium_bll = PremiumBLL()

            user_id = self.id_user.value.strip() if self.id_user.value else ""  # Loại bỏ khoảng trắng thừa
            premium_id = self.id_premium.value.strip() if self.id_premium.value else ""

            # Kiểm tra xem user_id và premium_id có hợp lệ không
            if not user_id or not user_bll.get_user_by_user_id(user_id):
                await interaction.followup.send(
                    f"User ID '{user_id}' not found.",
                    ephemeral=True
                )
                return
            
            if not premium_id or not premium_bll.get_premium_by_id(premium_id):
                await interaction.followup.send(
                    f"Premium ID '{premium_id}' not found.",
                    ephemeral=True
                )
                return
            
            # Lấy thông tin người dùng từ bot
            user_object = await self.bot.fetch_user(int(user_id))  # Đã thêm await ở đây
            if not user_object:
                await interaction.followup.send(
                    f"User ID '{user_id}' not found in bot's cache.",
                    ephemeral=True
                )
                return
            
            user_name = user_object.name

            # Thêm user vào database nếu chưa có
            user_dto = UserDTO(
                user_id=user_id,  # type: ignore
                user_name=user_name
            )
            user_bll.insert_user(user_dto)

            # Lấy thông tin premium từ database
            premium_dto = premium_bll.get_premium_by_id(premium_id)

            # Tạo DTO cho UserPremium
            user_premium_dto = UserPremiumDTO(
                user=user_dto,  # type: ignore
                premium=premium_dto,  # type: ignore
                date_registered=datetime.now()
            )

            # Thêm thông tin user_premium vào database
            user_premium_bll.insert_user_premium(user_premium_dto)

            await interaction.followup.send(
                f"Successfully added premium for User ID '{user_id}'.",
                ephemeral=True
            )

        except Exception as e:
            await interaction.followup.send(
                f"Error: {e}",
                ephemeral=True
            )
