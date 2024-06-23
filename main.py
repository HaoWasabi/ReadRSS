from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.EmtyDTO import EmtyDTO
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.ServerDTO import ServerDTO
from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.DTO.ChannelEmtyDTO import ChannelEmtyDTO
from bot.DTO.ServerChannelDTO import ServerChannelDTO
from bot.BLL.FeedBLL import FeedBLL
from bot.BLL.EmtyBLL import EmtyBLL
from bot.BLL.ServerBLL import ServerBLL
from bot.BLL.ChannelBLL import ChannelBLL
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL
from bot.BLL.ChannelEmtyBLL import ChannelEmtyBLL
from bot.BLL.ServerChannelBLL import ServerChannelBLL
from bot.utils.Database import Database
from bot.utils.ReadRSS import ReadRSS
from bot.GUI.Embed import Embed
from bot.GUI.Bot import bot
import os

def clear():
    db = Database()
    db.clear()

def readRSS():
    ReadRSS("https://fetchrss.com/rss/66692c903413f4ff7e03b4e2666fdd5607b27c15980a5e02.xml")

def test_feed_emty():
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
    
        print("____")
        for i in feedEmtyBLL.getAllFeedEmty(): 
            print(i)
    except Exception as e:
        print(f"Một lỗi đã xảy ra: {e}")

def test_channel_emty():
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
    
        print("____")
        results = channelEmtyBLL.getAllChannelEmty()
        if results:
            for i in results: 
                print(i)
        else:
            print("No data found for getAllChannelEmty.")
    except Exception as e:
        print(f"Một lỗi đã xảy ra: {e}")

def test_server_channel():
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
        
        print("____")
        results = serverChannelBLL.getAllServerChannel()
        if results:
            for i in results:
                print(i)
        else:
            print("No data found for getAllServerChannel.")
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
    
    # __EMBED_TESTING__
    # test_feed_emty()
    # embed = Embed("a", "a", "RED")
    # print(embed)
    
    # __BOT_RUNNING__
    # run()