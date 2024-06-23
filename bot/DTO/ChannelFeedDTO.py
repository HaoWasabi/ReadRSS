class ChannelFeedDTO:
    def __init__(self, link_feed,id_server):
        self.link_feed = link_feed
        self.id_server=id_server

    def __str__(self):
        return f"ChannelFeedDTO(link_feed={self.link_feed}, id_server={self.id_server})"

    def setLink_feed(self, link_feed):
        self.link_feed=link_feed

    def setId_server(self, id_server):
        self.id_server=id_server

    def getLink_feed(self):
        return self.link_feed

    def getId_server(self):
        return self.id_server

