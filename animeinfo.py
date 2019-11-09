from time import time
from database import DBWriter
import random
from abc import ABC, abstractmethod
import requests
import string
import os


class AnimeInfo(ABC):
    def __init__(self, link, onlink, namebase, name):
        self.link = link
        self.onlink = onlink
        self.days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье', 'Нестабильные релизы']
        self.db = DBWriter(namebase)
        self.namebase = namebase
        self.name = name

    # Метод запускает полное обновление списка аниме
    def full_update(self):
        print('Process pid:{0} name: {1}'.format(os.getpid(),self.namebase.split('.')[0]))
        t = time()
        report = self.get_links()
        self.db.push(report)
        t = time()-t
        self.logger('Done in %d sec'%t)
        if report is None:
            return False
        elif report is []:
            return False
        elif report is False:
            return False
        else:
            return True

    @abstractmethod
    def get_links(self, url=None):
        if url is None:
            url = self.onlink
        else:
            url = url

        try:
            req = requests.get(url)
        except requests.exceptions as e:
            print(e)
            return False
        return req

    @abstractmethod
    def get_ongoing(self,url):
        if isinstance(url,str):
            try:
                req = requests.get(url)
            except Exception as e:
                print(e)
                return False
            return req
        else:
            return False

    # Рандомим id для аниме
    def randid(self, ids, idpos):
        letters = string.ascii_lowercase
        ident = ''.join(random.choice(letters) for i in range(10))
        if len(ids) == 1:
            return ident
        elif self.check_id(ids, ident, idpos) is False:
            self.randid(ids, idpos)
        else:
            return ident

    # Проверяем, существует ли такой id в нашем списке ids

    @staticmethod
    def check_id(ids, ident,idpos):
        ids = ids
        identificators = []
        for i in ids:
            identificators.append(i[idpos])

        if ident in identificators:
            return False
        else:
            return True

    def logger(self,message, status = None):
        if status is None:
            print('{0} : {1}'.format(self.name,message))
        elif status is "Done":
            print('[+] {0} : {1}'.format(self.name,message))