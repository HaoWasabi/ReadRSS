# from typing import List

# from ..BLL.singleton import Singleton
# from ..DAL.user_channel_dal import UserChannelDAL
# from ..DTO.user_channel_dto import UserChannelDTO


# class UserChannelBLL(Singleton):
#     def __init__(self):
#         if not hasattr(self, '_initialized'):
#             self.__userchannelDAL = UserChannelDAL()
#             self._initialized = True
            
#     def insert_user_channel(self, userchannel_dto: UserChannelDTO) -> bool:
#         return self.__userchannelDAL.insert_user_channel(userchannel_dto)
    
#     def get_all_user_channel(self) -> List[UserChannelDTO]:
#         return self.__userchannelDAL.get_all_user_channel()
    
#     def get_all_user_channel_by_user_id(self, user_id: str) -> List[UserChannelDTO]:
#         return self.__userchannelDAL.get_all_user_channel_by_user_id(user_id)
    
#     def get_all_user_channel_by_channel_id(self, channel_id: str) -> List[UserChannelDTO]:
#         return self.__userchannelDAL.get_all_user_channel_by_channel_id(channel_id)
    
#     def delete_user_channel_by_user_id_and_channel_id(self, user_id: str, channel_id: str) -> bool:
#         return self.__userchannelDAL.delete_user_channel_by_user_id_and_channel_id(user_id, channel_id)