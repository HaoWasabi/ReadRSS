import nextcord
from nextcord.ui import Select, View
from nextcord import SelectOption
from ..BLL.premium_bll import PremiumBLL
from ..utils.check_authorization import check_authorization
from .modal_insert_user_premium import ModalInserUserPremium

class SelectInsertUserPremium(View):
    def __init__(self, user, bot):
        super().__init__()
        self.author = user
        self.bot = bot

        # Tạo Select với các tùy chọn premium
        self.select = Select(
            placeholder="Choose a premium to insert premium for user.",
            min_values=1,
            max_values=1,
            options=self.premium_options()  # Gọi hàm để tạo danh sách các tùy chọn
        )
        
        self.add_item(self.select)
        self.select.callback = self.select_callback
        
    # Callback cho Select
    async def select_callback(self, interaction: nextcord.Interaction):
        # Kiểm tra quyền
        if not await check_authorization(interaction, self.author):
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return
        
        selection = self.select.values[0]
        if selection:
            id_premium = int(selection)
            premium_bll = PremiumBLL()
            premium = premium_bll.get_premium_by_id(id_premium)
            if premium:
                premium_id = premium.get_premium_id()
                await interaction.response.send_modal(ModalInserUserPremium(self.author, self.bot, premium_id))
            else:
                await interaction.response.send_message(f"Invalid selection: {selection}", ephemeral=True)
  
    # Hàm để tạo danh sách các tùy chọn cho Select
    def premium_options(self) -> list[SelectOption]:
        premium_bll = PremiumBLL()
        premiums = premium_bll.get_all_premiums()
        options = []

        # Kiểm tra nếu có gói premium nào trong danh sách
        if premiums:
            for premium in premiums:
                try:
                    options.append(SelectOption(
                        label=premium.get_premium_name(),
                        description=premium.get_description(),
                        value=str(premium.get_premium_id())
                    ))
                except Exception as e:
                    print(f"Error creating SelectOption for premium: {str(e)}")
        else:
            # Nếu không có gói premium, thêm tùy chọn thông báo không có gói
            options.append(SelectOption(
                label="No premiums available",
                description="Currently, there are no premiums to select.",
                value="no_premium",
                default=True  # Chỉ chọn mục này nếu không có gói nào khác
            ))
            
        return options
