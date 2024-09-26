from email import message
from math import e
from tkinter.messagebox import NO
from nextcord import ButtonStyle, DMChannel, Emoji, PartialEmoji, User, Interaction
import logging, os, datetime, mbbank, re
import sys
from typing import Optional, Union
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Context
import nextcord
from nextcord import Interaction, TextChannel
from nextcord.ui import View, Button

from ..utils.datetime_format import datetime_from_string

from ..DTO.user_dto import UserDTO
from ..DTO.premium_dto import PremiumDTO
from ..GUI.button_of_premium import ButtonOfPayment
from ..DTO.user_premium_dto import UserPremiumDTO
from ..DTO.transaction_history_dto import TransactionHistoryDTO
from ..DTO.qr_code_pay_dto import QrPayCodeDTO

from ..BLL.premium_bll import PremiumBLL
from ..BLL.user_premium_bll import UserPremiumBLL
from ..BLL.transaction_history_bll import TransactionHistoryBLL
from ..BLL.qr_pay_code_bll import QrPayCodeBLL
from ..BLL.user_bll import UserBLL
from ..GUI.embed_custom import EmbedCustom

from ..utils.commands_cog import CommandsCog
from ..utils.create_qr_payment import QRGenerator


logger = logging.getLogger('paying')

class CommandPaying(CommandsCog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mb = mbbank.MBBankAsync(username=os.getenv('BANK_USER_NAME'), password=os.getenv('BANK_PASSWORD'))
        self.start_time: datetime.datetime = datetime.datetime.now()
        
    @tasks.loop(seconds=5)
    async def check_qr_code(self):
        qr_pay_code_bll = QrPayCodeBLL()
        all_qr = qr_pay_code_bll.get_all_qr_pay_code()
        for i in all_qr:
            denta = datetime.datetime.now() - i.date_created  # type: ignore
            if denta > datetime.timedelta(minutes=3) and not i.is_success:
                qr_pay_code_bll.delete_qr_pay_by_id(i.qr_code)
                channel = self.bot.get_channel(int(i.channel_id)) or self.bot.fetch_user(int(i.channel_id))
                
                if channel is None: 
                    logger.warning('Không tìm thấy channel')
                    return
                
                if isinstance(channel, TextChannel):
                    message = await channel.fetch_message(int(i.message_id))
                    await message.edit(content='QR đã hết hạn', embed=None)
                elif isinstance(channel, DMChannel):
                    await channel.send('QR đã hết hạn')
    
    async def get_bank_history(self):
        from_day = datetime.datetime.now()
        an = os.getenv('BANK_USER_NAME')
        if an is None:
            logger.error('Không có BANK_USER_NAME')
            sys.exit(0)
            
        history = await self.mb.getTransactionAccountHistory(accountNo=an, from_date=from_day - datetime.timedelta(days=2), to_date=from_day)
        for i in history['transactionHistoryList']:
            transaction_id = i.get('refNo', '')
            transactionDate = i.get('transactionDate', '')
            creditAmount = int(i.get('creditAmount', ''))
            currency = i.get('currency', '')
            description: str = i.get('description', '')
            
            transaction_history_bll = TransactionHistoryBLL()
            qr_pay_code_bll = QrPayCodeBLL()
            user_bll = UserBLL()
            premium_bll = PremiumBLL()
            
            for qrcode in re.findall("T\\d{20}T", description.replace(' ', '').upper()):
                qr = qr_pay_code_bll.get_qr_pay_code_by_qr_code(qrcode.replace("T", ""))
                
                if qr is None:
                    continue
                
                transaction = transaction_history_bll.get_transaction_history_by_id(transaction_id)
                if transaction is not None:
                    break
                
                transaction_history_bll.insert_transaction_history(TransactionHistoryDTO(
                    transaction_id, 
                    qrcode,
                    datetime.datetime.strptime(transactionDate, '%d/%m/%Y %H:%M:%S'),
                    description,
                    creditAmount,
                    currency
                ))
                
                qr.is_success = True
                qr_pay_code_bll.insert_qr_pay_code(qr)
                user_dto = user_bll.get_user_by_user_id(qr.user_id)
                premium_dto = premium_bll.get_premium_by_id(qr.premium_id)
                if premium_dto is None:
                    logger.error(f'PremiumDTO không tìm thấy cho premium_id: {qr.premium_id}')
                    continue
                if user_dto is None:
                    logger.error(f'UserDTO không tìm thấy cho user_id: {qr.user_id}')
                    continue
                user_premium_dto = UserPremiumDTO(user_dto, premium_dto, datetime.datetime.now())
                await self.pay_success(qr, user_premium_dto)
    
    async def pay_success(self, qr: QrPayCodeDTO, user_premium_dto: UserPremiumDTO):
        try:
            channel = self.bot.get_channel(int(qr.channel_id)) or self.bot.fetch_user(int(qr.channel_id))
            user_premium_bll = UserPremiumBLL()
            if channel is None: 
                logger.warning('Không tìm thấy channel')
                return
            
            if isinstance(channel, TextChannel):
                user_premium_bll.insert_user_premium(user_premium_dto)
                message = await channel.fetch_message(int(qr.message_id))
                await message.edit(content='Thanh toán thành công', embed=None)
            elif isinstance(channel, DMChannel):
                user_premium_bll.insert_user_premium(user_premium_dto)
                await channel.send('Thanh toán thành công')
                
        except Exception as e:
            logger.error(f'Không thể thanh toán: {e}')
                             
    @tasks.loop(seconds=30)
    async def start_listener_bank_history(self):
        if datetime.datetime.now() - self.start_time > datetime.timedelta(minutes=5):
            self.start_listener_bank_history.stop()
        
        await self.get_bank_history() 

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Kiểm tra mã QR bắt đầu')
        if not self.check_qr_code.is_running():
            self.check_qr_code.start()
              
    @commands.command(name="premium")
    async def pay_command(self, ctx: Context):
        '''Nạp để mở gói premium'''
        user_dto = UserDTO(str(ctx.author.id), ctx.author.name)
        UserBLL().insert_user(user_dto)
        
        embed_text = EmbedCustom(
            id_server=str(ctx.guild.id) if ctx.guild else str(ctx.author.id),
            title="Nạp để mở gói premium",
            description="Gói premium mang đến nhiều tính năng hơn. Đây là một số gói cơ bản:"
        )
        
        premium_bll = PremiumBLL()
        buttons = View()
        
        cls = self
        
        class GóiButton(Button):
            def __init__(self, pre: PremiumDTO):
                super().__init__(label=pre.get_premium_name())
                self.pre = pre
                
            async def callback(self, interaction: Interaction):
                embed_text = EmbedCustom(
                    id_server=str(ctx.guild.id) if ctx.guild else str(ctx.author.id),
                    title="Nạp để mở gói premium",
                    description="Gói premium mang đến nhiều tính năng hơn"
                )

                embed_text.add_field(name="Ngân hàng MB-Bank", value=os.getenv('BANK_USER_NAME'), inline=False)
                embed_text.add_field(name="Số tiền:", value=f"{self.pre.get_price()}đ", inline=False)
                
                qr_id = QRGenerator.generator_id()
                embed_text.add_field(name="Nội dung:", value=f"T{qr_id}T", inline=False)
                
                embed_text.set_image(QRGenerator.generator_qr(qr_id))
                message = await interaction.edit(content='', embed=embed_text, view=None)
                
                if message is None:
                    await ctx.send('Có gì đó lạ lắm')
                    return
                
                qr = QrPayCodeDTO(
                    qr_id, 
                    str(ctx.author.id), 
                    str(message.channel.id) if message.channel.id else str(ctx.author.id), 
                    self.pre.get_premium_id(),  # type: ignore
                    str(message.id), 
                    datetime.datetime.now(), 
                    False
                )
                
                qr_pay_code_bll = QrPayCodeBLL()
                qr_pay_code_bll.insert_qr_pay_code(qr)
                
                if not cls.start_listener_bank_history.is_running():
                    cls.start_listener_bank_history.start()
                cls.start_time = datetime.datetime.now()

        for pre in premium_bll.get_all_premiums():
            embed_text.add_field(
                name=pre.get_premium_name(), 
                value=f"{pre.get_description()}\nGiá: {pre.get_price()}đ\nThời hạn: {pre.get_duration()}",
                inline=False
            )
                    
            buttons.add_item(GóiButton(pre))
        
        await ctx.send(embed=embed_text, view=buttons)

    @nextcord.slash_command(name="premium", description="Nạp để mở gói premium")
    async def pay_slash_command(self, interaction: Interaction):
        await interaction.response.defer()
        
        # Kiểm tra nếu là DM, sử dụng user_id thay vì guild_id
        id_server = str(interaction.guild.id) if interaction.guild else str(interaction.user.id) # type: ignore
        
        user_dto = UserDTO(str(interaction.user.id), interaction.user.name) # type: ignore
        UserBLL().insert_user(user_dto)
        
        embed_text = EmbedCustom(
            id_server=id_server,  # Dùng id_server để hỗ trợ cả guild và DM
            title="Nạp để mở gói premium",
            description="Gói premium mang đến nhiều tính năng hơn. Đây là một số gói cơ bản:"
        )
        
        premium_bll = PremiumBLL()
        buttons = View()
        
        cls = self
        
        class GóiButton(Button):
            def __init__(self, pre: PremiumDTO):
                super().__init__(label=pre.get_premium_name())
                self.pre = pre
                
            async def callback(self, interaction: Interaction):
                embed_text = EmbedCustom(
                    id_server=id_server,  # Sử dụng id_server cho embed
                    title="Nạp để mở gói premium",
                    description="Gói premium mang đến nhiều tính năng hơn"
                )

                embed_text.add_field(name="Ngân hàng MB-Bank", value=os.getenv('BANK_USER_NAME'), inline=False)
                embed_text.add_field(name="Số tiền:", value=f"{self.pre.get_price()}đ", inline=False)
                
                qr_id = QRGenerator.generator_id()
                embed_text.add_field(name="Nội dung:", value=f"T{qr_id}T", inline=False)
                
                embed_text.set_image(QRGenerator.generator_qr(qr_id))
                message = await interaction.edit(content='', embed=embed_text, view=None)
                
                if message is None:
                    await interaction.followup.send('Có gì đó lạ lắm')
                    return
                
                # Lưu QR code với user_id hoặc channel_id tương ứng
                qr = QrPayCodeDTO(
                    qr_id, 
                    str(interaction.user.id), # type: ignore # Sử dụng user ID trong DM 
                    str(message.channel.id) if message.channel.id else str(interaction.user.id),  # type: ignore
                    self.pre.get_premium_id(),  # type: ignore
                    str(message.id), 
                    datetime.datetime.now(), 
                    False
                )
                
                qr_pay_code_bll = QrPayCodeBLL()
                qr_pay_code_bll.insert_qr_pay_code(qr)
                
                # Bắt đầu kiểm tra lịch sử ngân hàng và mã QR
                if not cls.start_listener_bank_history.is_running():
                    cls.start_listener_bank_history.start()
                cls.start_time = datetime.datetime.now()

                if not cls.check_qr_code.is_running():
                    cls.check_qr_code.start()

        for pre in premium_bll.get_all_premiums():
            embed_text.add_field(
                name=pre.get_premium_name(), 
                value=f"{pre.get_description()}\nGiá: {pre.get_price()}đ\nThời hạn: {pre.get_duration()}",
                inline=False
            )
                    
            buttons.add_item(GóiButton(pre))
        
        await interaction.followup.send(embed=embed_text, view=buttons)

async def setup(bot: commands.Bot):
    bot.add_cog(CommandPaying(bot))
