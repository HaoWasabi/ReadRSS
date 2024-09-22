from attr import dataclass
from datetime import datetime


@dataclass
class QrPayCodeDTO:
    qr_code: str
    user_id: str
    channel_id: str
    premium_id: str
    message_id: str
    is_success: bool
    date_created: datetime