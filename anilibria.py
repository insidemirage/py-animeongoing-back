from bs4 import BeautifulSoup
import re
from animeinfo import AnimeInfo
from database import AnilibriaBase

class Anilibria(AnimeInfo):
    def __init__(self, link, onlink, namebase, name):
        super().__init__(link, onlink, namebase, name)

        self.linksident = 'test'
        self.linksanime = 'goodcell'
        self.animename = 'schedule-runame'
        self.epnowid = 'schedule-series'
        self.seriaident = 'shortstoryHead'
        self.db = AnilibriaBase('anilibria')
    def get_links(self):
        req = super().get_links()
        soup = BeautifulSoup(req.text, 'html.parser')
        report = []
        day = ''
        name = ''
        episodenow = 0
        allepisodes = 0
        i = 0
        t = ''  # time переменная
        for animesblock in soup.find_all('table',{'class':self.linksident}):
            day = self.days[i]
            i += 1
            for anime in animesblock.find_all('td',{'class':self.linksanime}):
                link = anime.find('a')
                url = link.attrs['href']
                name = link.find('span',{'class':self.animename}).text
                eps = link.find('span',{'class':self.epnowid})
                episodenow = re.findall(r'\d[0-9]*', eps.text)
                if len(episodenow) == 1:
                    episodenow = episodenow[0]
                else:
                    episodenow = episodenow[1]
                log = '{0},{1},{2}'.format(name,day,episodenow)
                self.logger(log,status=self.loggermsg.Done)
                report.append({
                    'name':name,
                    'day':day,
                    'epnow':episodenow,
                    'url':url
                })
        return report

    def get_ongoing(self, url):
        super().get_ongoing(url)

    def update(self, today, mins):
        return super().update(today, mins)

    def catchlinks(self, today, links):
        return super().catchlinks(today, links)

    def getepisodenow(self, url):
        return super().getepisodenow(url)
        