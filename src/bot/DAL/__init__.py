from datetime import datetime
from .base_dal import BaseDAL

from .channel_dal import *
from .channel_feed_dal import *
from .emty_dal import *
from .feed_dal import *
from .qr_pay_code_dal import *
from .server_dal import *
from .server_pay_dal import *
from .transaction_history_dal import *
from .premium_dal import *

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
    
# PremiumDAL().insert_premium(PremiumDTO('1', 'gói 1', 'gói cơ bản', 10000, datetime.now(), 2, True))
# PremiumDAL().insert_premium(PremiumDTO('2', 'gói 2', 'gói cơ bản', 20000, datetime.now(), 2, True))
# PremiumDAL().insert_premium(PremiumDTO('3', 'gói 3', 'gói cơ bản', 30000, datetime.now(), 2, True))