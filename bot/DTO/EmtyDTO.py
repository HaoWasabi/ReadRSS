class EmtyDTO:
    def __init__(self, link_emty, title_emty, description_emty, image_emty, pubDate_emty):
        self.link_emty = link_emty
        self.title_emty = title_emty
        self.description_emty = description_emty
        self.image_emty = image_emty
        self.pubDate_emty = pubDate_emty
        
    def __str__(self):
        return f"EmtyDTO(link_emty={self.link_emty}, title_emty={self.title_emty}, description_emty={self.description_emty}, image_emty={self.image_emty}), pubDate_emty={self.pubDate_emty})"
        
    def setLink_emty(self, link_emty):
        self.link_emty = link_emty
    
    def setTitle_emty(self, title_emty):
        self.title_emty = title_emty
    
    def setDescription_emty(self, description_emty):
        self.description_emty = description_emty
    
    def setImage_emty(self, image_emty):
        self.image_emty = image_emty
    
    def setPubDate_emty(self, pubDate_emty):
        self.pubDate_emty = pubDate_emty
    
    def getLink_emty(self):
        return self.link_emty
    
    def getTitle_emty(self):
        return self.title_emty
    
    def getDescription_emty(self):
        return self.description_emty
    
    def getImage_emty(self):
        return self.image_emty
    
    def getPubDate_emty(self):
        return self.pubDate_emty