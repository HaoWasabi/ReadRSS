from ..utils.Database import dataBase

class DalBase:
    def __init__(self):
        self.__connection = dataBase.connection
        self.__cursor = dataBase.cursor