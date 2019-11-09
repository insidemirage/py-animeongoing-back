# coding=utf-8
from bs4 import BeautifulSoup
import re
from animeinfo import AnimeInfo


class Animevost(AnimeInfo):

    def __init__(self, link, onlink, namebase,name):
        super().__init__(link, onlink, namebase,name)
        self.linksident = 'raspisMon, raspisTue, raspisWed, raspisThu, raspisFri, raspisSat, raspisSun, raspisNest'
        self.linksident = self.linksident.split(', ')
        self.seriaident = 'shortstoryHead'

    # Функция для получения списка онгоингов
    def get_links(self):
        req = super().get_links()
        if req is False:
            return False
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
                i += 1
                for a in block.find_all('a'):
                    name = a.text
                    t = self.get_time(name)

                    if a.attrs['href'][0] == '/':
                        href = self.link + a.attrs['href']
                    else:
                        href = self.link + '/' + a.attrs['href']
                    episodez = self.get_ongoing(href)
                    if episodez is False:
                        continue
                    episodenow, allepisodes = episodez[0], episodez[1]
                    if episodenow is False:
                        continue
                    identificator = self.randid(report,5)

                    report.append([name, day, t, episodenow, allepisodes, identificator])
                    log = '{0},{1},{2},now:{3},all:{4}'.format(name,day,t,episodenow,allepisodes)
                    self.logger(log, status='Done')
        return report
    # Получаем количество вышедших серий и возвращаем в get_links

    def get_ongoing(self, url):
        req = super().get_ongoing(url)
        if req is False:
            return False
        bs = BeautifulSoup(req.text, 'html.parser')
        episodes = bs.find('div',{'class':self.seriaident})
        episodenow = re.findall(r'\w[0-9]*-[0-9]*',episodes.text)[0].split('-')[-1]
        episodelast = re.findall(r'из [0-9]*', episodes.text)[0].replace('из ', '')
        return [episodenow,episodelast]

    # Получаем время обновления серии
    @staticmethod
    def get_time(name):
        t = re.findall(r'([0-9]*:[0-9]*)', name)
        if len(t) > 0:
            return t[-1]
        else:
            return 'ninfo'


