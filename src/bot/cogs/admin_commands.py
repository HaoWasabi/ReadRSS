import nextcord
from nextcord.ext import commands
from typing import Optional
from ..utils.Database import dataBase
from nextcord.ext.commands import Bot
from ..BLL.channel_feed_bll import ChannelFeedBLL
from ..BLL.channel_emty_bll import ChannelEmtyBLL
from ..GUI.custom_embed import CustomEmbed
from ..GUI.select_view_of_superclear_command import SelectView

class AdminCommands(commands.Cog):
    
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        try: 
            embed = CustomEmbed(
                id_server=str(ctx.guild.id),
                title="Warning",
                description="The bot is shutting down...",
                color=0xFFA500
            )
            await ctx.send(embed=embed)
            await self.bot.close()
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"Error: {e}")
    
    @commands.command(name="superclear")
    @commands.is_owner()
    async def superclear(self, ctx):
        embed = CustomEmbed(
            id_server=str(ctx.guild.id),
            title="Warning",
            description="Choice an option to clear in database.",
            color=0xFFA500
        )
        await ctx.send(embed=embed, view=SelectView(user=ctx.author))

    @commands.command(name="supershow")
    @commands.is_owner()
    async def supershow(self, ctx):
        try:
            num = 0
            channel_feed_bll = ChannelFeedBLL()
            id_server = str(ctx.guild.id)
            
            # Tạo dictionary để nhóm các channel và feed theo server
            server_data = {}
            
            for channel_feed_dto in channel_feed_bll.get_all_channel_feed():
                channel_dto = channel_feed_dto.get_channel()
                feed_dto = channel_feed_dto.get_feed()
                
                channel = self.bot.get_channel(int(channel_dto.get_id_channel()))
                for server in self.bot.guilds:
                    if channel in server.channels:
                        server_name = f"**Server:** {server.name} ({server.id})"
                        channel_info = f"- **{channel_dto.get_name_channel()}** (`{channel_dto.get_id_channel()}`) - [{feed_dto.get_title_feed()}]({feed_dto.get_link_feed()})"
                        
                        # Thêm channel và feed vào server tương ứng
                        if server_name not in server_data:
                            server_data[server_name] = []
                        server_data[server_name].append(channel_info)
                        num += 1
            
            # Chuẩn bị nội dung cho embed
            embed = CustomEmbed(
                id_server=id_server,
                title="List of Feeds in Channels",
                description=f" You have {num} feeds in channels:",
                color=0xFFA500
            )
            
            # Thêm thông tin server và channel vào embed
            for server_name, channels in server_data.items():
                embed.add_field(
                    name=server_name,
                    value="\n".join(channels) if channels else "No channels found.",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error: {e}")
    
    @commands.command(name="superdelete")
    @commands.is_owner()
    async def superdelete(self, ctx, id_channel: str, link_feed: Optional[str] = None):
        try:
            channel_feed_bll = ChannelFeedBLL()
            if link_feed is None:
                channel_feed_bll.delete_channel_feed_by_id_channel(id_channel)
            else:
                channel_feed_bll.delete_channel_feed_by_id_channel_and_link_feed(id_channel, link_feed)
            
            embed = CustomEmbed(
                id_server=str(ctx.guild.id),
                title="Warning",
                description=f"Deleted feed settings for {id_channel} successfully.",
                color=0xFFA500
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}", e)
            print(f"Error: {e}")
        
    @commands.command(name="servers")
    @commands.is_owner()
    async def servers(self, ctx):
        guilds = self.bot.guilds
        num = 0
        guild_names = []
        for guild in guilds:
            guild_names.append(guild.name)
            num += 1
        embed = CustomEmbed(
            id_server=str(ctx.guild.id),
            title="Servers",
            description=f"The bot joined {num} guilds: **{', '.join(guild_names)}**",
            color=0xFFA500
        )
        await ctx.send(embed=embed)
      
async def setup(bot):
    bot.add_cog(AdminCommands(bot))
