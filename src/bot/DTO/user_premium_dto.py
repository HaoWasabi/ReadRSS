from datetime import datetime

from attr import dataclass

from ..DTO.premium_dto import PremiumDTO
from ..DTO.user_dto import UserDTO


@dataclass
class UserPremiumDTO:
    user: UserDTO
    premium: PremiumDTO
    date_registered: datetime
