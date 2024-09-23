
from attr import dataclass


@dataclass
class ServerDTO:
    server_id: str
    server_name: str
    hex_color: str = "0x3498DB"
    is_active: bool = True
