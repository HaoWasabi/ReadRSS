
from bot.DAL.EmtyDAL import EmtyDAL
from bot.DAL.FeedEmtyDAL import FeedEmtyDAL
from bot.DAL.FeedDAL import FeedDAL
from bot.DTO.EmtyDTO import EmtyDTO
from bot.DTO.FeedDTO import FeedDTO
from bot.DTO.FeedEmtyDTO import FeedEmtyDTO
from bot.utils.ReadRSS import ReadRSS

def clear():
    FeedDAL = FeedDAL()
    FeedDAL.deleteAllFeed()
    EmtyDAL = EmtyDAL()
    EmtyDAL.deleteAllEmty()
    FeedEmtyDAL = FeedEmtyDAL()
    FeedEmtyDAL.deleteAllFeedEmty()
    
if __name__ == "__main__":
    ReadRSS("https://fetchrss.com/rss/66692c903413f4ff7e03b4e2666fdd5607b27c15980a5e02.xml")

    
    