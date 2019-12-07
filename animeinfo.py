from time import time
import random
from abc import ABC, abstractmethod
import requests
import string
import os
from threading import Timer
from bs4 import BeautifulSoup
import re

'''
Планы на первый коммит:
Привести отчеты во всех файлах к виду
name
episodenow
allepisodes
url

Планы на второй коммит:
После добавить сравнение данных с базой данных
Обновление каждые 30 минут

Привести Event loop к нормальному виду

'''

class LoggerMessages:
    def __init__(self):
        self.Done = 'Done'
        self.Connect = 'Connect'
        self.ErrConnect = 'Connection Error'
        self.ProcConnect = 'ProcConnect'


class AnimeInfo(ABC):
    def __init__(self, link, onlink, namebase, name):
        self.link = link
        self.onlink = onlink
        self.days = [i for i in range(0,8)]
        self.namebase = namebase
        self.name = name
        self.loggermsg = LoggerMessages()
    # Метод запускает полное обновление списка аниме
    def full_update(self):
        self.logger(status=self.loggermsg.ProcConnect)
        t = time()
        report = self.get_links()
        self.db.push(report, hard = True)
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
    def getepisodenow(self,url):
        try:
            req = requests.get(url)
        except:
            self.logger('Connection error', status=self.loggermsg.ErrConnect)
            return False
        return req

    @abstractmethod
    def catchlinks(self, today, links):
        today = today
        links = links
        for link in links:
            epnow = self.getepisodenow(link['link'])
            epnn = link['epnow']
            if epnn == '':
                continue
            if int(epnow) == int(epnn):
                self.logger('No new episode now:{0}/base:{1}'.format(epnow,epnn))
            else:
                self.logger('New Episode now:{0}/base:{1}'.format(epnow,epnn))
                self.db.push([epnow,link])
        return True

    # Частичное обновление в зависимости от дня недели
    @abstractmethod
    def update(self, today, mins):
        links = self.db.today_links(today)
        self.catchlinks(today, links)
        
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

    
    def logger(self, message='', status=None):
        if status is None:
            print('{0} : {1}'.format(self.name, message))
        elif status is self.loggermsg.Done:
            print('[+] {0} : {1}'.format(self.name, message))
        elif status is self.loggermsg.ProcConnect:
            print('{0} connected on pid: {1}'.format(self.name, os.getpid()))

    def devonly(self):
        self.db.devfunction()