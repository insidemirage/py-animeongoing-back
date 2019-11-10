import csv
from abc import ABC, abstractmethod
import pymongo

class FlagsBD:
    def __init__(self):
        self.PUSHONE = 'PUSHONE'
        self.DELETEBD = 'DELETEBD'
        self.REMOVECOL = 'REMOVECOL'

class DataBase(ABC):
    def __init__(self, bdname):
        self.name = bdname
        self.flags = FlagsBD()  
        print(self.flags.PUSHONE)  
    #Флаг hard регулирует полную вставку документов с подчищением предыдущих экземляров для fullupd 
    @abstractmethod
    def push(self,data, hard = False, flag = ''):
        connection = pymongo.MongoClient()
        db = connection.animelist
        # TODO привести в нормальный вид эту функцию
        if hard is True:
            db.drop_collection(self.name)
            animecol = db[self.name]
            animecol.insert_many(data)
        elif flag is self.flags.PUSHONE:
            animecol = db[self.name]
            animecol.insert_one(data)
        else:
            animecol = db[self.name]
            anime = animecol.find_one({'_id':data[1]['_id']})
            print(data[0])
            anime['epnow'] = data[0]
            animecol.save(anime)
            print('Done')
        return True

    def today_links(self,nowdate):
        # TODO нужно что то сделать с коннектами к базе, это выглядит ужасно
        connection = pymongo.MongoClient()
        db = connection.animelist
        collection = db[self.name]
        animelist = []
        # TODO сделать исключение для пустого списка
        for anime in collection.find():
            day = int(anime['day'])
            if day == nowdate:
                animelist.append(anime)
        return animelist            

    def get_one(self):
        pass

    # ONLY FOR DEV CHANGING ONE ANIME VALUES
    def devfunction(self):
        connection = pymongo.MongoClient()
        db = connection.animelist
        collection = db[self.name]
        anime = collection.find_one({'day':6})
        anime['epnow'] = 1
        collection.save(anime)

class AnimevostBase(DataBase):
    def __init__(self, name):
        super().__init__(name)

    def push(self,data, hard = False, flag = None):
        return super().push(data, hard, flag)


class ShizaBase(DataBase):
    def __init__(self, name):
        super().__init__(name)

    def push(self,data, hard = False, flag = None):
        return super().push(data, hard, flag)
    

class AnilibriaBase(DataBase):
    def __init__(self, name):
        super().__init__(name)

    def push(self,data, hard = False, flag = None):
        return super().push(data, hard, flag)
        