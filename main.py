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
from bot.DAL.ChannelFeedDAL import ChannelFeedDAL
from bot.BLL.ServerChannelBLL import ServerChannelBLL
from bot.utils.Database import Database
from bot.utils.ReadRSS import ReadRSS
from bot.GUI.Embed import Embed
from bot.GUI.Bot import bot
import os

def about_us():
    print('''
This is a Discord bot built with Python, ReadRSS bot brings RSS feeds 
to your Discord server. Receive notifications from news sources 
including Facebook and much more. 

                        -- ABOUT US --
                         
         ██████╗  ██████╗██████╗ ███████╗██╗   ██╗     #GCdev24
        ██╔════╝ ██╔════╝██╔══██╗██╔════╝██║   ██║     HaoWasabi
        ██║  ███╗██║     ██║  ██║█████╗  ██║   ██║     NaelTuhline
        ██║   ██║██║     ██║  ██║██╔══╝  ╚██╗ ██╔╝     tivibin789
        ╚██████╔╝╚██████╗██████╔╝███████╗ ╚████╔╝   
        ╚═════╝  ╚═════╝╚═════╝ ╚══════╝  ╚═══╝                                                                 
''')

def clear():
    db = Database()
    db.clear()

def readRSS():
    ReadRSS("https://fetchrss.com/rss/66692c903413f4ff7e03b4e2666fdd5607b27c15980a5e02.xml")

def test_feed_emty():
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
        print(feedEmtyBLL.getFeedEmtyByLink_feedAndLink_emty("a", "a"))
           
        emtyDTO.setPubDate_emty("m")
        print(emtyDTO)
        emtyBLL.updateEmtyByLink_emty("a", emtyDTO)
    
        feedEmtyDTO = FeedEmtyDTO(feedDTO, emtyDTO)
        feedEmtyBLL.updateFeedEmtyByLink_feedAndLink_emty("a", "a", feedEmtyDTO)
    
        print("\nLIST FEED_EMTY DTO: BEGIN - - - -")
        for i in feedEmtyBLL.getAllFeedEmty(): 
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

def test_server_channel():
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
        
def test_channel_feed():   
    print ('''
           -- TEST CHANNEL_FEED --
           ''')
    channelFeedDAL = ChannelFeedDAL()
    channelBLL = ChannelBLL()
    feedBLL = FeedBLL()
    
    channelDTO = ChannelDTO("a", "a")
    channelBLL.insertChannel(channelDTO)
    
    feedDTO = FeedDTO("a", "a", "a", "a", "a", "a")
    feedBLL.insertFeed(feedDTO)
    
    channelFeedDTO = ChannelFeedDTO(channelDTO, feedDTO)
    print(channelFeedDTO)
    channelFeedDAL.insertChannelFeed(channelFeedDTO)
    
    try:
        print(channelFeedDAL.getChannelFeedById_channelAndLink_feed("a", "a"))
        
        feedDTO.setDescription_feed("b")
        feedBLL.updateFeedByLink_feed("a", feedDTO)
        
        channelFeedDTO = ChannelFeedDTO(channelDTO, feedDTO)
        channelFeedDAL.updateChannelFeedById_channelAndLink_feed("a", "a", channelFeedDTO)
        
        print("\nLIST CHANNEL_FEED DTO: BEGIN - - - -")
        results = channelFeedDAL.getAllChannelFeed()    
        if results:
            for i in results:
                print(i)
            print("FINSH - - - - - - - - - - ")
        else:
            print("No data found for getAllChannelFeed.")
    except Exception as e:
        print(f"Một lỗi không xảy ra: {e}")
    
def run():
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("TOKEN không được tìm thấy trong file .env.")
    
if __name__ == "__main__":
    clear()
    
    # __RSS_TESTING__
    # readRSS()
    
    # __DAL_TESTING__
    # test_channel_emty()
    # test_server_channel()
    # test_feed_emty()
    # test_channel_feed()
    
    # __EMBED_TESTING__
    # test_feed_emty()
    # embed = Embed("https://www.facebook.com/TuoitrekhoaCongngheThongtinSGU", "https://www.facebook.com/814717200441834/posts/957235702856649",  "RED")
    # print(embed)
    
    # __BOT_RUNNING__
    # run()
    about_us()