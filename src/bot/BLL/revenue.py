from datetime import datetime
from bot.BLL import transaction_history_bll
from bot.BLL.premium_bll import PremiumBLL
from bot.BLL.qr_pay_code_bll import QrPayCodeBLL
from bot.BLL.transaction_history_bll import TransactionHistoryBLL


class Revenue:
    def __init__(self):
        self.__transaction_history_bll = TransactionHistoryBLL()
        self.__qr_paycode_bll = QrPayCodeBLL()
        self.__premium_bll = PremiumBLL()
    
    def get_total_revenue(self) -> float:
        transaction_history_list = self.__transaction_history_bll.get_all_transaction_history()
        total = 0.0
        
        for transaction in transaction_history_list:
            total += float(transaction.credit_amount)
            
        return total

    def get_total_revenue_by_year(self, year: int, premium_id: str = None) -> float: #type:ignore
        qr_paycode_list = self.__qr_paycode_bll.get_all_qr_pay_code()
        transaction_history_list = self.__transaction_history_bll.get_all_transaction_history()
        total = 0.0
        
        for transaction in transaction_history_list:
            transaction_date = transaction.transaction_date
            if transaction_date.year == year:
                if premium_id:
                    matching_qr_paycode = next((qr for qr in qr_paycode_list if qr.qr_code == transaction.qr_code), None)
                    if matching_qr_paycode and matching_qr_paycode.premium_id == premium_id:
                        total += float(transaction.credit_amount)
                else:
                    total += float(transaction.credit_amount)
        
        return total
    
    def get_total_revenue_between_dates(self, start_date: datetime, end_date: datetime, premium_id: str = None) -> float: #type:ignore
        qr_paycode_list = self.__qr_paycode_bll.get_all_qr_pay_code()
        transaction_history_list = self.__transaction_history_bll.get_all_transaction_history()
        total = 0.0

        for transaction in transaction_history_list:
            transaction_date = transaction.transaction_date
            
            if start_date <= transaction_date <= end_date:
                if premium_id:
                    matching_qr_paycode = next((qr for qr in qr_paycode_list if qr.qr_code == transaction.qr_code), None)
                    if matching_qr_paycode and matching_qr_paycode.premium_id == premium_id:
                        total += float(transaction.credit_amount)
                else:
                    total += float(transaction.credit_amount)
        
        return total
    
    def get_total_revenue_by_quarter(self, year: int, quarter: int, premium_id: str = None) -> float: #type:ignore
        qr_paycode_list = self.__qr_paycode_bll.get_all_qr_pay_code()
        transaction_history_list = self.__transaction_history_bll.get_all_transaction_history()
        total = 0.0
        
        if quarter == 1:
            start_month, end_month = 1, 3
        elif quarter == 2:
            start_month, end_month = 4, 6
        elif quarter == 3:
            start_month, end_month = 7, 9
        elif quarter == 4:
            start_month, end_month = 10, 12
        else:
            raise ValueError("Quý không hợp lệ. Quý từ 1 đến 4.")

        for transaction in transaction_history_list:
            transaction_date = transaction.transaction_date
            
            if transaction_date.year == year and start_month <= transaction_date.month <= end_month:
                if premium_id:
                    matching_qr_paycode = next((qr for qr in qr_paycode_list if qr.qr_code == transaction.qr_code), None)
                    if matching_qr_paycode and matching_qr_paycode.premium_id == premium_id:
                        total += float(transaction.credit_amount)
                else:
                    total += float(transaction.credit_amount)

        return total
    
