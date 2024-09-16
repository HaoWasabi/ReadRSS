import asyncio
import datetime
import sys
import re
from tabnanny import check
from typing import Callable
from venv import logger
from nextcord import TextChannel
import logging, mbbank, os
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.ext.commands import Context

from ..DTO.server_pay_dto import ServerPayDTO
from ..DTO.transaction_history_dto import TransactionHistoryDTO
from ..DTO.qr_code_pay_dto import QrPayCodeDTO

from ..DAL.transaction_history_dal import TransactionHistoryDAL

from ..BLL.server_pay_bll import ServerPayBLL
from ..BLL.qr_pay_code_bll import QrPayCodeBLL


logger = logging.getLogger('bank_hander')


QR_TIME_OUT = datetime.timedelta(minutes=3)
BANK_HISTORY_DURATION = datetime.timedelta(minutes=5)


class PayHandle(commands.Cog):
    
    '''
    thêm 2 event mới
        + on_qr_time_out arg QrPayCodeDTO
        + on_payment_success arg QrPayCodeDTO
    '''

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot;
        
        if (os.getenv('BANK_USER_NAME') is None or os.getenv('BANK_PASSWORD') is None):
            logger.error('thiếu tên đăng nhập và mật khẩu Mbank')
            exit(0)
        self.mb = mbbank.MBBankAsync( username=os.getenv('BANK_USER_NAME'), password=os.getenv('BANK_PASSWORD'))
        self.start_time: datetime.datetime = datetime.datetime.now()
        self.payment_success_callback = []
        self.qr_time_out_callback = []
               
    @tasks.loop(seconds=5)
    async def check_qr_code(self):
        qr_pay_code_bll = QrPayCodeBLL()
        all_qr = qr_pay_code_bll.get_all_qr_pay_code()
        for i in all_qr:
            denta = datetime.datetime.now() - i.get_ngay_tao()
            # kiểm tra hết hạng của mã qr
            # ở đây tôi để 3p
            if (denta > QR_TIME_OUT):
                qr_pay_code_bll.delete_qr_pay_by_id(i.get_qr_code())
                
                await self.__qr_trigger(i)
                
                
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
                    
                    server_pay_dto = ServerPayDTO(qr.get_id_server(), True)
                    server_pay.insert_server_pay(server_pay_dto)
                    
                    await self.__payment_trigger(qr)
    
    @tasks.loop(seconds=30)
    async def __start_listener_bank_history(self):
        # thời gian lấy lịch sử
        # chỉ khi có giao dịch sảu ra mới lấy lịch sử
        # tôi để 5p
        if datetime.datetime.now() - self.start_time > BANK_HISTORY_DURATION:
            self.__start_listener_bank_history.stop()
        
        # print('aaaaaaaaaaaaa')
        await self.get_bank_history() 
        
    # def payment_success(self, fun: Callable[[QrPayCodeDTO], None]):
    #     self.payment_success_callback.append(fun)
    #     return fun
    
    # def qr_time_out(self, fun):
    #     self.qr_time_out_callback.append(fun)
    #     return fun
        
        
    async def __qr_trigger(self, qr: QrPayCodeDTO):
        self.bot.dispatch('qr_time_out', qr)
    
    
    async def __payment_trigger(self, qr: QrPayCodeDTO):
        self.bot.dispatch('payment_success', qr)
        
    @staticmethod
    def start_listener_bank_history(bot: commands.Bot):
        bot.dispatch('start_listener_bank_history')
    
    
    @commands.Cog.listener()
    async def on_start_listener_bank_history(self):
        if not self.__start_listener_bank_history.is_running():
            self.__start_listener_bank_history.start()
        self.start_time: datetime.datetime = datetime.datetime.now()
        
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('check qr code start')
        if not self.check_qr_code.is_running():
            self.check_qr_code.start()
            

async def setup(bot: commands.Bot):
    # NOTE: add_cog là một funstion bình thường không phải là async funstion
    bot.add_cog(PayHandle(bot))