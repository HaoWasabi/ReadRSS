from bot.dto.feed_dto import FeedDTO
from bot.dto.emty_dto import EmtyDTO
from bot.dto.color_dto import ColorDTO
from bot.dto.channel_dto import ChannelDTO
from bot.dto.server_dto import ServerDTO
from bot.dto.feed_emty_dto import FeedEmtyDTO
from bot.dto.channel_emty_dto import ChannelEmtyDTO
from bot.dto.channel_feed_dto import ChannelFeedDTO
from bot.dto.server_channel_dto import ServerChannelDTO
from bot.dto.server_color_dto import ServerColorDTO
from bot.bll.feed_bll import FeedBLL
from bot.bll.emty_bll import EmtyBLL
from bot.bll.feed_emty_bll import FeedEmtyBLL
from bot.bll.server_bll import ServerBLL
from bot.bll.channel_bll import ChannelBLL
from bot.bll.channel_emty_bll import ChannelEmtyBLL
from bot.bll.channel_feed_bll import ChannelFeedBLL
from bot.bll.server_channel_bll import ServerChannelBLL
from bot.bll.server_color_bll import ServerColorBLL
from bot.gui.feed_embeb import FeedEmbed
from bot.utils.read_rss import ReadRSS

def test_feed_emty():
    print ('''
           -- TEST FEED_EMTY --
           ''')
    feedEmtyBLL = FeedEmtyBLL()
    feedBLL = FeedBLL()
    emtyBLL = EmtyBLL()
    
    feedDTO = FeedDTO("a", "a", "a", "a", "a", "a")
    feedBLL.insert_feed(feedDTO)
    
    emtyDTO = EmtyDTO("a", "a", "a", "a", "a")
    emtyBLL.insert_emty(emtyDTO)
    
    feedEmtyBLL.insert_feed_emty(FeedEmtyDTO(feedDTO, emtyDTO))
    
    try:
        print(feedEmtyBLL.get_feed_emty_by_link_atom_feed_and_link_emty("a", "a"))
           
        emtyDTO.set_pubdate_emty("m")
        print(emtyDTO)
        emtyBLL.update_emty_by_link_emty("a", emtyDTO)
    
        print("\nLIST FEED_EMTY DTO: BEGIN - - - -")
        for i in feedEmtyBLL.get_all_feed_emty(): 
            print(i)
        print("FINSH - - - - - - - - - - ")
    except Exception as e:
        print(f"Một lỗi đã xảy ra: {e}")

def test_channel_emty():
    print ('''
           -- TEST CHANNEL_EMTY --
           ''')
    channelEmtyBLL = ChannelEmtyBLL()
    channelBLL = ChannelBLL()
    emtyBLL = EmtyBLL()
    
    channelDTO = ChannelDTO("a", "a")
    channelBLL.insert_channel(channelDTO)
    
    emtyDTO = EmtyDTO("a", "a", "a", "a", "a")
    emtyBLL.insert_emty(emtyDTO)
    
    channelEmtyBLL.insert_channel_emty(ChannelEmtyDTO(channelDTO, emtyDTO))
    
    try:
        print(channelEmtyBLL.get_channel_emty_by_id_channel_and_link_emty("a", "a"))
    
        emtyDTO.set_pubdate_emty("m")
        print(emtyDTO)
        emtyBLL.update_emty_by_link_emty("a", emtyDTO)
    
        print("\nLIST CHANNEL_EMTY DTO: BEGIN - - - -")
        results = channelEmtyBLL.get_all_channel_emty()
        if results:
            for i in results: 
                print(i)
            print("FINSH - - - - - - - - - - ")
        else:
            print("No data found for getAllChannelEmty.")
    except Exception as e:
        print(f"Một lỗi đã xảy ra: {e}")

