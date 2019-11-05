# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
from time import sleep,time
from database import DBWriter
import random, string


class Shizaprj:
    def __init__(self):
        self.link = 'http://shiza-project.com/'
        self.ongoinglink = 'http://shiza-project.com/releases/view/1410'
        self.cardident = 'grid-card'
        self.days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье', 'Нестабильные релизы']
        filename = 'shizaprj.csv'
        self.statusind = 'relstatus'
        self.linkident = 'card-box'
        self.db = DBWriter(filename)
        self.topelem = 'params'

    def update(self):
        pass

    def full_update(self):
        t = time()
        report = self.get_links()
        self.db.push(report)
        t = time()-t
        print('Done in %d sec'%t)
        # report = self.get_links()
        # self.db.push(report)
    # Эта функция используется для получения списка всех онгоингов

    def get_links(self):
        req = requests.get(self.link+'status/ongoing')
        bs = BeautifulSoup(req.text, 'html.parser')
        report = []
        day = ''
        name = ''
        episodenow = 0
        allepisodes = 0
        id = ''
        # Проходимся по всем карточкам на главной
        for card in bs.find_all('article', {'class':self.cardident}):
        # получаем строку в которой хранятся данные о выпуске серий
            serias = card.find('span', {'class':self.statusind})
            if '-' in serias.text:
                episodenow = re.findall(r'[0-9]*-[0-9]*', serias.text)[0].split('-')[-1]
            else:
                episodenow = re.findall(r'\d[0-9]*', serias.text)[0]
        #   ищем ссылку в карточке указывающую на страницу аниме
            print(episodenow, serias.text)
            link = card.find('a', {'class':self.linkident})
            # получаем информацию об онгоинге(все эпизоды)
            allepisodes = self.get_ongoing(self.ongoinglink)
            # получаем название онгоинга
            name = link.find('img').attrs['alt']
            id = self.randid(report)
            report.append([name, episodenow, allepisodes, id])
        return report
        # проходимся по всем блокам с релизами и смотрим ссылки и названия аниме

    # Получаем количество вышедших серий и возвращаем в get_links

    def get_ongoing(self, url):
        try:
            req = requests.get(url)
            bs = BeautifulSoup(req.text, 'html.parser')
            topelem = bs.find('ul', {'class':self.topelem})
            nexitem = topelem.find_all('li')[1]
            link = nexitem.find('a')
            link = link.text
            if 'xx' in link[:3]:
                return 'xx'
            alleps = re.findall(r'\d*',link)[0]
            return alleps
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
            ids.append(i[3])
        if id in ids:
            return False
        else:
            return True
