import nextcord
from nextcord import SelectOption
from nextcord.ui import Select, View
from ..utils.check_authorization import check_authorization
from ..DTO.color_dto import ColorDTO
from ..GUI.embed_custom import EmbedCustom
from ..GUI.modal_insert_premium import ModalInserPremium
from ..GUI.modal_delete_premium import ModalDeletePremium
from ..BLL.premium_bll import PremiumBLL

class SelectPremium(View):
    def __init__(self, user, bot):
        super().__init__()
        self.author = user
        self.bot = bot
        self.color = int(ColorDTO("darkkhaki").get_hex_color().replace("#", ""), 16)

        self.select = Select(
            placeholder="Choose an option to change premium.",
            min_values=1,
            max_values=1,
            options=[
                SelectOption(label="insert", value="insert", description="Insert a premium."),
                SelectOption(label="delete", value="delete", description="Delete a premium."),
                SelectOption(label="show", value="show", description="Show list of premiums."),
            ]
        )

        self.add_item(self.select)
        self.select.callback = self.select_callback

    # Callback for Select
    async def select_callback(self, interaction: nextcord.Interaction):
        # Check for authorization
        if not await check_authorization(interaction, self.author):
            await interaction.followup.send("You are not authorized to use this command.", ephemeral=True)
            return

        selection = self.select.values[0]

        if selection == "insert":
            # Show the insert modal
            await interaction.response.send_modal(ModalInserPremium(self.author))

        elif selection == "delete":
            # Show the delete modal
            await interaction.response.send_modal(ModalDeletePremium(self.author))

        elif selection == "show":
            # Defer response to allow for time-consuming operations
            await interaction.response.defer()
            try:
                premium_bll = PremiumBLL()
                data = []
                num = 0

                # Fetch all premium data
                for premium_dto in premium_bll.get_all_premiums():
                    premium_info = f'''
**{premium_dto.get_premium_name()}** (`{premium_dto.get_premium_id()}`)
- Description: {premium_dto.get_description()}
- Price: {premium_dto.get_price()}
- Duration (ms): {premium_dto.get_duration()}
- Date created: {premium_dto.get_date_created()}
'''
                    data.append(premium_info + "\n")
                    num += 1

                # Create an embed with the premium data
                id_server = str(interaction.guild_id) if interaction.guild else str(interaction.user.id)  # type: ignore
                embed = EmbedCustom(
                    id_server=id_server,
                    title="List of Premiums",
                    description=f"You have {num} premiums:\n" + "\n".join(data),
                    color=self.color
                )

                # Send the embed as followup
                await interaction.followup.send(embed=embed, ephemeral=True)

            except Exception as e:
                # Handle errors
                await interaction.followup.send(f"Error: {e}", ephemeral=True)
                print(f"Error: {e}")
