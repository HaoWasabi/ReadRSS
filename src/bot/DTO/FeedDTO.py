class FeedDTO:
    def __init__(self, link_feed, linkAtom_feed, title_feed, description_feed, logo_feed, pubDate_feed):
        self.__link_feed = link_feed
        self.__linkAtom_feed = linkAtom_feed
        self.__title_feed = title_feed
        self.__description_feed = description_feed
        self.__logo_feed = logo_feed
        self.__pubDate_feed = pubDate_feed

    def __str__(self):
        return f"FeedDTO(link_feed={self.__link_feed}, linkAtom_feed={self.__linkAtom_feed}, title_feed={self.__title_feed}, description_feed={self.__description_feed}, logo_feed={self.__logo_feed}, pubDate_feed={self.__pubDate_feed})"

    def setLink_feed(self, link_feed):
        self.__link_feed = link_feed
    
    def setLinkAtom_feed(self, linkAtom_feed):
        self.__linkAtom_feed = linkAtom_feed
        
    def setTitle_feed(self, title_feed):
        self.__title_feed = title_feed
    
    def setDescription_feed(self, description_feed):
        self.__description_feed = description_feed
    
    def setLogo_feed(self, logo_feed):
        self.__logo_feed = logo_feed
    
    def setPubDate_feed(self, pubDate_feed):
        self.__pubDate_feed = pubDate_feed
    
    def getLink_feed(self):
        return self.__link_feed
    
    def getLinkAtom_feed(self):
        return self.__linkAtom_feed
    
    def getTitle_feed(self):
        return self.__title_feed
    
    def getDescription_feed(self):
        return self.__description_feed
    
    def getLogo_feed(self):
        return self.__logo_feed
    
    def getPubDate_feed(self):
        return self.__pubDate_feed
    