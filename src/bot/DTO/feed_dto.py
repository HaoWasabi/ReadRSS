from datetime import datetime
from types import NotImplementedType
from typing import Optional

from attr import dataclass


@dataclass
class FeedDTO:
    link_feed: str
    link_atom_feed: str
    title_feed: str
    description_feed: str
    logo_feed: str
    pubdate_feed: datetime
    channel_id: Optional[str] = None
