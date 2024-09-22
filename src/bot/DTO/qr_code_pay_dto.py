from attr import dataclass
from datetime import datetime


@dataclass
class QrPayCodeDTO:
    qr_code: str
    user_id: str
    channel_id: str
    premium_id: str
    message_id: str
    date_created: datetime
    is_success: bool