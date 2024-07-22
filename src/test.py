from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.EmtyDTO import EmtyDTO
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.ServerDTO import ServerDTO
from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.DTO.ChannelEmtyDTO import ChannelEmtyDTO
from bot.DTO.ChannelFeedDTO import ChannelFeedDTO
from bot.DTO.ServerChannelDTO import ServerChannelDTO
from bot.BLL.FeedBLL import FeedBLL
from bot.BLL.EmtyBLL import EmtyBLL
from bot.BLL.ServerBLL import ServerBLL
from bot.BLL.ChannelBLL import ChannelBLL
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL
from bot.BLL.ChannelEmtyBLL import ChannelEmtyBLL
from bot.BLL.ChannelFeedBLL import ChannelFeedBLL
from bot.BLL.ServerChannelBLL import ServerChannelBLL
from bot.GUI.FeedEmbed import FeedEmbed
from bot.utils.ReadRSS import ReadRSS

def testFeedEmty():
    print ('''
           -- TEST FEED_EMTY --
           ''')
    feedEmtyBLL = FeedEmtyBLL()
    feedBLL = FeedBLL()
    emtyBLL = EmtyBLL()
    
    feedDTO = FeedDTO("a", "a", "a", "a", "a", "a")
    feedBLL.insertFeed(feedDTO)
    
    emtyDTO = EmtyDTO("a", "a", "a", "a", "a")
    emtyBLL.insertEmty(emtyDTO)
    
    feedEmtyBLL.insertFeedEmty(FeedEmtyDTO(feedDTO, emtyDTO))
    
    try:
        print(feedEmtyBLL.getFeedEmtyByLinkAtom_feedAndLink_emty("a", "a"))
           
        emtyDTO.setPubDate_emty("m")
        print(emtyDTO)
        emtyBLL.updateEmtyByLink_emty("a", emtyDTO)
    
        feedEmtyDTO = FeedEmtyDTO(feedDTO, emtyDTO)
        feedEmtyBLL.updateFeedEmtyByLinkAtom_feedAndLink_emty("a", "a", feedEmtyDTO)
    
        print("\nLIST FEED_EMTY DTO: BEGIN - - - -")
        for i in feedEmtyBLL.getAllFeedEmty(): 
            print(i)
        print("FINSH - - - - - - - - - - ")
    except Exception as e:
        print(f"Một lỗi đã xảy ra: {e}")

def testChannelEmty():
    print ('''
           -- TEST CHANNEL_EMTY --
           ''')
    channelEmtyBLL = ChannelEmtyBLL()
    channelBLL = ChannelBLL()
    emtyBLL = EmtyBLL()
    
    channelDTO = ChannelDTO("a", "a")
    channelBLL.insertChannel(channelDTO)
    
    emtyDTO = EmtyDTO("a", "a", "a", "a", "a")
    emtyBLL.insertEmty(emtyDTO)
    
    channelEmtyBLL.insertChannelEmty(ChannelEmtyDTO(channelDTO, emtyDTO))
    
    try:
        print(channelEmtyBLL.getChannelEmtyById_channelAndLink_emty("a", "a"))
    
        emtyDTO.setPubDate_emty("m")
        print(emtyDTO)
        emtyBLL.updateEmtyByLink_emty("a", emtyDTO)
    
        channelEmtyDTO = ChannelEmtyDTO(channelDTO, emtyDTO)
        channelEmtyBLL.updateChannelEmtyById_channelAndLink_emty("a", "a", channelEmtyDTO)
    
        print("\nLIST CHANNEL_EMTY DTO: BEGIN - - - -")
        results = channelEmtyBLL.getAllChannelEmty()
        if results:
            for i in results: 
                print(i)
            print("FINSH - - - - - - - - - - ")
        else:
            print("No data found for getAllChannelEmty.")
    except Exception as e:
        print(f"Một lỗi đã xảy ra: {e}")

def testServerChannel():
    print ('''
           -- TEST SERVER_CHANNEL --
           ''')
    serverChannelBLL = ServerChannelBLL()
    serverBLL = ServerBLL()
    channelBLL = ChannelBLL()
    
    serverDTO = ServerDTO("a", "a")
    serverBLL.insertServer(serverDTO)
    
    channelDTO = ChannelDTO("a", "a")
    channelBLL.insertChannel(channelDTO)
    
    serverChannelBLL.insertServerChannel(ServerChannelDTO(serverDTO, channelDTO))
    
    try:
        print(serverChannelBLL.getServerChannelById_serverAndId_channel("a", "a"))

        channelDTO.setName_channel("b")
        print(channelDTO)
        channelBLL.updateChannelById_channel("a", channelDTO)
        
        serverChannelDTO = ServerChannelDTO(serverDTO, channelDTO)
        serverChannelBLL.updateServerChannelById_serverAndId_channel("a", "a", serverChannelDTO)
        
        print("\nLIST SERVER_CHANNEL DTO: BEGIN - - - -")
        results = serverChannelBLL.getAllServerChannel()
        if results:
            for i in results:
                print(i)
            print("FINSH - - - - - - - - - - ")
        else:
            print("No data found for getAllServerChannel.")
    except Exception as e:
        print(f"Một lỗi không xảy ra: {e}")
        
def testChannelFeed():   
    print ('''
           -- TEST CHANNEL_FEED --
           ''')
    channelFeedBLL = ChannelFeedBLL()
    channelBLL = ChannelBLL()
    feedBLL = FeedBLL()
    
    channelDTO = ChannelDTO("a", "a")
    channelBLL.insertChannel(channelDTO)
    
    feedDTO = FeedDTO("a", "a", "a", "a", "a", "a")
    feedBLL.insertFeed(feedDTO)
    
    channelFeedDTO = ChannelFeedDTO(channelDTO, feedDTO)
    print(channelFeedDTO)
    channelFeedBLL.insertChannelFeed(channelFeedDTO)
    
    try:
        print(channelFeedBLL.getChannelFeedById_channelAndLinkAtom_feed("a", "a"))
        
        feedDTO.setDescription_feed("b")
        feedBLL.updateFeedByLinkAtom_feed("a", feedDTO)
        
        channelFeedDTO = ChannelFeedDTO(channelDTO, feedDTO)
        channelFeedBLL.updateChannelFeedById_channelAndLinkAtom_feed("a", "a", channelFeedDTO)
        
        print("\nLIST CHANNEL_FEED DTO: BEGIN - - - -")
        results = channelFeedBLL.getAllChannelFeed()    
        if results:
            for i in results:
                print(i)
            print("FINSH - - - - - - - - - - ")
        else:
            print("No data found for getAllChannelFeed.")
    except Exception as e:
        print(f"Một lỗi không xảy ra: {e}")
        
def testReadRSS():
    link_atom_feed = input("Nhập link atom feed: ")
    read_rss = ReadRSS(link_atom_feed)
    print(read_rss.getLink_firstEntry()) 
        
def testFeedEmbeb():
    print ('''
           -- TEST EMBED --
           ''')
    # testFeedEmty()
    link_atom_feed = input("Nhập link atom feed: ")
    read_rss = ReadRSS(link_atom_feed)
    link_first_entry = read_rss.getLink_firstEntry()   
    embed = FeedEmbed(link_atom_feed, link_first_entry).get_embed()
    # embed = FeedEmbed("a", "a")
    print(embed)
    
def testChannel():
    channelBLL = ChannelBLL()
    for channelDTO in channelBLL.getAllChannel():
        print(channelDTO)