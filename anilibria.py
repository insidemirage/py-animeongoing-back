import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from database import DBWriter
import random, string

class Anilibria:
    def __init__(self):
        self.link = 'https://www.anilibria.tv'
        self.rasplink = 'https://www.anilibria.tv/pages/schedule.php'
        self.linksident = 'test'
        self.linksanime = 'goodcell'
        self.animename = 'schedule-runame'
        self.epnowid = 'schedule-series'
        # self.linksident = self.linksident.split(', ')
        self.days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        self.seriaident = 'shortstoryHead'
        filename = 'anilibria.csv'
        self.db = DBWriter(filename)

    def update(self):
        pass

    def full_update(self):
        report = self.get_links()
        self.db.push(report)

    def get_links(self):
        req = requests.get(self.rasplink)
        soup = BeautifulSoup(req.text, 'html.parser')
        report = []
        day = ''
        name = ''
        episodenow = 0
        allepisodes = 0
        i = 0
        id = ''
        t = ''  # time переменная
        for animesblock in soup.find_all('table',{'class':self.linksident}):
            day = self.days[i]
            i += 1
            for anime in animesblock.find_all('td',{'class':self.linksanime}):
                link = anime.find('a')
                name = link.find('span',{'class':self.animename}).text
                eps = link.find('span',{'class':self.epnowid})
                episodenow = re.findall(r'\d[0-9]*', eps.text)
                if len(episodenow) == 1:
                    episodenow = episodenow[0]
                else:
                    episodenow = episodenow[1]
                id = self.randid(report)
                report.append([name, day,episodenow, id])
        return report
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

