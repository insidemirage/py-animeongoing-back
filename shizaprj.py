# coding=utf-8
from bs4 import BeautifulSoup
import re
from animeinfo import AnimeInfo


class Shizaprj(AnimeInfo):
    def __init__(self,link,onlink,namebase):
        super().__init__(link, onlink, namebase)
        self.cardident = 'grid-card'
        self.statusind = 'relstatus'
        self.linkident = 'card-box'
        self.topelem = 'params'

    def get_links(self):
        # TODO Дописать функцию для получения страниц онгоингов(на случай, если она будет всего одна или несколько)
        pages = [self.link+'status/ongoing',self.link+'status/ongoing?page=2']
        report = []

        for page in pages:
            req = super().get_links()
            if req is False:
                return False
            bs = BeautifulSoup(req.text, 'html.parser')
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
                elif not len(re.findall(r'\d[0-9]*', serias.text)) == 0:
                    episodenow = re.findall(r'\d[0-9]*', serias.text)[0]
                else:
                    episodenow = '1'
         #   ищем ссылку в карточке указывающую на страницу аниме
                link = card.find('a', {'class':self.linkident})
            # получаем информацию об онгоинге(все эпизоды)
                allepisodes = self.get_ongoing(link.attrs['href'])
            # получаем название онгоинга
                name = link.find('img').attrs['alt']
                print(name, episodenow, serias.text)
                id = self.randid(report, 3)
                report.append([name, episodenow, allepisodes, id])
        return report
        # проходимся по всем блокам с релизами и смотрим ссылки и названия аниме

    # Получаем количество вышедших серий и возвращаем в get_links

    def get_ongoing(self, url):
        req = super().get_ongoing(url)
        if req is not False:
            bs = BeautifulSoup(req.text, 'html.parser')
            topelem = bs.find('ul', {'class':self.topelem})
            nexitem = topelem.find_all('li')[1]
            link = nexitem.find('a')
            link = link.text
            if 'xx' in link[:3]:
                return 'xx'
            alleps = re.findall(r'\d*',link)[0]
            return alleps
        else:
            return False
