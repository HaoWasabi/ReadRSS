# import datetime
# from bot.DTO.feed_dto import FeedDTO
# from bot.DTO.emty_dto import EmtyDTO
# from bot.DTO.color_dto import ColorDTO
# from bot.DTO.channel_dto import ChannelDTO
# from bot.DTO.server_dto import ServerDTO
# from bot.DTO.feed_emty_dto import FeedEmtyDTO
# from bot.DTO.channel_emty_dto import ChannelEmtyDTO
# from bot.DTO.channel_feed_dto import ChannelFeedDTO
# from bot.DTO.server_channel_dto import ServerChannelDTO
from datetime import datetime
from bot.DAL.premium_dal import PremiumDAL
from bot.DTO.premium_dto import PremiumDTO
from bot.DTO.server_dto import ServerDTO
# from bot.DTO.server_color_dto import ServerColorDTO
# from bot.BLL.feed_bll import FeedBLL
from bot.BLL.emty_bll import EmtyBLL
from bot.DTO.emty_dto import EmtyDTO
# from bot.BLL.feed_emty_bll import FeedEmtyBLL
from bot.BLL.server_bll import ServerBLL
# from bot.BLL.channel_bll import ChannelBLL
# from bot.BLL.channel_emty_bll import ChannelEmtyBLL
# from bot.BLL.channel_feed_bll import ChannelFeedBLL
# from bot.BLL.server_channel_bll import ServerChannelBLL
# from bot.BLL.server_color_bll import ServerColorBLL
# from bot.GUI.feed_embed import FeedEmbed
# from bot.utils.read_rss import ReadRSS
# from bot.utils.text_processor import TextProcessor
# from bot.DAL.server_pay_dal import ServerPayDAL
# from bot.DTO.server_pay_dto import ServerPayDTO
# from bot.DAL.qr_pay_code_dal import QrPayCodeDAL
# from bot.DTO.qr_code_pay_dto import QrPayCodeDTO
# from bot.DTO.transaction_history_dto import TransactionHistoryDTO
# from bot.DAL.transaction_history_dal import TransactionHistoryDAL

def test_feed_emty():
    print ('''
           -- TEST FEED_EMTY --
           ''')
    # feedEmtyBLL = FeedEmtyBLL()
    # feedBLL = FeedBLL()
    # emtyBLL = EmtyBLL()
    # emtyBLL.delete_all_emty()
    
    # feedDTO = FeedDTO("a", "a", "a", "a", "a", "a". )
    # feedBLL.insert_feed(feedDTO)
    
    # emtyDTO = EmtyDTO("a", "a", "a", "a", "a", "a", "a")
    # emtyBLL.insert_emty(emtyDTO)
    
    # feedEmtyBLL.insert_feed_emty(FeedEmtyDTO(feedDTO, emtyDTO))
    
    # try:
        # print(feedEmtyBLL.get_feed_emty_by_link_atom_feed_and_link_emty("a", "a"))
           
        # emtyDTO.set_pubdate_emty("m")
        # print(emtyDTO)
        # emtyBLL.update_emty_by_link_emty("a", emtyDTO)
    
        # print("\nLIST FEED_EMTY DTO GET ALL FEED EMTY: BEGIN - - - -")
        # for i in feedEmtyBLL.get_all_feed_emty(): 
        #     print(i)
        # print("FINSH - - - - - - - - - - ")
        
        # print("\nLIST FEED_EMTY DTO GET ALL FEED EMTY BY LINK FEED: BEGIN - - - -")
        # for i in feedEmtyBLL.get_all_feed_emty_by_link_feed("a"): 
        #     print(i)
        # print("FINSH - - - - - - - - - - ")
        # feedEmtyBLL.delete_all_feed_emty()
        # feedBLL.delete_all_feed()

    # except Exception as e:
    #     print(f"Một lỗi đã xảy ra: {e}")

# def test_channel_emty():
#     print ('''
#            -- TEST CHANNEL_EMTY --
#            ''')
#     channelEmtyBLL = ChannelEmtyBLL()
#     channelBLL = ChannelBLL()
#     emtyBLL = EmtyBLL()
    
#     channelDTO = ChannelDTO("a", "a")
#     channelBLL.insert_channel(channelDTO)
    
#     emtyDTO = EmtyDTO("a", "a", "a", "a", "a")
#     emtyBLL.insert_emty(emtyDTO)
    
#     channelEmtyBLL.insert_channel_emty(ChannelEmtyDTO(channelDTO, emtyDTO))
    
#     try:
#         print(channelEmtyBLL.get_channel_emty_by_id_channel_and_link_emty("a", "a"))
    
#         emtyDTO.set_pubdate_emty("m")
#         print(emtyDTO)
#         emtyBLL.update_emty_by_link_emty("a", emtyDTO)
    
#         print("\nLIST CHANNEL_EMTY DTO: BEGIN - - - -")
#         results = channelEmtyBLL.get_all_channel_emty()
#         if results:
#             for i in results: 
#                 print(i)
#             print("FINSH - - - - - - - - - - ")
#         else:
#             print("No data found for getAllChannelEmty.")
#     except Exception as e:
#         print(f"Một lỗi đã xảy ra: {e}")

# def test_server_channel():
#     print ('''
#            -- TEST SERVER_CHANNEL --
#            ''')
#     serverChannelBLL = ServerChannelBLL()
#     serverBLL = ServerBLL()
#     channelBLL = ChannelBLL()
    
