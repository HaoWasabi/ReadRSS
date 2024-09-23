from datetime import datetime

from attr import dataclass
from ..DTO.channel_dto import ChannelDTO
from ..DTO.user_dto import UserDTO


@dataclass
class UserChannelDTO:
    user: UserDTO
    channel: ChannelDTO
    date: datetime
