

from datetime import datetime
from types import NotImplementedType

from attr import dataclass

@dataclass
class TransactionHistoryDTO:
    id_transaction: str
    qr_code: str
    transaction_date: datetime
    content: str
    currency: int
    credit_amount: str