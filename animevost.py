# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from database import DBWriter


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

    # Эта функция используется для получения списка всех онгоингов
    def get_links(self):
        req = requests.get(self.link)
        bs = BeautifulSoup(req.text, 'html.parser')
        report = []
        day = ''
        name = ''
        episodenow = 0
        episodelast = 0
        i = 0
        # проходимся по всем блокам с релизами и смотрим ссылки и названия аниме
        for ident in self.linksident:
            for block in bs.find_all('div', {'id': ident}):
                day = self.days[i]
                for a in block.find_all('a'):
                    name = a.text
                    if a.attrs['href'][0] == '/':
                        href = self.link + a.attrs['href']
                    else:
                        href = self.link + '/' + a.attrs['href']
                    episodenow = self.get_ongoing(href)
                    if episodenow is False:
                        continue
                    report.append([name, day, episodenow])
                    print(a.text, ' Done')
                    sleep(1)
        self.push_db(report)
    # Получаем количество вышедших серий и возвращаем в get_links

    def get_ongoing(self, url):
        try:
            req = requests.get(url)
            bs = BeautifulSoup(req.text, 'html.parser')
            episodes = bs.find('div',{'class':self.seriaident})
            episodenow = re.findall(r'\w[0-9]*-[0-9]*',episodes.text)[0].split('-')[-1]
            return episodenow
        except:
            return False

    def push_db(self, report):
        self.db.push(report)

    def test(self):
        print('Animevost working!')