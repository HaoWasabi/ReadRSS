from datetime import datetime
from tokenize import Double
from typing import Optional

from attr import dataclass


@dataclass
class PremiumDTO:
    premium_id: str
    premium_name: str
    description: str
    price: float
    date_created: datetime
    duration: int
    is_active: bool