#     serverDTO = ServerDTO("DM", "DM")
#     serverBLL.insert_server(serverDTO)
    
#     channelDTO = ChannelDTO("a", "a")
#     channelBLL.insert_channel(channelDTO)
    
#     serverChannelBLL.insert_server_channel(ServerChannelDTO(serverDTO, channelDTO))
    
#     try:
#         print(serverChannelBLL.get_server_channel_by_id_server_and_id_channel("a", "a"))

#         channelDTO.set_name_channel("b")
#         print(channelDTO)
#         channelBLL.update_channel_by_id_channel("a", channelDTO)
        
#         print("\nLIST SERVER_CHANNEL DTO: BEGIN - - - -")
#         results = serverChannelBLL.get_all_server_channel()
#         if results:
#             for i in results:
#                 print(i)
#             print("FINSH - - - - - - - - - - ")
#         else:
#             print("No data found for getAllServerChannel.")
#     except Exception as e:
#         print(f"Một lỗi không xảy ra: {e}")
        
# def test_channel_feed():   
#     print ('''
#            -- TEST CHANNEL_FEED --
#            ''')
#     channelFeedBLL = ChannelFeedBLL()
#     channelBLL = ChannelBLL()
#     feedBLL = FeedBLL()
    
#     channelDTO = ChannelDTO("a", "a")
#     channelBLL.insert_channel(channelDTO)
    
#     feedDTO = FeedDTO("a", "a", "a", "a", "a", "a")
#     feedBLL.insert_feed(feedDTO)
    
#     channelFeedDTO = ChannelFeedDTO(channelDTO, feedDTO)
#     print(channelFeedDTO)
#     channelFeedBLL.insert_channel_feed(channelFeedDTO)
    
#     try:
#         print(channelFeedBLL.get_channel_feed_by_id_channel_and_link_atom_feed("a", "a"))
        
#         feedDTO.set_description_feed("b")
#         feedBLL.update_feed_by_link_atom_feed("a", feedDTO)
        
#         print("\nLIST CHANNEL_FEED DTO: BEGIN - - - -")
#         results = channelFeedBLL.get_all_channel_feed()    
#         if results:
#             for i in results:
#                 print(i)
#             print("FINSH - - - - - - - - - - ")
#         else:
#             print("No data found for getAllChannelFeed.")
#     except Exception as e:
#         print(f"Một lỗi không xảy ra: {e}")

# def test_server_color():
#     print ('''
#            -- TEST SERVER_COLOR --
#            ''')
    serverBLL = ServerBLL()
    serverDTO = ServerDTO("DM", "DM")
    serverBLL.insert_server(serverDTO)
    
#     colorDTO = ColorDTO("blue")
#     serverColorDTO = ServerColorDTO(serverDTO, colorDTO)
#     print(serverDTO)
#     print(colorDTO)
#     print(serverColorDTO)
    
#     serverColorBLL = ServerColorBLL()
#     # serverColorBLL.delete_all_server_color()
#     serverColorBLL.insert_server_color(serverColorDTO)
    
#     try:
#         print(serverColorBLL.get_server_color_by_id_server("b"))
#         serverColorDTO.set_color(ColorDTO("YELLOW"))
#         serverColorBLL.update_server_color_by_id_server("b", serverColorDTO)
#         # serverColorBLL.delete_server_color_by_id_server("b")
        
#         print("\nLIST SERVER_COLOR DTO: BEGIN - - - -")
#         results = serverColorBLL.get_all_server_color()
#         if results:
#             for i in results:
#                 print(i)
#             print("FINSH - - - - - - - - - - ")
#         else:
#             print("No data found for getAllServerColor.")
#     except Exception as e:
#         print(f"Một lỗi không xảy ra: {e}")
        
# def test_read_rss():
#     link_atom_feed = input("Nhập link atom feed: ")
#     read_rss = ReadRSS(link_atom_feed)
#     print(read_rss.get_link_first_entry()) 
        
# def test_text_processor():
#     text_processor = TextProcessor() 
#     text = input("Nhập đoạn code chứa unicode escape: ")
#     text = text_processor.proccess_unicode_text(text)
#     print(text)
    
# def test_server_pay_dal():
#     a = ServerPayDAL()
#     print(a.get_all_server_pay())
#     try:
#         a.insert_server_pay(ServerPayDTO('1234', True))
#     except:
#         pass
#     print(a.get_all_server_pay())
#     print(a.get_server_pay_by_server_id('123456'))
    
#     print(a.delete_server_pay_by_id_server('1234'))
#     print(a.get_all_server_pay())
    
    
# def test_qr_pay_code():
#     a = QrPayCodeDAL()
#     print(a.get_all_qr_pay_code())
#     try:
#         print(a.insert_qr_pay_code(QrPayCodeDTO('12', '13', '12', '34', datetime.datetime.now())))
#     except:
#         pass
#     print(a.get_all_qr_pay_code())
#     print(a.delete_qr_pay_by_id('12'))
#     print(a.get_all_qr_pay_code())
    
# def test_():
#     a = TransactionHistoryDAL()
    
    
#     a.insert_transaction_history(TransactionHistoryDTO('1', datetime.datetime.now(), '', 1, ''))
#     print(a.get_transaction_history_by_id('1'))


# test_()
    
# test_qr_pay_code()
# test_server_pay_dal()
# test_server_color()
# test_feed_emty()
# PremiumDAL().insert_premium(PremiumDTO('1', 'gói 1', 'gói cơ bản', 10000, datetime.now(), 2, True))