from email import message
from tkinter.messagebox import NO
from discord import ButtonStyle, Emoji, PartialEmoji
import logging, os , datetime, mbbank, re
import sys
from typing import Optional
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Context
import nextcord
from nextcord import Interaction, SlashOption, TextChannel
from nextcord.ui import View, Button, button

from ..utils.datetime_format import datetime_from_string

from ..DTO.premium_dto import PremiumDTO

from ..GUI.button_of_premium import ButtonOfPayment

from ..DTO.user_premium_dto import UserPremiumDTO
from ..DTO.transaction_history_dto import TransactionHistoryDTO
from ..DTO.qr_code_pay_dto import QrPayCodeDTO

from ..BLL.premium_bll import PremiumBLL
from ..BLL.user_premium_bll import UserPremiumBLL
from ..BLL.transaction_history_bll import TransactionHistoryBLL
from ..BLL.qr_pay_code_bll import QrPayCodeBLL

from ..GUI.embed_custom import EmbedCustom

from ..utils.commands_cog import CommandsCog
from ..utils.create_qr_payment import QRGenerator

logger = logging.getLogger('paying')

class CommandPaying(CommandsCog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mb = mbbank.MBBankAsync( username=os.getenv('BANK_USER_NAME'), password=os.getenv('BANK_PASSWORD'))
        self.start_time: datetime.datetime = datetime.datetime.now()
        
    @tasks.loop(seconds=5)
    async def check_qr_code(self):
        qr_pay_code_bll = QrPayCodeBLL()
        all_qr = qr_pay_code_bll.get_all_qr_pay_code()
        for i in all_qr:
            denta = datetime.datetime.now() - i.date_created # type: ignore
            # kiểm tra hết hạng của mã qr
            # ở đây tôi để 3p
            if denta > datetime.timedelta(minutes=3) and not i.is_success:
                qr_pay_code_bll.delete_qr_pay_by_id(i.qr_code)
                channel = self.bot.get_channel(int(i.channel_id))
                
                if (channel is None): 
                    logger.warning('không tìm thấy channel')
                    return
                
                if isinstance(channel, TextChannel):
                    message = await channel.fetch_message(int(i.message_id))
                    await message.edit(content = 'qr đã hết hạn', embed=None)
    
    async def get_bank_history(self):
        from_day = datetime.datetime.now()
        an = os.getenv('BANK_USER_NAME')
        if (an is None):
            logger.error('không có BANK_USER_NAME')
            sys.exit(0)
            
        history = await self.mb.getTransactionAccountHistory(accountNo=an, from_date=from_day - datetime.timedelta(days=2), to_date=from_day)
        for i in history['transactionHistoryList']:
            i: dict
            transaction_id = i.get('refNo', '')
            transactionDate = i.get('transactionDate', '')
            creditAmount = int(i.get('creditAmount', ''))
            currency = i.get('currency', '')
            description : str = i.get('description', '')
            
            transaction_history_bll = TransactionHistoryBLL()
            qr_pay_code_bll = QrPayCodeBLL()
            user_premium_bll = UserPremiumBLL()
            premium_bll = PremiumBLL()
            
            for qrcode in re.findall("T\\d{20}T" , description.replace(' ', '').upper()):
                qr = qr_pay_code_bll.get_qr_pay_code_by_qr_code(qrcode.replace("T", ""))
                
                
                if qr is None:
                    continue
                
                # NOTE lưu những dao dịnh đã được sử lý
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
                
                # NOTE sác nhận là qr được chuyển tiền thành công
                qr.is_success = True
                qr_pay_code_bll.insert_qr_pay_code(qr)
                 
            
                await self.pay_success(qr)
    
    async def pay_success(self, qr: QrPayCodeDTO):
        channel = self.bot.get_channel(int(qr.channel_id))

        if (channel is None): 
            logger.warning('không tìm thấy channel')
            return
        
        if isinstance(channel, TextChannel):
            message = await channel.fetch_message(int(qr.message_id))
            await message.edit(content = 'Thanh toán thành công', embed=None)
                         
    @tasks.loop(seconds=30)
    async def start_listener_bank_history(self):
        # thời gian lấy lịch sử
        # chỉ khi có giao dịch sảu ra mới lấy lịch sử
        # tôi để 5p
        if datetime.datetime.now() - self.start_time > datetime.timedelta(minutes=5):
            self.start_listener_bank_history.stop()
        
        # print('aaaaaaaaaaaaa')
        await self.get_bank_history() 

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('check qr code start')
        if not self.check_qr_code.is_running():
            self.check_qr_code.start()
              
    @commands.command(name="premium")
    async def pay(self, ctx: Context):
        # if await self.is_dm_channel(ctx): 
        #     return
        
        # if not await self.is_server_owner(ctx=ctx):
        #     return
        
        embed_text = EmbedCustom(
        id_server=str(ctx.guild.id) if ctx.guild else "DM",
        title="Nạp để mở gói premium",
        description="Gói premium mang đến nhiều tính năng hơn. ở đây là một số gói cơ bản:")
        
        premium_bll = PremiumBLL()
        
        
        
        buttons = View()
        
        cls = self
        
        class goiButton(Button):
            def __init__(self, pre: PremiumDTO):
                super().__init__(label=pre.get_premium_name())
                self.pre = pre
                
            async def callback(self, interaction: Interaction):
                
                embed_text = EmbedCustom(
                    id_server=str(ctx.guild.id) if ctx.guild else "DM",
                    title="Nạp để mở gói premium",
                    description="Gói premium mang đến nhiều tính năng hơn")



                embed_text.add_field(name="Ngân hàng MB-Bank", value=os.getenv('BANK_USER_NAME'), inline=False)
                embed_text.add_field(name="Số Tiền:", value=f"{self.pre.get_price()}đ", inline=False)

                if (ctx.guild is None or ctx.channel is None):
                    await ctx.send('có gì đó lạ lắm')
                    return
                
                qr_id = QRGenerator.generator_id()
                embed_text.add_field(name="Nội dung:", value=f"T{qr_id}T", inline=False)
                
                embed_text.set_image(QRGenerator.generator_qr(qr_id))
                message = await interaction.edit(content='', embed=embed_text, view=None)
                
                if message is None:
                    await ctx.send('có gì đó lạ lắm')
                    return
                qr = QrPayCodeDTO(qr_id, str(ctx.author.id), str(message.channel.id), self.pre.get_premium_id(), str(message.id), datetime.datetime.now(), False)
                
                qr_pay_code_bll = QrPayCodeBLL()
                qr_pay_code_bll.insert_qr_pay_code(qr)
                if not cls.start_listener_bank_history.is_running():
                    cls.start_listener_bank_history.start()
                cls.start_time = datetime.datetime.now()
                
        
        for index, pre in enumerate(premium_bll.get_all_premiums()):
            embed_text.add_field(name=pre.get_premium_name(), value=f"""{pre.get_description()}\ngiá: {pre.get_price()}\nthời hạn: {pre.get_duration()}""", inline=False)
                    
            buttons.add_item(goiButton(pre))
        
        await ctx.send(embed=embed_text, view=buttons)
        

async def setup(bot: commands.Bot):
    # NOTE: add_cog là một funstion bình thường không phải là async funstion
    bot.add_cog(CommandPaying(bot))