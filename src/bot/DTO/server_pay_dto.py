from types import NotImplementedType

from attr import dataclass
from .server_dto import ServerDTO


@dataclass
class ServerPayDTO:
    server_dto: str
    is_pay: bool
