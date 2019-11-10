import csv
from abc import ABC, abstractmethod
import pymongo


class DataBase(ABC):
    def __init__(self, bdname):
        self.name = bdname
    
    #Флаг hard регулирует полную вставку документов с подчищением предыдущих экземляров для fullupd 
    @abstractmethod
    def push(self,data, hard = False):
        connection = pymongo.MongoClient()
        db = connection.animelist
        if hard is True:
            db.drop_collection(self.name)
            animecol = db[self.name]
            animecol.insert_many(data)
        else:
            animecol = db[self.name]
            anime = animecol.find_one({'_id':data[1]['_id']})
            print(data[0])
            anime['epnow'] = data[0]
            animecol.save(anime)
            print('Done')

    def today_links(self,nowdate):
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

    def push(self,data, hard = False):
        return super().push(data, hard)


class ShizaBase(DataBase):
    def __init__(self, name):
        super().__init__(name)

    def push(self,data, hard = False):
        return super().push(data, hard)
    

class AnilibriaBase(DataBase):
    def __init__(self, name):
        super().__init__(name)

    def push(self,data, hard = False):
        return super().push(data, hard)
        