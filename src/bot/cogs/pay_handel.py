import datetime
import sys
import re
from discord import ChannelType, Embed, TextChannel
import logging, mbbank, os
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.ext.commands import Context

from ..BLL.server_pay_bll import ServerPayBLL
from ..DTO.server_pay_dto import ServerPayDTO

from ..DTO.transaction_history_dto import TransactionHistoryDTO
from ..DAL.transaction_history_dal import TransactionHistoryDAL
from ..DTO.qr_code_pay_dto import QrPayCodeDTO
from ..utils.create_qr_payment import QRGenerator

from .check_dm_channel import check_dm_channel
from ..BLL.qr_pay_code_bll import QrPayCodeBLL

# file này chỉ chuyên sử lý qr code và chuyển khoản mà thôi

logger = logging.getLogger('paying')

class Paying(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mb = mbbank.MBBankAsync( username=os.getenv('BANK_USER_NAME'), password=os.getenv('BANK_PASSWORD'))
        self.start_time: datetime.datetime = datetime.datetime.now()
        
    async def cog_check(self, ctx):
        if check_dm_channel(ctx):
            await ctx.send("You can't use this command in DM.")
            return False
        return True

    def is_server_owner(self, ctx):
        return ctx.author.id == ctx.guild.owner_id
        
    @tasks.loop(seconds=5)
    async def check_qr_code(self):
        qr_pay_code_bll = QrPayCodeBLL()
        all_qr = qr_pay_code_bll.get_all_qr_pay_code()
        for i in all_qr:
            denta = datetime.datetime.now() - i.get_ngay_tao()
            # kiểm tra hết hạng của mã qr
            # ở đây tôi để 3p
            if (denta > datetime.timedelta(minutes=3)):
                qr_pay_code_bll.delete_qr_pay_by_id(i.get_qr_code())
                channel = self.bot.get_channel(int(i.get_channel_id()))
                
                if (channel is None): 
                    logger.warning('không tìm thấy channel')
                    return
                
                if isinstance(channel, TextChannel):
                    message = await channel.fetch_message(int(i.get_message_id()))
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
            
            transaction_history_dal = TransactionHistoryDAL()
            qr_pay_code_dal = QrPayCodeBLL()
            server_pay = ServerPayBLL()
            transaction = transaction_history_dal.get_transaction_history_by_id(transaction_id)
            
            if transaction is None:
                transaction_history_dto = TransactionHistoryDTO(transaction_id, datetime.datetime.strptime(transactionDate, '%d/%m/%Y %H:%M:%S'), description, creditAmount, currency)
                transaction_history_dal.insert_transaction_history(transaction_history_dto)
                
                for j in re.findall("T\\d{20}T" , description.replace(' ', '').upper()):
                    qr = qr_pay_code_dal.get_qr_pay_code_by_qr_code(j.replace("T", ""))
                    if qr is None:
                        continue
                    
                    
                    server_pay.insert_server_pay(ServerPayDTO(qr.get_id_server(), True))
                    channel = self.bot.get_channel(int(qr.get_channel_id()))

                    if (channel is None): 
                        logger.warning('không tìm thấy channel')
                        return
                    
                    if isinstance(channel, TextChannel):
                        message = await channel.fetch_message(int(qr.get_message_id()))
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
              
    @commands.command(name="pay")
    async def pay(self, ctx: Context):
        if not await self.cog_check(ctx): return
        if not self.is_server_owner(ctx):
            await ctx.send("You need to be the server owner to use this command.")
            return
        
        embed_text = Embed(title="Thanh toán đi bạn trẻ")
        embed_text.add_field(name="Ngân hàng MB-Bank", value="0347402306", inline=False)
        embed_text.add_field(name="Số Tiền:", value="10k", inline=False)

        if (ctx.guild is None or ctx.channel is None):
            await ctx.send('có gì đó lạ lắm')
            return
        
        
        qr_id = QRGenerator.generator_id(str(ctx.guild.id))
        embed_text.add_field(name="Nội dung:", value=f"T{qr_id}T", inline=False)
        
        embed_text.set_image(QRGenerator.generator_qr(qr_id))
        message = await ctx.send(embed=embed_text)
        
        
        qr = QrPayCodeDTO(qr_id, str(ctx.guild.id), str(ctx.channel.id), str(message.id), datetime.datetime.now())
        
        qr_pay_code_bll = QrPayCodeBLL()
        qr_pay_code_bll.insert_qr_pay_code(qr)
        if not self.start_listener_bank_history.is_running():
            self.start_listener_bank_history.start()
        self.start_time: datetime.datetime = datetime.datetime.now()
            
async def setup(bot: commands.Bot):
    # NOTE: add_cog là một funstion bình thường không phải là async funstion
    bot.add_cog(Paying(bot))