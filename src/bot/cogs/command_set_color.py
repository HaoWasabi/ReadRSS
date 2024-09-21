import logging
from ..utils.commands_cog import CommandsCog
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from ..DTO.color_dto import ColorDTO
from ..DTO.server_dto import ServerDTO
from ..BLL.server_bll import ServerBLL
from ..GUI.embed_custom import EmbedCustom

logger = logging.getLogger("CommandSetColor")

class CommandSetColor(CommandsCog):
    def __init__(self, bot):
        super().__init__(bot)
        
    @commands.command(name='setcolor')
    async def command_set_color(self, ctx, color: str):
        if await self.is_dm_channel(ctx):
            return
        if not color:
            await ctx.send('This command must have color.')
            return
        await self._set_color(ctx, color)
        
    @nextcord.slash_command(name="setcolor", description="Set the color of all embeds that you want it would send")
    async def slash_set_color(self, interaction: Interaction, 
                              color: str = SlashOption(
                                  name="color",
                                  description="Choose a color for the embeds",
                                  choices={"Red": "red", "Orange": "orange", "Yellow": "yellow", "Green": "green", 
                                           "Blue": "blue", "Purple": "purple", "Black": "black", "Gray": "gray"}
                              )):
        await interaction.response.defer()
        
        if not interaction.guild:
            await interaction.followup.send("This command can only be used in a server.")
            return

        await self._set_color(interaction.followup, color, interaction.guild)
            
    async def _set_color(self, ctx, color: str, guild=None):
        if await self.is_dm_channel(ctx):
            return
        
        guild = guild or ctx.guild

        try:
            server_bll = ServerBLL()
            color_dto = ColorDTO(color)
            server_dto = ServerDTO(str(guild.id), guild.name, color_dto.get_hex_color())
            
            if not server_bll.get_server_by_server_id(server_dto.get_server_id()):
                server_bll.insert_server(server_dto)
            else:
                server_bll.update_server(server_dto)
            
            hex_color = color_dto.get_hex_color()
            embed = EmbedCustom(
                id_server=server_dto.get_server_id(),
                title="Set color",
                description=f"Set color **{color_dto.get_name_color()}** successfully.",
                color=int(hex_color, 16)
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

async def setup(bot):
    bot.add_cog(CommandSetColor(bot))
