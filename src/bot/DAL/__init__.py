from .base_dal import BaseDAL

from .channel_dal import *
from .channel_emty_dal import *
from .channel_feed_dal import *
from .emty_dal import *
from .feed_dal import *
from .feed_emty_dal import *
from .qr_pay_code_dal import *
from .server_channel_dal import *
from .server_color_dal import *
from .server_dal import *
from .server_pay_dal import *
from .transaction_history_dal import *

# một hàm nào đó tôi tìm được trên mạng
# lấy toàn bộ các supclass
def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses

# Tạo toàn bộ database
for i in inheritors(BaseDAL):
    baseDAL: BaseDAL = i()
    baseDAL.create_table()
    

dm_dto = ServerDTO("DM", "DM")
color_dto = ColorDTO("blue")
server_bll = ServerDAL()
server_color_bll = ServerColorDAL()

if (server_bll.get_server_by_id_server(dm_dto.get_id_server()) is None):
    server_bll.insert_server(dm_dto)
    server_color_bll.insert_server_color(ServerColorDTO(dm_dto, color_dto))