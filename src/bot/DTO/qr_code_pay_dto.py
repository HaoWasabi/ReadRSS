from types import NotImplementedType
from .server_dto import ServerDTO
from datetime import datetime


class QrPayCodeDTO:
    def __init__(self, qr_code: str, id_server: str, channel_id: str, message_id: str, ngay_tao: datetime):
        self.__qr_code = qr_code
        self.__id_server = id_server
        self.__channel_id = channel_id
        self.__message_id = message_id
        self.__ngay_tao = ngay_tao

    def __str__(self) -> str:
        return f"QrPayCodeDTO(qr_code={self.__qr_code} id_server={self.__id_server} channel_id={self.__channel_id} message_id={self.__message_id} ngay_tao={self.__ngay_tao})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QrPayCodeDTO):
            return NotImplementedType
        return self.__qr_code == other.__qr_code and \
               self.__id_server == other.__id_server and \
               self.__channel_id == other.__channel_id and \
               self.__message_id == other.__message_id and \
               self.__ngay_tao == other.__ngay_tao
            
    def get_qr_code(self):
        return self.__qr_code
    def get_id_server(self):
        return self.__id_server
    def get_channel_id(self):
        return self.__channel_id
    def get_message_id(self):
        return self.__message_id
    def get_ngay_tao(self):
        return self.__ngay_tao
    
    def set_qr_code(self, qr_code: str):
        self.__qr_code = qr_code
    def set_id_server(self, id_server: str):
        self.__id_server = id_server
    def set_channel_id(self, channel_id: str):
        self.__channel_id = channel_id
    def set_message_id(self, message_id: str):
        self.__message_id = message_id
    def set_ngay_tao(self, ngay_tao: datetime):
        self.__ngay_tao = ngay_tao