from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.EmtyDTO import EmtyDTO
from bot.BLL.FeedEmtyBLL import FeedEmtyBLL
from bot.BLL.FeedBLL import FeedBLL
from bot.BLL.EmtyBLL import EmtyBLL
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
        for i in feedEmtyBLL.getFeedEmtyByLink_feed("a"):
            print(i)
    
        emtyDTO.setPubDate_emty("m")
        print(emtyDTO)
        emtyBLL.updateEmtyByLink_emty("a", emtyDTO)
    
        feedEmtyDTO = FeedEmtyDTO(feedDTO, emtyDTO)
        feedEmtyBLL.updateFeedEmtyByLink_emty("a", feedEmtyDTO)  # Ensure feedEmtyDTO is passed correctly
    
        print("____")
        for i in feedEmtyBLL.getAllFeedEmty(): 
            print(i)
    except Exception as e:
        print(f"Một lỗi đã xảy ra: {e}")

if __name__ == "__main__":
    clear()
    # test_feed_emty()
    # readRSS()