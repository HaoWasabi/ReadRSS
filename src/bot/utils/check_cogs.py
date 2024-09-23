from typing import Optional
from nextcord import DMChannel, TextChannel
from nextcord.ext.commands import Context, Cog
from nextcord import Interaction
from typing import Optional

from pyparsing import Opt

class CheckCogs:
    @staticmethod
    async def is_dm_channel(ctx):
        if isinstance(ctx.channel, DMChannel):
            return True
        return False
    
    @staticmethod
    async def is_text_channel(ctx):
        if isinstance(ctx.channel, TextChannel):
            return True
        return False
    
    @staticmethod
    async  def is_server_owner(ctx: Optional[Context] = None, interaction: Optional[Interaction] = None):
        # Kiểm tra nếu ctx hoặc interaction có giá trị, và đảm bảo chỉ có một trong hai được sử dụng
        if ctx and not interaction:
            # Kiểm tra guild có tồn tại và ctx.author có phải là chủ sở hữu guild không
            return ctx.guild is not None and ctx.author.id == ctx.guild.owner_id
        elif interaction and not ctx: 
        # Kiểm tra guild có tồn tại và interaction.user có phải là chủ sở hữu guild không
            if interaction.guild and interaction.user:
                return interaction.user.id == interaction.guild.owner_id
        return False
    

    @staticmethod
    def is_onwer_server_w(fun):
        
        @functools.wraps(fun) # type: ignore
        async def check_is_onwer_server(self: Cog, ctx: Context | Interaction, *args, **kwargs):
            
            if isinstance(ctx, Context):
                if await CheckCogs.is_server_owner(ctx=ctx):
                    return await fun(self, ctx, *args, **kwargs)
                await ctx.send("You need to be the server owner to use this command.")
            if isinstance(ctx, Interaction):
                if await CheckCogs.is_server_owner(interaction=ctx):
                    return await fun(self, ctx, *args, **kwargs)
                
                # await ctx.followup.send_message("You need to be the server owner to use this command.")
                await ctx.response.send_message("You need to be the server owner to use this command.")
                
        return check_is_onwer_server
    
    @staticmethod
    def is_dm_channel_w(fun):
        
        @functools.wraps(fun) # type: ignore
        async def check_is_dm_channel(self: Cog, ctx: Context | Interaction, *args, **kwargs    ):
            if await CheckCogs.is_dm_channel(ctx):
                
                if isinstance(ctx, Context):
                    await ctx.send("Can not send DMChannels")
                if isinstance(ctx, Interaction):
                    await ctx.response.send_message("Cannot send DMChannels", ephemeral=True)
                return True
        
            await fun(self, ctx, *args, **kwargs) # type: ignore
        
                    
        return check_is_dm_channel