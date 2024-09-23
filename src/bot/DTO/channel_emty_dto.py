from attr import dataclass
from ..DTO.channel_dto import ChannelDTO
from ..DTO.emty_dto import EmtyDTO
from types import NotImplementedType


@dataclass
class ChannelEmtyDTO:
    channel_dto: ChannelDTO
    emty_dto: EmtyDTO
