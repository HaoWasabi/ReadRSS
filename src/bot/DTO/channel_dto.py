from types import NotImplementedType
from attr import dataclass

from .color_dto import ColorDTO


@dataclass
class ChannelDTO:
    channel_id: str
    server_id: str
    channel_name: str
    is_active: bool = True
