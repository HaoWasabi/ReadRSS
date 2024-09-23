from datetime import datetime
from typing import Optional
from attr import dataclass


@dataclass
class EmtyDTO:
    link_emty: str
    link_feed: str
    link_atom_feed: str
    title_emty: str
    description_emty: str
    image_emty: str
    pubdate_emty: datetime
    channel_id: Optional[str] = None
