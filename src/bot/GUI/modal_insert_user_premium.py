from nextcord import Interaction, SelectOption
import nextcord
from nextcord.ui import TextInput, Modal, Select
from datetime import date, datetime
from ..DTO.user_premium_dto import UserPremiumDTO
from ..DTO.user_dto import UserDTO
from ..DTO.premium_dto import PremiumDTO
from ..utils.check_authorization import check_authorization
from ..BLL.user_premium_bll import UserPremiumBLL
from ..BLL.user_bll import UserBLL
from ..BLL.premium_bll import PremiumBLL

class ModalInserUserPremium(Modal):
    def __init__(self, user, bot, id_premium):
        self.bot = bot
        super().__init__(title="Insert User To Have Premium")
        self.author = user
        self.id_user = TextInput(label="User ID", placeholder="Enter the user ID", required=True)
        self.id_premium = id_premium
        self.add_item(self.id_user)
        
    async def callback(self, interaction: Interaction):
        try:
            # Kiểm tra quyền
            if not await check_authorization(interaction, self.author):
                await interaction.followup.send("You are not authorized to perform this action.", ephemeral=True)
                return
            
            await interaction.response.defer()  # Dùng defer để phản hồi không hết thời gian
            
            user_premium_bll = UserPremiumBLL()
            user_bll = UserBLL()
            premium_bll = PremiumBLL()

            user_id = self.id_user.value.strip() if self.id_user.value else ""  # Loại bỏ khoảng trắng thừa

            # Kiểm tra xem user_id và self.id_premium có hợp lệ không
            if not user_id:
                await interaction.followup.send("User ID cannot be empty.", ephemeral=True)
                return
            
            # Kiểm tra người dùng trong database
            user_in_db = user_bll.get_user_by_user_id(user_id)
            if not user_in_db:
                await interaction.followup.send(f"User ID '{user_id}' not found in database.", ephemeral=True)
                return
            
            # Kiểm tra Premium ID trong database
            premium_in_db = premium_bll.get_premium_by_id(self.id_premium)
            if not premium_in_db:
                await interaction.followup.send(f"Premium ID '{self.id_premium}' not found in database.", ephemeral=True)
                return
            
            # Fetch user từ bot
            try:
                user_object = await self.bot.fetch_user(int(user_id))
            except Exception as e:
                await interaction.followup.send(f"Error fetching user from bot: {str(e)}.", ephemeral=True)
                return
            
            if not user_object:
                await interaction.followup.send(f"User ID '{user_id}' not found in bot's cache.", ephemeral=True)
                return
            
            user_name = user_object.name

            # Thêm user vào database nếu chưa có
            user_dto = UserDTO(
                user_id=user_id,
                user_name=user_name
            )
            user_bll.insert_user(user_dto)  # Chèn nếu chưa có

            # Lấy thông tin premium từ database
            premium_dto = premium_bll.get_premium_by_id(self.id_premium)

            if not premium_dto:
                await interaction.followup.send(f"Premium ID '{self.id_premium}' not found in database.", ephemeral=True)
                return

            # Tạo DTO cho UserPremium
            user_premium_dto = UserPremiumDTO(
                user=user_dto,
                premium=premium_dto,
                date_registered= datetime.now()
            )

            # Thêm thông tin user_premium vào database
            user_premium_bll.insert_user_premium(user_premium_dto)

            await interaction.followup.send(
                f"Successfully added premium (`{self.id_premium}`) for user (`{user_id}`).",
                ephemeral=True
            )

        except Exception as e:
            await interaction.followup.send(
                f"An error occurred: {str(e)}",
                ephemeral=True
            )
            print(f"Error in callback: {str(e)}")
