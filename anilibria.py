from bs4 import BeautifulSoup
import re
from animeinfo import AnimeInfo


class Anilibria(AnimeInfo):
    def __init__(self, link, onlink, namebase):
        super().__init__(link, onlink,namebase)

        self.linksident = 'test'
        self.linksanime = 'goodcell'
        self.animename = 'schedule-runame'
        self.epnowid = 'schedule-series'
        self.seriaident = 'shortstoryHead'

    def get_links(self):
        req = super().get_links()
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
                id = self.randid(report, 3)
                report.append([name, day,episodenow, id])
        return report

    def get_ongoing(self, url):
        super().get_ongoing(url)
