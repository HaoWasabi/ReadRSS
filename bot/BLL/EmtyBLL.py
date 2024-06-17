from bot.DAL.EmtyDAL import EmtyDAL

class EmtyBLL:
    def __init__(self):
        self.EmtyDAL = EmtyDAL()
    
    def insertEmty(self, emty_dto):
        return self.EmtyDAL.insertEmty(emty_dto)

    def deleteEmtyByLink_emty(self, emty_link):
        return self.EmtyDAL.deleteEmtyByLink_emty(emty_link)

    def deleteAllEmty(self):
        return self.EmtyDAL.deleteAllEmty()

    def updateEmtyByLink_emty(self, emty_link, emty_dto):
        return self.EmtyDAL.updateEmtyByLink_emty(emty_link, emty_dto)

    def getEmtyByLink_emty(self, emty_link):
        return self.EmtyDAL.getEmtyByLink_emty(emty_link)

    def getAllEmty(self):
        return self.EmtyDAL.getAllEmty()
    