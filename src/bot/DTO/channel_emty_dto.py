# from ..DTO.channel_dto import ChannelDTO
# from ..DTO.emty_dto import EmtyDTO
# from types import NotImplementedType

# class ChannelEmtyDTO:
#     def __init__(self, channel_dto: ChannelDTO, emty_dto: EmtyDTO):
#         self.__channel_dto = channel_dto
#         self.__emty_dto = emty_dto
    
#     def __str__(self) -> str:
#         return f"ChannelEmtyDTO(channel={self.__channel_dto}, emty={self.__emty_dto})"
    
#     def __eq__(self, other: object) -> bool:
#         if not isinstance(other, ChannelEmtyDTO):
#             return NotImplementedType
#         return self.__channel_dto == other.__channel_dto and self.__emty_dto == other.__emty_dto
    
#     def set_channel(self, channel_dto: ChannelDTO) -> None:
#         self.__channel_dto = channel_dto
        
#     def set_emty(self, emty_dto: EmtyDTO) -> None:
#         self.__emty_dto = emty_dto
        
#     def get_channel(self) -> ChannelDTO:
#         return self.__channel_dto
    
#     def get_emty(self) -> EmtyDTO:
#         return self.__emty_dto
    