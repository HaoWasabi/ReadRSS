from ..BLL.user_premium_bll import UserPremiumBLL
from ..BLL.user_premium_bll import UserPremiumBLL


def check_have_premium(user_id: str) -> bool:
    user_premium_bll = UserPremiumBLL()
    list_user_premium_dto = user_premium_bll.get_all_userpremiums_by_user_id(user_id)
    return False if list_user_premium_dto == [] else True