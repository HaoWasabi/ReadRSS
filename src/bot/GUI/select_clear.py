# import nextcord
# from nextcord.ui import View
# from nextcord import SelectOption
# from ..utils.check_authorization import check_authorization
# from ..GUI.modal_clear_table_of_db import ModalClearTable
# from ..utils.Database import dataBase

# class SelectClear(View):
#     def __init__(self, user):
#         super().__init__()
#         self.author = user  # Store the user who initiated the interaction

#     @nextcord.ui.select(
#         placeholder="Choose a command category",
#         options=[
#             SelectOption(label="all", value="all", description="Clear all database."),
#             SelectOption(label="tbl", value="tbl", description="Clear a table in database."),
#             SelectOption(label="feed", value="feed", description="Clear a feed in database."), 
#             SelectOption(label="premium", value="premium", description="Hide a premium in database.")
#         ]
#     )
    
#     async def select_callback(self, select, interaction: nextcord.Interaction):
#         if not await check_authorization(interaction, self.author):
#             return
        
#         selection = select.values[0]
#         if selection == "all":
#             dataBase.clear()
#             await interaction.response.send_message("Cleared all database successfully.", ephemeral=True)
        
#         elif selection == "tbl":
#             await interaction.response.send_modal(ModalClearTable(self.author))
            