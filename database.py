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
    #Флаг hard регулирует полную вставку документов с подчищением предыдущих экземляров для fullupd
    
    def connect(self):
        connection = pymongo.MongoClient()
        db = connection.animelist
        animecol = db[self.name]
        return animecol,db

    @abstractmethod
    def push(self, data, hard = False, flag = ''):
        animecol,db = self.connect()
        for item in data:
            anime = animecol.find_one({'name': item['name']})
            if anime:
                print(f'From {anime} changed to {item}')
                animecol.update(anime, item)
            else:
                print(f'Inserting {item} into database')
                animecol.insert_one(item)
        print('Done')
        return True

    def today_links(self,nowdate):
        animecol,db = self.connect()
        animelist = []
        if animecol.find() is None:
            return False
        for anime in animecol.find():
            day = int(anime['day'])
            if day == nowdate:
                animelist.append(anime)
        return animelist            

    def get_one(self, name):
        # anime = name.lower()
        anime = name
        animecol, db = self.connect()
        return animecol.find_one({'name':anime})


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
        