def test_server_channel():
    print ('''
           -- TEST SERVER_CHANNEL --
           ''')
    serverChannelBLL = ServerChannelBLL()
    serverBLL = ServerBLL()
    channelBLL = ChannelBLL()
    
    serverDTO = ServerDTO("a", "a")
    serverBLL.insert_server(serverDTO)
    
    channelDTO = ChannelDTO("a", "a")
    channelBLL.insert_channel(channelDTO)
    
    serverChannelBLL.insert_server_channel(ServerChannelDTO(serverDTO, channelDTO))
    
    try:
        print(serverChannelBLL.get_server_channel_by_id_server_and_id_channel("a", "a"))

        channelDTO.set_name_channel("b")
        print(channelDTO)
        channelBLL.update_channel_by_id_channel("a", channelDTO)
        
        print("\nLIST SERVER_CHANNEL DTO: BEGIN - - - -")
        results = serverChannelBLL.get_all_server_channel()
        if results:
            for i in results:
                print(i)
            print("FINSH - - - - - - - - - - ")
        else:
            print("No data found for getAllServerChannel.")
    except Exception as e:
        print(f"Một lỗi không xảy ra: {e}")
        
def test_channel_feed():   
    print ('''
           -- TEST CHANNEL_FEED --
           ''')
    channelFeedBLL = ChannelFeedBLL()
    channelBLL = ChannelBLL()
    feedBLL = FeedBLL()
    
    channelDTO = ChannelDTO("a", "a")
    channelBLL.insert_channel(channelDTO)
    
    feedDTO = FeedDTO("a", "a", "a", "a", "a", "a")
    feedBLL.insert_feed(feedDTO)
    
    channelFeedDTO = ChannelFeedDTO(channelDTO, feedDTO)
    print(channelFeedDTO)
    channelFeedBLL.insert_channel_feed(channelFeedDTO)
    
    try:
        print(channelFeedBLL.get_channel_feed_by_id_channel_and_link_atom_feed("a", "a"))
        
        feedDTO.set_description_feed("b")
        feedBLL.update_feed_by_link_atom_feed("a", feedDTO)
        
        print("\nLIST CHANNEL_FEED DTO: BEGIN - - - -")
        results = channelFeedBLL.get_all_channel_feed()    
        if results:
            for i in results:
                print(i)
            print("FINSH - - - - - - - - - - ")
        else:
            print("No data found for getAllChannelFeed.")
    except Exception as e:
        print(f"Một lỗi không xảy ra: {e}")

def test_server_color():
    print ('''
           -- TEST SERVER_COLOR --
           ''')
    serverBLL = ServerBLL()
    serverDTO = ServerDTO("b", "a")
    serverBLL.insert_server(serverDTO)
    
    colorDTO = ColorDTO("RED")
    serverColorDTO = ServerColorDTO(serverDTO, colorDTO)
    print(serverDTO)
    print(colorDTO)
    print(serverColorDTO)
    
    serverColorBLL = ServerColorBLL()
    # serverColorBLL.delete_all_server_color()
    serverColorBLL.insert_server_color(serverColorDTO)
    
    try:
        print(serverColorBLL.get_server_color_by_id_server("b"))
        serverColorDTO.set_color(ColorDTO("A"))
        serverColorBLL.update_server_color_by_id_server("b", serverColorDTO)
        # serverColorBLL.delete_server_color_by_id_server("b")
        
        print("\nLIST SERVER_COLOR DTO: BEGIN - - - -")
        results = serverColorBLL.get_all_server_color()
        if results:
            for i in results:
                print(i)
            print("FINSH - - - - - - - - - - ")
        else:
            print("No data found for getAllServerColor.")
    except Exception as e:
        print(f"Một lỗi không xảy ra: {e}")
        
def test_read_rss():
    link_atom_feed = input("Nhập link atom feed: ")
    read_rss = ReadRSS(link_atom_feed)
    print(read_rss.get_link_first_entry()) 
        
def test_feed_embeb():
    print ('''
           -- TEST EMBED --
           ''')
    # test_feed_emty()
    link_atom_feed = input("Nhập link atom feed: ")
    read_rss = ReadRSS(link_atom_feed)
    link_first_entry = read_rss.get_link_first_entry()   
    embed = FeedEmbed(link_atom_feed, link_first_entry).get_embed()
    # embed = FeedEmbed("a", "a")
    print(embed)
    