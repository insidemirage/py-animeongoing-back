# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
from time import sleep, time
from database import DBWriter
import random, string


class Animevost:
    def __init__(self):
        self.link = 'https://a30.agorov.org'
        self.linksident = 'raspisMon, raspisTue'
        # , raspisWed, raspisThu, raspisFri, raspisSat, raspisSun, raspisNest'
        self.linksident = self.linksident.split(', ')
        #
        self.days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье', 'Нестабильные релизы']
        self.seriaident = 'shortstoryHead'
        filename = 'animevost.csv'
        self.db = DBWriter(filename)

    def update(self):
        pass

    def full_update(self):
        starttime = time()
        report = self.get_links()
        self.db.push(report)
        endtime = time()-starttime
        print('Done in %d s'%endtime)
    # Эта функция используется для получения списка всех онгоингов

    def get_links(self):
        req = requests.get(self.link)
        bs = BeautifulSoup(req.text, 'html.parser')
        report = []
        day = ''
        name = ''
        episodenow = 0
        allepisodes = 0
        i = 0
        id = ''
        t = '' #time переменная
        # проходимся по всем блокам с релизами и смотрим ссылки и названия аниме
        for ident in self.linksident:
            for block in bs.find_all('div', {'id': ident}):
                day = self.days[i]
                for a in block.find_all('a'):
                    name = a.text
                    t = self.get_time(name)

                    if a.attrs['href'][0] == '/':
                        href = self.link + a.attrs['href']
                    else:
                        href = self.link + '/' + a.attrs['href']
                    episodez = self.get_ongoing(href)
                    episodenow, allepisodes = episodez[0], episodez[1]
                    if episodenow is False:
                        continue
                    id = self.randid(report)

                    report.append([name, day, t, episodenow, allepisodes, id])
                    print(a.text, ' Done')
                    sleep(1)
        return report
    # Получаем количество вышедших серий и возвращаем в get_links

    def get_ongoing(self, url):
        try:
            req = requests.get(url)
            bs = BeautifulSoup(req.text, 'html.parser')
            episodes = bs.find('div',{'class':self.seriaident})
            episodenow = re.findall(r'\w[0-9]*-[0-9]*',episodes.text)[0].split('-')[-1]
            episodelast = re.findall(r'из [0-9]*', episodes.text)[0].replace('из ', '')
            return [episodenow,episodelast]
        except:
            return False

    def push_db(self, report):
        self.db.push(report)

    def randid(self,database):
        letters = string.ascii_lowercase
        id =  ''.join(random.choice(letters) for i in range(10))
        if len(database) == 1:
            return id
        if self.check_id(database, id) is False:
            self.randid(database)
        else:
            return id

    def check_id(self, database, id):
        ids = []
        for i in database:
            ids.append(i[4])
        if id in ids:
            return False
        else:
            return True

    def get_time(self,name):
        t = re.findall(r'([0-9]*:[0-9]*)',name)
        return t
