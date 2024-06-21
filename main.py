from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.EmtyDTO import EmtyDTO
from bot.DTO.ChannelDTO import ChannelDTO
from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.DTO.ChannelEmtyDTO import ChannelEmtyDTO
from bot.BLL.FeedBLL import FeedBLL
from bot.BLL.EmtyBLL import EmtyBLL
from bot.BLL.ChannelBLL import ChannelBLL
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL
from bot.BLL.ChannelEmtyBLL import ChannelEmtyBLL
from bot.GUI.embed.Embed import Embed
from bot.utils.Database import Database
from bot.utils.ReadRSS import ReadRSS

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
        for i in feedEmtyBLL.getFeedEmtyByLink_feedAndLink_emty("a", "a"):
            print(i)
    
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
        results = channelEmtyBLL.getChannelEmtyById_channelAndId_emty("a", "a")
        if results:
            for i in results:
                print(i)
        else:
            print("No data found for getChannelEmtyById_channel.")
    
        emtyDTO.setPubDate_emty("m")
        print(emtyDTO)
        emtyBLL.updateEmtyById_channelAndLink_emty("a", "a", emtyDTO)
    
        channelEmtyDTO = ChannelEmtyDTO(channelDTO, emtyDTO)
        channelEmtyBLL.updateChannelEmtyById_channelAndLink_emty("a", "a", channelEmtyDTO)
    
        results = channelEmtyBLL.getAllChannelEmty()
        if results:
            for i in results: 
                print(i)
        else:
            print("No data found for getAllChannelEmty.")
    except Exception as e:
        print(f"Một lỗi đã xảy ra: {e}")

if __name__ == "__main__":
    clear()
    
    # __TESTING__
    # test_feed_emty()
    # embed = Embed("a", "a")
    # print(embed)
