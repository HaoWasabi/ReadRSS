from types import NotImplementedType
from .server_dto import ServerDTO
from datetime import datetime

class QrPayCodeDTO:
    def __init__(self, qr_code: str, server_dto: ServerDTO, ngay_tao: datetime):
        self.__qr_code = qr_code
        self.__server_dto = server_dto
        self.__ngay_tao = ngay_tao
    
    def __str__(self) -> str:
        return f"QrPayCodeDTO(server={self.__server_dto}, qr_code={self.__qr_code})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QrPayCodeDTO):
            return NotImplementedType
        return self.__server_dto == other.__server_dto and self.__qr_code == other.__qr_code
    
    def set_server(self, channel_dto: ServerDTO) -> None:
        self.__server_dto = channel_dto
        
    def set_qr_code(self, qr_code: str) -> None:
        self.__qr_code = qr_code
        
    def get_server(self) -> ServerDTO:
        return self.__server_dto
    
    def get_qr_code(self) -> str:
        return self.__qr_code
    
    def get_ngay_tao(self):
        return self.__ngay_tao

    def set_ngay_tao(self, ngay_tao: datetime):
        self.__ngay_tao = ngay_tao
    