from calendar import c
import nextcord
import datetime
import sys
import re
from nextcord import ChannelType, Embed, TextChannel
import logging, mbbank, os
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord import Interaction

from ..DTO.server_pay_dto import ServerPayDTO
from ..DTO.transaction_history_dto import TransactionHistoryDTO
from ..DTO.qr_code_pay_dto import QrPayCodeDTO

from ..DAL.transaction_history_dal import TransactionHistoryDAL

from ..BLL.server_pay_bll import ServerPayBLL
from ..BLL.qr_pay_code_bll import QrPayCodeBLL

from ..GUI.custom_embed import CustomEmbed

from ..utils.create_qr_payment import QRGenerator
from ..utils.check_cogs import CheckCogs

# file này chỉ chuyên sử lý qr code và chuyển khoản mà thôi

logger = logging.getLogger('paying')

class SlashCommandPaying(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mb = mbbank.MBBankAsync( username=os.getenv('BANK_USER_NAME'), password=os.getenv('BANK_PASSWORD'))
        self.start_time: datetime.datetime = datetime.datetime.now()
        
    async def is_dm_channel(self, interaction: Interaction):
        if await CheckCogs.is_dm_channel(interaction):
            await interaction.followup.send("Can not send DMChannels") # type: ignore
            return True
        else: 
            return False
        
    async def is_owner_server(self, interaction: Interaction):
        if await CheckCogs.is_server_owner(interaction=interaction):
            return True
        else:
            await interaction.followup.send("You need to be the server owner to use this command.")
            return False
    
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
                    
                    await self.pay_success(qr)
    
    async def pay_success(self, qr: QrPayCodeDTO):
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

    @nextcord.slash_command(name="premium", description="Upgrade to use advanced packages")
    async def pay(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            if await self.is_dm_channel(interaction): 
                return
            
            if not await self.is_owner_server(interaction): 
                return
            
            embed_text = CustomEmbed(
                id_server=str(interaction.guild.id) if interaction.guild else "DM",
                title="Nạp mở để gói premium",
                description="Gói premium mang đến nhiều tính năng hơn.",)
            embed_text.add_field(name="Ngân hàng MB-Bank", value=os.getenv('BANK_USER_NAME'), inline=False)
            embed_text.add_field(name="Số Tiền:", value="10k", inline=False)

            if (interaction.guild is None or interaction.channel is None):
                await interaction.followup.send('có gì đó lạ lắm', ephemeral=True)
                return
            
            qr_id = QRGenerator.generator_id(str(interaction.guild.id))
            embed_text.add_field(name="Nội dung:", value=f"T{qr_id}T", inline=False)
            
            embed_text.set_image(QRGenerator.generator_qr(qr_id))
            message = await interaction.followup.send(embed=embed_text, ephemeral=True)
            
            qr = QrPayCodeDTO(qr_id, str(interaction.guild.id), str(interaction.channel.id), str(message.id), datetime.datetime.now()) # type: ignore
            
            qr_pay_code_bll = QrPayCodeBLL()
            qr_pay_code_bll.insert_qr_pay_code(qr)
            if not self.start_listener_bank_history.is_running():
                self.start_listener_bank_history.start()
            self.start_time: datetime.datetime = datetime.datetime.now()
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            print(f"Error: {e}")
            
async def setup(bot: commands.Bot):
    # NOTE: add_cog là một funstion bình thường không phải là async funstion
    bot.add_cog(SlashCommandPaying(bot))