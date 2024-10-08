

from .singleton import Singleton
from ..DTO.qr_code_pay_dto import QrPayCodeDTO
from ..DAL.qr_pay_code_dal import QrPayCodeDAL


class QrPayCodeBLL(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__QrPayCodeBLL = QrPayCodeDAL()
            self._initialized = True
            
    def get_qr_pay_code_by_qr_code(self, qr_code: str):
        return self.__QrPayCodeBLL.get_qr_pay_code_by_qr_code(qr_code)
    
    def get_all_qr_pay_code(self):
        return self.__QrPayCodeBLL.get_all_qr_pay_code()

    def insert_qr_pay_code(self, qr_pay: QrPayCodeDTO):
        return self.__QrPayCodeBLL.insert_qr_pay_code(qr_pay)

    def delete_qr_pay_by_id(self, qr_code: str):
        return self.__QrPayCodeBLL.delete_qr_pay_by_id(qr_code)